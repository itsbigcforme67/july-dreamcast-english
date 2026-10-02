"""Extract the ISO9660 filesystem of track03.bin into work/fs."""
import struct,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import R,W
T=open(W+'/track03.bin','rb'); BASE=45000
def sec(lba,n=1):
    out=b''
    for i in range(n):
        T.seek((lba+i-BASE)*2352+16); out+=T.read(2048)
    return out
pvd=sec(BASE+16); assert pvd[1:6]==b'CD001',pvd[:8]
root=pvd[156:156+34]
files=[]
def walk(rec,path):
    lba,size=struct.unpack('<I',rec[2:6])[0],struct.unpack('<I',rec[10:14])[0]
    data=sec(lba,(size+2047)//2048); p=0
    while p<size:
        l=data[p]
        if l==0: p=(p//2048+1)*2048; continue
        r=data[p:p+l]; nl=r[32]; name=r[33:33+nl]
        if name not in (b'\0',b'\1'):
            nm=name.decode('ascii').split(';')[0]; fl=r[25]
            flba,fsz=struct.unpack('<I',r[2:6])[0],struct.unpack('<I',r[10:14])[0]
            if fl&2: walk(r,path+'/'+nm)
            else: files.append((path+'/'+nm,flba,fsz))
        p+=l
walk(root,'')
out=W+'/fs'
for f,l,s in files:
    d=out+f; os.makedirs(os.path.dirname(d),exist_ok=True)
    with open(d,'wb') as o:
        rem=s; lb=l
        while rem>0:
            n=min(rem,2048*512); o.write(sec(lb,(n+2047)//2048)[:n]); rem-=n; lb+=(n+2047)//2048
    print(l,s,f)
