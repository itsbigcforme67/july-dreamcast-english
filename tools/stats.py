import json,glob,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import R,W; tot=done=0
for f in glob.glob(R+'/text/jp/*.json'):
    es=json.load(open(f)); p=R+'/text/en/'+os.path.basename(f); en=json.load(open(p)) if os.path.exists(p) else {}
    tot+=len(es); done+=sum(1 for e in es if e['id'] in en)
print(f'{done}/{tot} strings ({100*done/tot:.1f}%)')
