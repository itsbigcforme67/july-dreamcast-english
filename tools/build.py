import json,glob,os,re,sys,struct
sys.path.insert(0,os.path.dirname(__file__))
import snr,enc,fontgen,disc
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import R,W
LAYOUT={'narr':(26,5),'say':(36,3),'mono':(36,3),'hero':(36,3),'ask2':(26,2),'ask3':(26,2)}
PAGE='%K%E'
T=enc.Table()
warn=[]
def split_ends(jp):
    pre=re.match(r'^((?:\t|%S\d+)*)',jp).group(1)
    suf=re.search(r'((?:%K|%E|%O|%N|\t)*)$',jp).group(1)
    return pre,suf
def encode_entry(e,en,fname):
    op=e['op']; jp=e['jp']; slot=e['id'][-1]
    W,NL=LAYOUT[op]
    if op in('ask2','ask3') and slot=='1':
        opts=en if isinstance(en,list) else en.split(' // ')
        lines=[]
        for o in opts:
            ol=enc.wrap(o,W)
            if len(ol)>2: warn.append(f'{fname} {e["id"]} option too long: {o}')
            lines+= (ol+[''])[:2]
        body=''; full_prev=False
        for j,l in enumerate(lines):
            e2=T.enc_line(l).decode('cp932')
            if j>0: body+=('' if full_prev else '%N')+'\t\t'
            body+=e2; full_prev=len(e2)>=W//2
        return ('\t\t'+body+'\t\t')
    pre,suf=split_ends(jp)
    pages=[]
    for chunk in en.split('||'):
        ls=enc.wrap(chunk.strip(),W)
        while ls: pages.append(ls[:NL]); ls=ls[NL:]
    if len(pages)>1: warn.append(f'{fname} {e["id"]} paginated ({len(pages)} pages)')
    def pg_enc(pg,first):
        out=''
        for j,l in enumerate(pg):
            e=T.enc_line(l).decode('cp932')
            if j>0: out+='' if full_prev else '%N'
            out+=('\t\t' if (j>0 or not first) else '')+e
            full_prev=len(e)>=W//2
        return out
    sep=PAGE+('%N%N' if op=='narr' else '')
    body=sep.join(pg_enc(pg,i==0) for i,pg in enumerate(pages))
    if op in('ask2','ask3'):
        suf=suf if suf.startswith('%N') else '%N'
    return pre+body+suf
def build(only=None):
    outdir=W+'/out/SNR'; os.makedirs(outdir,exist_ok=True)
    files={}
    for f in sorted(glob.glob(R+'/text/en/*.json')):
        name=os.path.basename(f)[:-5]
        if only and name not in only: continue
        en=json.load(open(f)); jp={e['id']:e for e in json.load(open(R+f'/text/jp/{name}.json'))}
        d,recs,base,strs=snr.load(W+f'/fs/SNR/{name}.BIN')
        newstr={}
        for i,r in enumerate(recs):
            for slot in (0,1):
                k=f'{i}.{slot}'
                if k in en: newstr[(i,slot)]=encode_entry(jp[k],en[k],name).encode('cp932')
        # compact rebuild of string area
        out=bytearray(d[:base]); pool={}
        for i,r in enumerate(recs):
            for slot in (0,1):
                p=r[8+slot]
                if p<base: continue
                s=newstr.get((i,slot),strs[p])
                if s not in pool:
                    pool[s]=len(out); out+=s+b'\0'
                struct.pack_into('<i',out,8+i*40+32+4*slot,pool[s])
        d=out
        while len(d)%4: d+=b'\0'
        files['/SNR/'+name+'.BIN']=bytes(d)
    return files
if __name__=='__main__':
    files=build()
    import exepatch
    exe,ew=exepatch.patch(T,open(W+'/fs/1ST_READ.BIN','rb').read()); warn+=ew
    files['/1ST_READ.BIN']=exe
    print('pairs used',len(T.map),'of',len(enc.SLOTS))
    fontgen.build(W+'/fs/SONOTA/FNT2626.BIN',T,W+'/out/FNT2626.BIN')
    files['/SONOTA/FNT2626.BIN']=open(W+'/out/FNT2626.BIN','rb').read()
    os.makedirs(W+'/patched',exist_ok=True)
    D=disc.Disc(W+'/track03.bin',W+'/patched/track03.bin')
    for p,data in files.items(): D.replace(p,data)
    D.close()
    import shutil
    for fn in ('track01.bin','track02.raw'):
        if not os.path.exists(W+'/patched/'+fn): os.link(W+'/'+fn,W+'/patched/'+fn)
    shutil.copy(glob.glob(W+'/*.gdi')[0],W+'/patched/July (English).gdi')
    for w in warn: print('WARN',w)
    print('built',len(files),'files')
