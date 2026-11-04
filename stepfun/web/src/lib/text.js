const SENTENCE_BOUNDARY = /(?<=[。！？.!?])\s+/u;

export function normalizeDocumentText(value) {
  return String(value ?? "")
    .replace(/^\uFEFF/, "")
    .replace(/\r\n?/g, "\n")
    .replace(/\u0000/g, "")
    .trim();
}

function findNaturalCut(text, maxChars) {
  const window = text.slice(0, maxChars + 1);
  const candidates = [
    window.lastIndexOf("\n"),
    window.lastIndexOf("。"),
    window.lastIndexOf("！"),
    window.lastIndexOf("？"),
    window.lastIndexOf(". "),
    window.lastIndexOf("! "),
    window.lastIndexOf("? "),
    window.lastIndexOf(" "),
  ];
  const best = Math.max(...candidates);
  return best >= Math.floor(maxChars * 0.55) ? best + 1 : maxChars;
}

function splitLongBlock(block, maxChars) {
  const pieces = [];
  let remaining = block;
  while (remaining.length > maxChars) {
    const cut = findNaturalCut(remaining, maxChars);
    pieces.push(remaining.slice(0, cut).trim());
    remaining = remaining.slice(cut).trim();
  }
  if (remaining) {
    pieces.push(remaining);
  }
  return pieces;
}

function overlapTail(text, overlapChars) {
  if (overlapChars <= 0 || text.length <= overlapChars) {
    return text;
  }
  const tail = text.slice(-overlapChars);
  const boundary = tail.search(/[。！？.!?]\s*/u);
  return boundary >= 0 ? tail.slice(boundary + 1).trimStart() : tail;
}

export function chunkText(
  value,
  { maxChars = 1_200, overlapChars = 120 } = {},
) {
  if (!Number.isInteger(maxChars) || maxChars < 100) {
    throw new Error("maxChars must be an integer of at least 100");
  }
  if (
    !Number.isInteger(overlapChars) ||
    overlapChars < 0 ||
    overlapChars >= maxChars
  ) {
    throw new Error("overlapChars must be smaller than maxChars");
  }

  const text = normalizeDocumentText(value);
  if (!text) {
    return [];
  }

  const blocks = text
    .split(/\n\s*\n+/u)
    .flatMap((block) => {
      const normalized = block.replace(/\s+/g, " ").trim();
      if (!normalized) {
        return [];
      }
      if (normalized.length <= maxChars) {
        return [normalized];
      }
      return normalized
        .split(SENTENCE_BOUNDARY)
        .flatMap((sentence) => splitLongBlock(sentence.trim(), maxChars))
        .filter(Boolean);
    });

  const chunks = [];
  let current = "";
  for (const block of blocks) {
    const candidate = current ? `${current}\n${block}` : block;
    if (candidate.length <= maxChars) {
      current = candidate;
      continue;
    }

    if (current) {
      chunks.push(current);
      current = `${overlapTail(current, overlapChars)}\n${block}`.trim();
    } else {
      current = block;
    }

    if (current.length > maxChars) {
      const split = splitLongBlock(current, maxChars);
      chunks.push(...split.slice(0, -1));
      current = split.at(-1) || "";
    }
  }
  if (current) {
    chunks.push(current);
  }

  return chunks.map((chunk, index) => ({
    index,
    text: chunk,
    charCount: chunk.length,
  }));
}

export async function sha256Hex(value) {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), (byte) =>
    byte.toString(16).padStart(2, "0"),
  ).join("");
}

export function titleFromFilename(filename) {
  return filename
    .replace(/\.[^.]+$/, "")
    .replace(/[_-]+/g, " ")
    .trim()
    .slice(0, 200);
}

export function inferTitle(text, fallback = "未命名文档") {
  const firstLine = normalizeDocumentText(text)
    .split("\n")
    .map((line) => line.replace(/^#+\s*/, "").trim())
    .find((line) => line.length >= 2 && line.length <= 120);
  return (firstLine || fallback).slice(0, 200);
}

export function formatDuration(milliseconds) {
  if (!Number.isFinite(milliseconds)) {
    return "—";
  }
  if (milliseconds < 1) {
    return "<1 ms";
  }
  if (milliseconds < 1_000) {
    return `${Math.round(milliseconds)} ms`;
  }
  return `${(milliseconds / 1_000).toFixed(2)} s`;
}
