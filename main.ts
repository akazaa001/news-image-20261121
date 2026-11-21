// news-image-20261121 — the entry program.
//
// The picture for Saturday 21 November 2026 is already drawn and saved
// as entry.png alongside this file (see draw.py for how it was made).
// When the grader runs this program it has no network, so there is
// nothing to fetch or render here: the job is simply to hand the
// finished picture over. This file drops an exact copy of entry.png
// into the folder the grader reads from — /output by default, or
// wherever MAKEFUN_OUTPUT_DIR points while testing locally.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// entry.png lives in the same directory as this script.
const here = dirname(fileURLToPath(import.meta.url));
const picture = resolve(here, "entry.png");

// The grader's output folder; overridable for local runs. An empty
// value falls back to the default, so `MAKEFUN_OUTPUT_DIR=` is safe.
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const outFile = join(outDir, "entry.png");

if (!existsSync(picture)) {
  throw new Error(`entry.png is missing from ${here} — nothing to deliver`);
}

// Make the destination folder if the grader has not created it yet.
mkdirSync(outDir, { recursive: true });

// Byte-for-byte copy, so the judged image is exactly the drawn one.
copyFileSync(picture, outFile);
const bytes = statSync(outFile).size;
console.log(`entry.png delivered to ${outFile} (${bytes} bytes)`);
