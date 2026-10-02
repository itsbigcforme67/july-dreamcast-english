# JULY (Dreamcast) English Translation Patch

An unofficial English fan translation of **JULY** (Fortyfive, 1998), a Dreamcast
launch-window visual novel that was only ever released in Japan.

This repository contains a **patch**, not the game. You need your own copy of
the original disc image to use it.

## Status: v1.0

Translated:

- The complete script for both routes, Makoto and Joshua (15,125 lines)
- All choices
- Speaker name plates
- Character files (bios), affiliations and location names
- Chapter titles and chapter summaries
- Save / load messages

Not translated yet:

- Some pre-rendered graphics (a few title cards) are still in Japanese
- Save file names shown in the Dreamcast BIOS memory manager

Known risks:

- Only the opening chapters have been play-tested so far. If the game hangs
  or shows garbled text anywhere, please open an issue and say which route and
  chapter you were in (a screenshot helps a lot).

## What you need

- The original game as a GDI image:
  `July v2.000 (1998)(Fortyfive)(JP)[!]` (three tracks: `track01.bin`,
  `track02.raw`, `track03.bin`, plus the `.gdi` file)
- Python 3 (any recent version; no extra packages needed to apply the patch)

Only `track03.bin` is changed. Tracks 1 and 2 and the `.gdi` are untouched.

## How to apply

### Option A: the included script (no extra software)

Download the latest release zip, unpack it, then run:

```
python3 apply_patch.py "/path/to/folder/with/the/original/gdi"
```

The folder you pass must have the `.gdi` and the three track files directly
inside it. The script checks the original, then writes a patched copy to a
new folder called `JULY English` next to the script. Open
`JULY English/July (English).gdi` in your emulator (tested with Flycast) or
put the folder on your GDEMU / ODE SD card.

### Option B: xdelta3 or Delta Patcher

`track03.xdelta` is a standard VCDIFF file.

```
xdelta3 -d -s track03.bin track03.xdelta track03_en.bin
```

Rename the result to `track03.bin` and keep it next to the original
`track01.bin`, `track02.raw` and `.gdi`.

## Reporting problems

Use the Issues tab. Useful details: route (Makoto / Joshua), chapter, what you
saw, and a screenshot if you can. Typos and awkward lines are welcome too.

## How it works

The game only has a fixed-width 26x26 Japanese font, so English is drawn as
two-character tiles: each pair of letters becomes one glyph that replaces a
kanji slot the English script no longer needs. See [docs/FORMATS.md](docs/FORMATS.md)
for notes on the script format, the font, the executable and the disc layout.

## Building from source

The tools in `tools/` rebuild the patched disc from your own copy of the game
plus a set of translation files. The repository does not include any game
data, and the translation sources are maintained outside this public
repository, so this section is mainly useful as documentation or if you want
to adapt the tools for another translation.

```
mkdir work            # put track01.bin, track02.raw, track03.bin and the .gdi here
python3 tools/gdx.py      # extract the disc filesystem to work/fs
python3 tools/extract.py  # dump the Japanese script to text/jp
python3 tools/build.py    # build work/patched/ from text/en and text/exe
python3 tools/vcdiff.py e work/track03.bin work/patched/track03.bin patch/track03.xdelta
```

Requirements for building: Python 3 with `numpy` and `Pillow`, a C compiler
(`cc`), and the DejaVu Sans Mono Bold font.

## Credits

- Translation, hacking and tools: **Big C**
- Original game: Fortyfive (1998)

The tools in `tools/` and `patch/` are released under the MIT license (see
[LICENSE](LICENSE)). That license covers the code only, not the game or its
script.

## Legal

This is an unofficial, non-commercial fan project. It is not affiliated with
or endorsed by Fortyfive or Sega. JULY and all related characters and artwork
belong to their respective owners. No game data is distributed here; please
support the original release and use your own copy of the game.
