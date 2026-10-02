JULY (Dreamcast, Fortyfive 1998) - English translation patch v1.0
Base image: July v2.000 (1998)(Fortyfive)(JP)[!] (GDI, 3 tracks)

HOW TO APPLY
 Option A (no extra software):
   python3 apply_patch.py "/path/to/folder/with/original/gdi"
   (the folder must contain the .gdi and the three track files directly)
   This creates "JULY English/" next to the script with the patched GDI set.
 Option B: apply track03.xdelta to track03.bin with xdelta3 / Delta Patcher:
   xdelta3 -d -s track03.bin track03.xdelta track03_en.bin
   then rename it to track03.bin next to the original track01/track02 + .gdi.
Only track03 changes; tracks 1 and 2 and the .gdi are untouched.

Translated: full script (both routes), choices, name plates, character
files, location names, chapter titles and summaries, save/load messages.
Still Japanese: a few pre-rendered graphics; save names in the BIOS.

Unofficial, non-commercial fan project. No game data is included.
