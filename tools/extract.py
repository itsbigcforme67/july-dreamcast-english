import glob,json,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import snr
from paths import R,W
TEXTOPS={0x5:'say',0xd:'mono',0xf:'hero',0x2b:'narr',0x1a:'ask2',0x1b:'ask3'}
os.makedirs(R+'/text/jp',exist_ok=True)
tot=0
for f in sorted(glob.glob(W+'/fs/SNR/*.BIN')):
    d,recs,base,strs=snr.load(f)
    out=[]; seen={}
    for i,r in enumerate(recs):
        if r[0] not in TEXTOPS: continue
        for slot in (0,1):
            p=r[8+slot]
            if p==base or p in seen: continue
            if r[0] not in (0x1a,0x1b) and slot==1: continue
            t=strs[p].decode('cp932')
            if not re.search(r'[^\t%A-Z\s]',re.sub(r'%[A-Z]','',t)): continue
            seen[p]=1
            out.append({'id':f'{i}.{slot}','op':TEXTOPS[r[0]],'arg':r[1],'jp':t})
    tot+=len(out)
    json.dump(out,open(R+'/text/jp/'+os.path.basename(f)[:-4]+'.json','w'),ensure_ascii=False,indent=0)
print(tot)
