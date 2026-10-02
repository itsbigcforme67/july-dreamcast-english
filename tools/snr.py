import struct,os,re
def load(path):
    d=open(path,'rb').read()
    n,hs=struct.unpack('<II',d[:8]); assert hs==8
    recs=[list(struct.unpack('<10i',d[8+i*40:48+i*40])) for i in range(n)]
    base=8+n*40
    def s(p):
        e=d.find(b'\0',p); return d[p:e]
    strs={}
    for r in recs:
        for p in r[8:10]: strs[p]=s(p)
    return d,recs,base,strs
