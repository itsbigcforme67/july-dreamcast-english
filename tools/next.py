import sys,os,json,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import R,W
budget=int(sys.argv[1]) if len(sys.argv)>1 else 4000
order=open(R+'/text/order.txt').read().split()
import show
M=show.tm()
picked=[];tot=0
for n in order:
    es=json.load(open(R+f'/text/jp/{n}.json'))
    p=R+f'/text/en/{n}.json'; en=json.load(open(p)) if os.path.exists(p) else {}
    todo=[e for e in es if e['id'] not in en and e['jp'] not in M]
    auto=[e for e in es if e['id'] not in en and e['jp'] in M]
    if not todo and not auto: continue
    picked.append(n); tot+=sum(len(show.clean(e['jp'])) for e in todo)
    if tot>=budget: break
os.execvp('python3',['python3',R+'/tools/show.py']+picked)
