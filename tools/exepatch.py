"""Translate strings in 1ST_READ.BIN: encode, allocate into freed holes, repoint."""
import json,os,re,sys,struct
sys.path.insert(0,os.path.dirname(__file__))
import enc
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import R,W
BASE=0x8c010000
def load_tr():
    tr={}
    for fn in ('bios','summ','misc','bg','labels','ui'):
        p=f'{R}/text/exe/{fn}.txt'
        if not os.path.exists(p): continue
        for line in open(p,encoding='utf-8'):
            line=line.rstrip('\n')
            if not line or line.startswith('#'): continue
            off,txt=line.split('|',1)
            tr[int(off,16)]=txt.replace('\\n','\n')
    return tr
def layout(T,txt,W,maxl,warn,tag):
    lines=enc.wrap(txt,W)
    if len(lines)>maxl: warn.append(f'{tag}: {len(lines)} lines > {maxl}')
    out='%E%S0'; full=False
    for j,l in enumerate(lines):
        e=T.enc_line(l).decode('cp932')
        if j>0 and not full: out+='%N'
        out+='\t\t'+e; full=len(e)>=W//2
    return out+'%O'
def encode(T,off,txt,warn):
    if 0x5863c<=off<0x5e03c: return layout(T,txt,26,9,warn,hex(off)).encode('cp932')
    if 0x5e03c<=off<0x60390: return layout(T,txt,36,6,warn,hex(off)).encode('cp932')
    if '%' in txt:
        out=b''
        for part in re.split(r'(%Y-C0X40|%S\d|%[ENOK])',txt):
            if part.startswith('%'): out+=part.encode()
            elif part: out+=T.enc_line(part)
        return out
    return T.enc_line(txt)
def patch(T,exe):
    warn=[]
    d=bytearray(exe)
    m=json.load(open(R+'/data/exe_refs.json'))
    refs={int(k):v for k,v in m['refs'].items()}
    starts=set(refs); allstr=set(m['strs'])
    tr=load_tr()
    new={}
    for off,txt in tr.items():
        assert off in refs, hex(off)
        new[off]=encode(T,off,txt,warn)
    # holes
    holes=[]
    for off in sorted(new):
        end=off+d.index(b'\0',off)-off+1
        e2=end
        while d[e2] in (0,0xff) and e2 not in starts and e2-end<16: e2+=1
        if e2 in allstr: end=e2
        else:
            while end%4 and d[end]==0 and end not in starts: end+=1
        if holes and holes[-1][1]==off: holes[-1][1]=end
        else: holes.append([off,end])
    total=sum(b-a for a,b in holes); need=sum(len(s)+1 for s in set(new.values()))
    print(f'exe: holes {total} bytes, need {need}')
    for a,b in holes: d[a:b]=b'\0'*(b-a)
    # dedupe
    placed={}
    for off,s in sorted(new.items(),key=lambda kv:-len(kv[1])):
        if s in placed: addr=placed[s]
        else:
            n=len(s)+1; best=None
            for h in holes:
                a=h[0]
                if h[1]-a>=n and (best is None or h[1]-a<best[1]-best[0]): best=h
            if best is None: raise Exception(f'no room for {hex(off)} ({n} bytes)')
            a=best[0]; d[a:a+n]=s+b'\0'; best[0]=a+n; addr=a; placed[s]=a
        for r in refs[off]:
            assert struct.unpack_from('<I',d,r)[0]==BASE+off, (hex(off),hex(r))
            struct.pack_into('<I',d,r,BASE+addr)
    free=sum(b-a for a,b in holes)
    print(f'exe: {len(new)} strings, {free} bytes left')
    return bytes(d),warn
if __name__=='__main__':
    T=enc.Table()
    exe=open(W+'/fs/1ST_READ.BIN','rb').read()
    out,warn=patch(T,exe)
    for w in warn: print('WARN',w)
