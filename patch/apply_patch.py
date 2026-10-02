#!/usr/bin/env python3
"""JULY (Dreamcast) English patch applier.
Usage: python3 apply_patch.py /path/to/original/gdi/folder
Writes a patched copy to a new folder 'JULY English' next to this script.
Needs only Python 3 (no xdelta). The .xdelta also works with xdelta3/Delta Patcher."""
import sys,os,shutil,glob,zlib
EXPECTED=1122769753
here=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,here); import vcdiff
src=sys.argv[1] if len(sys.argv)>1 else here
gdis=glob.glob(os.path.join(src,'*.gdi'))
if not gdis: sys.exit('No .gdi found in '+src)
for f in ('track01.bin','track02.raw','track03.bin'):
    if not os.path.exists(os.path.join(src,f)): sys.exit('Missing '+f)
print('Checking original track03.bin...')
c=0
with open(os.path.join(src,'track03.bin'),'rb') as fh:
    for b in iter(lambda: fh.read(1<<24),b''): c=zlib.crc32(b,c)
if c!=EXPECTED: print('WARNING: track03.bin CRC %08x does not match the expected %08x; patching anyway.'%(c,EXPECTED))
out=os.path.join(here,'JULY English'); os.makedirs(out,exist_ok=True)
print('Patching track03.bin (takes a minute or two)...')
vcdiff.decode(os.path.join(src,'track03.bin'),os.path.join(here,'track03.xdelta'),os.path.join(out,'track03.bin'))
for f in ('track01.bin','track02.raw'): shutil.copy(os.path.join(src,f),os.path.join(out,f))
shutil.copy(gdis[0],os.path.join(out,'July (English).gdi'))
print('Done! Load "%s" in your emulator.'%os.path.join(out,'July (English).gdi'))
