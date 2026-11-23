// A news-image-20261122 entry (Node 22, standard library only): its image is
// the entry.png beside this file, and the program copies it to /output/entry.png.
// The image is a 1024x1024 newspaper front page summing up the world news of
// Sunday 22 November 2026; it was drawn by generate.py (Pillow + Liberation
// fonts, deterministic, no network) from the wires of that day. The gate takes
// a whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge
// sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
