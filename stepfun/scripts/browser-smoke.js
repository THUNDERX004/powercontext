import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright-core";

const baseUrl = process.env.STEPFUN_BASE_URL || "http://127.0.0.1:3000";
const executablePath =
  process.env.BROWSER_EXECUTABLE ||
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const disableWebGPU = process.env.STEPFUN_DISABLE_WEBGPU === "1";
const evidenceName = disableWebGPU ? "browser-smoke-wasm" : "browser-smoke-webgpu";
const artifactDirectory = path.resolve("results/evidence");
fs.mkdirSync(artifactDirectory, { recursive: true });

if (!fs.existsSync(executablePath)) {
  throw new Error(`Browser executable not found: ${executablePath}`);
}

const browser = await chromium.launch({
  executablePath,
  headless: true,
  args: [
    "--enable-unsafe-webgpu",
    "--enable-features=Vulkan",
    "--disable-gpu-sandbox",
    ...(disableWebGPU
      ? [
          "--disable-gpu",
          "--disable-software-rasterizer",
          "--disable-features=WebGPU,Vulkan",
        ]
      : []),
  ],
});

const context = await browser.newContext({
  viewport: { width: 1440, height: 1200 },
  deviceScaleFactor: 1,
});
if (disableWebGPU) {
  await context.addInitScript(() => {
    Object.defineProperty(navigator, "gpu", {
      configurable: true,
      value: undefined,
    });
  });
}
const page = await context.newPage();
const browserEvents = [];
const importResponses = [];
page.on("console", (message) => {
  browserEvents.push({
    type: `console:${message.type()}`,
    text: message.text(),
  });
});
page.on("pageerror", (error) => {
  browserEvents.push({ type: "pageerror", text: error.message });
});
page.on("requestfailed", (request) => {
  browserEvents.push({
    type: "requestfailed",
    text: `${request.url()} :: ${request.failure()?.errorText || "unknown"}`,
  });
});
page.on("response", async (response) => {
  if (
    response.request().method() === "POST" &&
    /\/api\/knowledge-bases\/[^/]+\/documents$/.test(response.url())
  ) {
    try {
      const body = await response.json();
      if (response.ok()) {
        importResponses.push(body);
      }
    } catch {
      // The page-level browser events capture malformed responses.
    }
  }
});

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

