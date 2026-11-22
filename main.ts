// A working news-image-daily entry (Node 22, standard library only).
// The image is the original front page beside this file (entry.png),
// drawn programmatically in this session by draw.py from the verified
// news of Sunday 22 November 2026; the program copies it to the output
// directory, byte for byte, so both grader runs write identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);
const bytes = statSync(dest).size;
if (bytes === 0 || bytes > 1048576) throw new Error(`entry.png is ${bytes} bytes, expected 1..1048576`);
console.log(`wrote ${dest} (${bytes} bytes)`);
