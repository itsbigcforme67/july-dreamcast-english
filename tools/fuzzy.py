import json,glob,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import R,W
def norm(s):
    s=re.sub(r'%[A-Z]\d*','',s)
    return re.sub(r'[\s\t/、。，．・…！？!?「」『』＜＞　]','',s)
tm={}
for f in glob.glob(R+'/text/jp/*.json'):
    n=os.path.basename(f)[:-5]; ep=R+'/text/en/'+n+'.json'
    if not os.path.exists(ep): continue
    en=json.load(open(ep))
    for e in json.load(open(f)):
        if e['id'] in en: tm.setdefault(norm(e['jp']),en[e['id']])
cnt=0
for f in glob.glob(R+'/text/jp/*.json'):
    n=os.path.basename(f)[:-5]; ep=R+'/text/en/'+n+'.json'
    en=json.load(open(ep)) if os.path.exists(ep) else {}
    ch=False
    for e in json.load(open(f)):
        if e['id'] in en: continue
        k=norm(e['jp'])
        if k in tm and k:
            en[e['id']]=tm[k]; ch=True; cnt+=1
    if ch: json.dump(en,open(ep,'w'),ensure_ascii=False,indent=0)
print('fuzzy filled',cnt)
