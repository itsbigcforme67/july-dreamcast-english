import numpy as np
from PIL import Image,ImageDraw,ImageFont
CW,CH=13,26
import os
_cands=[os.environ.get('JULY_FONT',''),'/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
        '/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf','/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf',
        '/Library/Fonts/DejaVuSansMono-Bold.ttf','C:/Windows/Fonts/DejaVuSansMono-Bold.ttf']
_font=next((p for p in _cands if p and os.path.exists(p)),None)
if not _font: raise SystemExit('DejaVuSansMono-Bold.ttf not found; set JULY_FONT to its path')
F=ImageFont.truetype(_font,19)
_c={}
def glyph(c):
    if c in _c: return _c[c]
    im=Image.new('L',(CW*3,CH),0); dr=ImageDraw.Draw(im)
    w=dr.textlength(c,font=F); dr.text((CW+(CW-w)/2,21),c,font=F,fill=255,anchor='ls')
    a=np.asarray(im)[:,CW:2*CW].astype(float)
    a=np.clip(np.round(a/255*15*1.1),0,15).astype(np.uint8); _c[c]=a; return a
def build(orig_path,table,out_path):
    d=np.frombuffer(open(orig_path,'rb').read(),np.uint8)
    p=np.empty(d.size*2,np.uint8); p[0::2]=d>>4; p[1::2]=d&15
    g=p.reshape(3440,26,26).copy()
    for pr,idx in table.map.items():
        if idx==0: continue
        g[idx]=np.concatenate([glyph(pr[0]),glyph(pr[1])],axis=1)
    f=g.reshape(-1); out=(f[0::2]<<4)|f[1::2]
    open(out_path,'wb').write(out.astype(np.uint8).tobytes())
