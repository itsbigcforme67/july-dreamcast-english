# Technical notes

These notes describe what the tools in `tools/` rely on. Offsets refer to
`July v2.000 (1998)(Fortyfive)(JP)[!]`.

## Disc

- GDI with three tracks. `track03.bin` uses raw 2352-byte Mode 1 sectors and
  starts at LBA 45000. The ISO9660 volume descriptor is at LBA 45016.
- Game files start around LBA 294735; the area from LBA 50000 up to there is
  padding. Files that grow are relocated into that padding (`tools/disc.py`),
  and the directory records (LBA and size, both byte orders) are updated.
- EDC/ECC for every rewritten sector is recomputed (`tools/ecc.c`).

## Script files (`/SNR/*.BIN`)

- Header: `u32 count`, `u32 8`.
- Then `count` records of 40 bytes: opcode, seven arguments, and two pointers.
  Pointers are absolute file offsets into the string area that follows.
- Text opcodes: `0x05` speech (argument selects the speaker), `0x0d`
  monologue, `0x0f` hero line, `0x2b` narration, `0x1a` / `0x1b` two- and
  three-way choices (the second string holds the options).
- Control codes inside strings: `%N` newline, `%K` wait for button, `%E` clear,
  `%O` end, `%S<n>` speed. A pair of tabs marks the start of a line.
- A line that exactly fills the box wraps on its own, so it must not be
  followed by `%N` or a blank line appears.
- `tools/build.py` rebuilds the whole string area compactly, so translated
  files stay close to their original size.

## Layout limits used by the build

| Box | Characters per line | Lines |
|---|---|---|
| Narration | 26 | 5 |
| Speech / monologue | 36 | 3 |
| Choice question | 26 | 2 |
| Choice option | 26 | 2 |

Text that does not fit is split into pages automatically.

## Font (`/SONOTA/FNT2626.BIN`)

- 3440 glyphs, 26x26 pixels, 4 bits per pixel, in JIS order.
- English is encoded as two-character tiles. Each distinct letter pair used by
  the script is drawn into a 26x26 cell (two 13-pixel half cells) and assigned
  to a glyph slot from index 170 upward, reusing kanji the English script does
  not need. About 1,350 pairs are in use.

## Executable (`1ST_READ.BIN`, loaded at `0x8c010000`)

- UI strings, speaker names, location names, character files and chapter
  summaries live in the executable and are reached through 32-bit pointers.
- `data/exe_refs.json` lists string offsets and the locations of the pointers
  that reference them (addresses only, no game text).
- `tools/exepatch.py` frees the space used by the original strings, packs the
  translated ones into it and repoints every reference. Space is tight, so
  the character files are written concisely.

## Patch format

`patch/track03.xdelta` is plain VCDIFF (RFC 3284) without secondary
compression, so it works with xdelta3 and Delta Patcher. `patch/vcdiff.py` is
a small pure-Python encoder/decoder used by `apply_patch.py`.
