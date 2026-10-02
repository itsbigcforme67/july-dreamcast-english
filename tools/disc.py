import struct,ctypes,os,shutil
import subprocess,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from paths import R,W
_so=os.path.join(W,'libecc.so')
if not os.path.exists(_so):   # small C helper for CD-ROM EDC/ECC, built on first use
    os.makedirs(W,exist_ok=True)
    subprocess.check_call(['cc','-O2','-shared','-fPIC','-o',_so,os.path.join(R,'tools','ecc.c')])
L=ctypes.CDLL(_so)
BASE=45000; RAW=2352
class Disc:
    def __init__(s,src,dst):
        if True:
            shutil.copyfile(src,dst)
        s.f=open(dst,'r+b'); s.src=src
        s.recs={}   # path -> (dir_lba, offset_in_dir, lba, size)
        s.free=50000
        pvd=s.read(BASE+16); root=pvd[156:190]
        s._walk(struct.unpack('<I',root[2:6])[0],struct.unpack('<I',root[10:14])[0],'')
    def read(s,lba,n=1):
        out=b''
        for i in range(n):
            s.f.seek((lba+i-BASE)*RAW+16); out+=s.f.read(2048)
        return out
    def write(s,lba,data):
        data=data+b'\0'*((-len(data))%2048)
        for i in range(len(data)//2048):
            s.f.seek((lba+i-BASE)*RAW); r=bytearray(s.f.read(RAW))
            r[16:2064]=data[i*2048:(i+1)*2048]
            L.fix_mode1((ctypes.c_uint8*RAW).from_buffer(r))
            s.f.seek((lba+i-BASE)*RAW); s.f.write(r)
    def _walk(s,lba,size,path):
        data=s.read(lba,(size+2047)//2048); p=0
        while p<size:
            l=data[p]
            if l==0: p=(p//2048+1)*2048; continue
            r=data[p:p+l]; nm=r[33:33+r[32]]
            if nm not in (b'\0',b'\1'):
                name=path+'/'+nm.decode().split(';')[0]
                flba,fsz=struct.unpack('<I',r[2:6])[0],struct.unpack('<I',r[10:14])[0]
                if r[25]&2: s._walk(flba,fsz,name)
                else: s.recs[name]=(lba,p,flba,fsz)
            p+=l
    def replace(s,path,data):
        dlba,off,flba,fsz=s.recs[path]
        if (len(data)+2047)//2048 > (fsz+2047)//2048:
            flba=s.free; s.free+=(len(data)+2047)//2048+1
            assert s.free<294700
        s.write(flba,data)
        sec=dlba+off//2048; o=off%2048
        blk=bytearray(s.read(sec))
        blk[o+2:o+6]=struct.pack('<I',flba); blk[o+6:o+10]=struct.pack('>I',flba)
        blk[o+10:o+14]=struct.pack('<I',len(data)); blk[o+14:o+18]=struct.pack('>I',len(data))
        s.write(sec,bytes(blk))
        s.recs[path]=(dlba,off,flba,len(data))
    def close(s): s.f.close()
