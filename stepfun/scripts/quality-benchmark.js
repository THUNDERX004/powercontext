import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright-core";

const baseUrl = process.env.STEPFUN_BASE_URL || "http://127.0.0.1:3000";
const executablePath =
  process.env.BROWSER_EXECUTABLE ||
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const qualityBackend = process.env.QUALITY_BACKEND || "auto";
const dtypes = (process.env.QUALITY_DTYPES || "fp32,fp16")
  .split(",")
  .map((value) => value.trim())
  .filter((value) => value === "fp32" || value === "fp16");
const repeats = Math.max(
  1,
  Math.min(5, Number.parseInt(process.env.QUALITY_REPEATS || "3", 10)),
);
const outputDirectory = path.resolve("results/quality");
fs.mkdirSync(outputDirectory, { recursive: true });

function median(values) {
  const sorted = values
    .filter((value) => Number.isFinite(value))
    .sort((left, right) => left - right);
  if (!sorted.length) {
    return null;
  }
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2
    ? sorted[middle]
    : (sorted[middle - 1] + sorted[middle]) / 2;
}

function aggregateRuns(dtypeRuns) {
  const first = dtypeRuns[0];
  return {
    ...first,
    model: {
      ...first.model,
      firstLoadMs: first.model.loadMs,
      warmedLoadMedianMs: median(
        dtypeRuns.slice(1).map((run) => run.model.loadMs),
      ),
      loadSamplesMs: dtypeRuns.map((run) => run.model.loadMs),
      downloadedBytes: first.model.downloadedBytes,
    },
    timings: {
      ...first.timings,
      documentEmbeddingSamplesMs: dtypeRuns.map(
        (run) => run.timings.documentEmbeddingMs,
      ),
      documentEmbeddingMedianMs: median(
        dtypeRuns.map((run) => run.timings.documentEmbeddingMs),
      ),
      documentThroughputMedianPerSecond: median(
        dtypeRuns.map((run) => run.timings.documentThroughputPerSecond),
      ),
      queryEmbeddingMedianSamplesMs: dtypeRuns.map(
        (run) => run.timings.queryEmbeddingMedianMs,
      ),
      queryEmbeddingMedianOfMediansMs: median(
        dtypeRuns.map((run) => run.timings.queryEmbeddingMedianMs),
      ),
    },
    runs: dtypeRuns,
    repeatCount: dtypeRuns.length,
  };
}

const browser = await chromium.launch({
  executablePath,
  headless: true,
  args: [
    "--enable-unsafe-webgpu",
    "--enable-features=Vulkan",
    "--disable-gpu-sandbox",
  ],
});
const context = await browser.newContext();
const results = {};

try {
  for (const dtype of dtypes) {
    const dtypeRuns = [];
    for (let repeat = 0; repeat < repeats; repeat += 1) {
      const page = await context.newPage();
      const pageErrors = [];
      page.on("pageerror", (error) => pageErrors.push(error.message));
      await page.goto(
        `${baseUrl}/benchmark.html?dtype=${dtype}&backend=${encodeURIComponent(qualityBackend)}&batch=8&repeat=${repeat}`,
        { waitUntil: "domcontentloaded", timeout: 30_000 },
      );
      await page.waitForFunction(
        () => ["complete", "error"].includes(document.body.dataset.status),
        null,
        { timeout: 300_000 },
      );
      const result = await page.evaluate(() => window.__QUALITY_BENCHMARK__);
      if (!result || result.ok === false) {
        throw new Error(
          `${dtype} benchmark failed: ${result?.error || "unknown error"}`,
        );
      }
      if (pageErrors.length) {
        result.pageErrors = pageErrors;
      }
      result.repeat = repeat;
      dtypeRuns.push(result);
      if (repeat === 0) {
        await page.screenshot({
          path: path.join(
            outputDirectory,
            `quality-${dtype}-${qualityBackend}.png`,
          ),
          fullPage: true,
        });
      }
      await page.close();
    }
    const aggregate = aggregateRuns(dtypeRuns);
    results[dtype] = aggregate;
    fs.writeFileSync(
      path.join(outputDirectory, `quality-${dtype}-${qualityBackend}.json`),
      `${JSON.stringify(aggregate, null, 2)}\n`,
    );
  }

  const summary = {
    schemaVersion: 1,
    timestamp: new Date().toISOString(),
    model: results.fp16.model.id,
    revision: results.fp16.model.revision,
    backend: results.fp16?.model.backend || results.fp32.model.backend,
    modelBytes: {
      fp32Weights: 90_318_300,
      fp16Weights: 45_184_187,
      compressionRatio: 90_318_300 / 45_184_187,
    },
    fp32: results.fp32
      ? {
          quality: results.fp32.quality,
          timings: results.fp32.timings,
          model: results.fp32.model,
        }
      : null,
    fp16: results.fp16
      ? {
          quality: results.fp16.quality,
          timings: results.fp16.timings,
          model: results.fp16.model,
        }
      : null,
    deltas:
      results.fp32 && results.fp16
        ? Object.fromEntries(
            Object.keys(results.fp32.quality).map((metric) => [
              metric,
              results.fp16.quality[metric] - results.fp32.quality[metric],
            ]),
          )
        : null,
  };
  fs.writeFileSync(
    path.join(outputDirectory, `summary-${qualityBackend}.json`),
    `${JSON.stringify(summary, null, 2)}\n`,
  );
  console.log(JSON.stringify(summary, null, 2));
} finally {
  await context.close();
  await browser.close();
}