try {
  await page.goto(baseUrl, {
    waitUntil: "domcontentloaded",
    timeout: 30_000,
  });
  await page.waitForFunction(
    () => {
      const text =
        document.querySelector("#runtimeStatusText")?.textContent || "";
      return /WebGPU|WASM/.test(text) && !/正在|加载|检测/.test(text);
    },
    null,
    { timeout: 240_000 },
  );

  const runtimeLabel = await page.locator("#runtimeStatusText").innerText();
  const databaseLabel = await page.locator("#dbStatusText").innerText();
  if (disableWebGPU && !runtimeLabel.includes("WASM")) {
    throw new Error(`Expected WASM fallback, received ${runtimeLabel}`);
  }
  await page.getByRole("button", { name: "装入示例知识" }).click();
  await page.waitForFunction(
    () => {
      const toasts = Array.from(document.querySelectorAll(".toast"));
      return toasts.some((toast) =>
        /已导入 8 份示例文档/.test(toast.textContent || ""),
      );
    },
    null,
    { timeout: 240_000 },
  );

  const query = "WebGPU 不可用时如何降级？";
  await page.locator("#searchInput").fill(query);
  await page.locator("#searchForm").evaluate((form) => form.requestSubmit());
  await page.waitForFunction(
    () => document.querySelectorAll(".result-card").length > 0,
    null,
    { timeout: 90_000 },
  );
  await page.waitForFunction(
    () => document.querySelector("#searchButton")?.disabled === false,
    null,
    { timeout: 30_000 },
  );

  const resultTitles = await page.locator(".result-card h3").allTextContents();
  const firstTrace = await page.evaluate(
    () => globalThis.__stepfunDiagnostics?.().lastTrace,
  );
  const primarySearchSamples = firstTrace ? [firstTrace] : [];
  for (let repeat = 1; repeat < 5; repeat += 1) {
    const previousTimestamp =
      primarySearchSamples.at(-1)?.timestamp || "1970-01-01T00:00:00.000Z";
    await page.locator("#searchForm").evaluate((form) => form.requestSubmit());
    await page.waitForFunction(
      (previous) => {
        const trace = globalThis.__stepfunDiagnostics?.().lastTrace;
        const button = document.querySelector("#searchButton");
        return (
          trace?.timestamp > previous &&
          trace?.resultCount > 0 &&
          !button?.disabled
        );
      },
      previousTimestamp,
      { timeout: 30_000 },
    );
    primarySearchSamples.push(
      await page.evaluate(
        () => globalThis.__stepfunDiagnostics?.().lastTrace,
      ),
    );
  }
  const timing = {
    embedding: await page.locator("#embeddingTime").innerText(),
    search: await page.locator("#searchTime").innerText(),
    total: await page.locator("#totalTime").innerText(),
  };
  const primaryDiagnostics = await page.evaluate(() =>
    globalThis.__stepfunDiagnostics?.(),
  );
  const screenshotPath = path.join(artifactDirectory, `${evidenceName}.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  const primaryKb = await page.evaluate(
    () => globalThis.__stepfunDiagnostics?.().knowledgeBase,
  );
  const isolatedName = `隔离验收 ${Date.now()}`;
  await page.getByRole("button", { name: "新建知识库" }).click();
  await page.locator("#newKbName").fill(isolatedName);
  await page.getByRole("button", { name: "创建知识库", exact: true }).click();
  await page.waitForFunction(
    () => document.querySelector("#documentCount")?.textContent === "0",
    null,
    { timeout: 30_000 },
  );
  const isolatedKb = await page.evaluate(
    () => globalThis.__stepfunDiagnostics?.().knowledgeBase,
  );
  await page.locator("#searchInput").fill("这个知识库不应命中其他集合");
  await page.locator("#searchForm").evaluate((form) => form.requestSubmit());
  await page.waitForFunction(
    () => document.querySelectorAll(".result-card").length === 0,
    null,
    { timeout: 30_000 },
  );
  await page
    .getByRole("button", { name: new RegExp(primaryKb.name) })
    .click();
  await page.waitForFunction(
    () => document.querySelector("#documentCount")?.textContent === "8",
    null,
    { timeout: 30_000 },
  );
  await page.evaluate(async (kbId) => {
    await fetch(`/api/knowledge-bases/${encodeURIComponent(kbId)}`, {
      method: "DELETE",
    });
  }, isolatedKb.id);
  await page.waitForTimeout(250);
  const finalDiagnostics = await page.evaluate(() =>
    globalThis.__stepfunDiagnostics?.(),
  );

  const report = {
    ok: true,
    baseUrl,
    browser: await browser.version(),
    runtimeLabel,
    databaseLabel,
    primaryDiagnostics,
    finalDiagnostics,
    query,
    resultCount: resultTitles.length,
    resultTitles,
    timing,
    searchMedians: {
      queryEmbeddingMs: median(
        primarySearchSamples.map((trace) => trace.timings.queryEmbeddingMs),
      ),
      databaseSearchMs: median(
        primarySearchSamples.map((trace) => trace.timings.databaseSearchMs),
      ),
      endToEndMs: median(
        primarySearchSamples.map((trace) => trace.timings.endToEndMs),
      ),
      sampleCount: primarySearchSamples.length,
      samples: primarySearchSamples.map((trace) => ({
        timestamp: trace.timestamp,
        ...trace.timings,
      })),
    },
    stateIsolation: {
      primaryKnowledgeBase: primaryKb?.id,
      temporaryKnowledgeBase: isolatedKb?.id,
      emptyCollectionResultCount: 0,
      switchedBackDocumentCount: Number(
        await page.locator("#documentCount").innerText(),
      ),
    },
    importTimings: {
      count: importResponses.length,
      embeddingMedianMs: median(
        primaryDiagnostics?.importHistory?.map(
          (item) => item.timings.embeddingMs,
        ) || [],
      ),
      indexRefreshMedianMs: median(
        importResponses.map((item) => item.timings.indexRefreshMs),
      ),
      visibilityWaitMedianMs: median(
        importResponses.map((item) => item.timings.visibilityWaitMs),
      ),
      writeMedianMs: median(
        importResponses.map((item) => item.timings.writeMs),
      ),
    },
    screenshot: screenshotPath,
    browserEvents,
  };
  fs.writeFileSync(
    path.join(artifactDirectory, `${evidenceName}.json`),
    `${JSON.stringify(report, null, 2)}\n`,
  );
  console.log(JSON.stringify(report, null, 2));
} finally {
  await context.close();
  await browser.close();
}
