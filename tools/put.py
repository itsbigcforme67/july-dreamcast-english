"""usage: put.py < file  ; input blocks:  '## NAME' then lines 'id|english' (use \\n for newline, ' // ' between choice options)"""
import json,sys,os,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import R,W
cur=None; data={}
for line in sys.stdin:
    line=line.rstrip('\n')
    if not line.strip(): continue
    m=re.match(r'^## (\S+)',line)
    if m: cur=m.group(1); data.setdefault(cur,{}); continue
    k,_,v=line.partition('|')
    v=v.replace('\\n','\n').strip()
    if k.endswith('.1') and ' // ' in v: v=v.split(' // ')
    data[cur][k.strip()]=v
for name,kv in data.items():
    p=R+f'/text/en/{name}.json'
    en=json.load(open(p)) if os.path.exists(p) else {}
    jp={e['id'] for e in json.load(open(R+f'/text/jp/{name}.json'))}
    bad=[k for k in kv if k not in jp]
    if bad: print('UNKNOWN IDS',name,bad)
    en.update({k:v for k,v in kv.items() if k in jp})
    json.dump(en,open(p,'w'),ensure_ascii=False,indent=0)
    print(name,len(en),'/',len(jp))
