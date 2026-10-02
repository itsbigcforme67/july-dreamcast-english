import json,sys,struct,re,os,glob
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import R,W
d=open(W+'/fs/1ST_READ.BIN','rb').read()
def s(a):
    o=a-0x8c010000; e=d.find(b'\0',o); return d[o:e].decode('cp932','replace')
def table(start,n): return [s(struct.unpack_from('<I',d,start+4*i)[0]) for i in range(n)]
SHORT=table(0xc3aec,175); GEN=table(0xc56a4,30)
def speaker(e,fname):
    if e['op']=='say':
        a=e['arg']
        if a>=1: return SHORT[a-1] if a-1<len(SHORT) else f"#{a}"
        if a<=-2: return GEN[-a-2] if -a-2<len(GEN) else f"#{a}"
        return '?'
    return {'hero':'HERO','mono':'MONO','narr':'NARR','ask2':'Q','ask3':'Q'}[e['op']]
def clean(t):
    t=re.sub(r'%N(\t\t)?','/',t); t=t.replace('\t','')
    t=re.sub(r'%[KEO]|%S\d+','',t); return t.strip('/')
def tm():
    m={}
    for f in glob.glob(R+'/text/en/*.json'):
        en=json.load(open(f)); jp={e['id']:e['jp'] for e in json.load(open(R+'/text/jp/'+os.path.basename(f)))}
        for k,v in en.items():
            if k in jp: m[jp[k]]=v
    return m
if __name__=='__main__':
    M=tm()
    for name in sys.argv[1:]:
        es=json.load(open(R+f'/text/jp/{name}.json'))
        enp=R+f'/text/en/{name}.json'
        en=json.load(open(enp)) if os.path.exists(enp) else {}
        filled=0
        for e in es:
            if e['id'] not in en and e['jp'] in M: en[e['id']]=M[e['jp']]; filled+=1
        if filled: json.dump(en,open(enp,'w'),ensure_ascii=False,indent=0)
        todo=[e for e in es if e['id'] not in en]
        print(f'## {name} ({len(todo)} todo, {filled} autofilled)')
        for e in todo:
            t=e['jp']
            if e['op'] in ('ask2','ask3') and e['id'].endswith('.1'):
                body=t[:-2] if t.endswith('\t\t') else t
                ls=[]
                for seg in body.split('%N'): ls+=seg.split('\t\t')[1:] or ['']
                ls=ls+['']*(len(ls)%2)
                t=' // '.join((ls[i]+' '+ls[i+1]).strip() for i in range(0,len(ls)-1,2))
            else: t=clean(t)
            print(f"{e['id']}|{speaker(e,name)}|{t}")
