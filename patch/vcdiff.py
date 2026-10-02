"""Minimal VCDIFF (RFC 3284) encoder/decoder, xdelta3-compatible (no secondary compression)."""
import sys
def vi(n):
    out=[n&0x7f]; n>>=7
    while n: out.append(0x80|(n&0x7f)); n>>=7
    return bytes(reversed(out))
def rvi(b,p):
    n=0
    while True:
        c=b[p]; p+=1; n=(n<<7)|(c&0x7f)
        if not c&0x80: return n,p
WIN=1<<22
def encode(src,dst,out):
    s=open(src,'rb'); t=open(dst,'rb'); o=open(out,'wb')
    o.write(b'\xd6\xc3\xc4\x00\x00')
    pos=0
    while True:
        T=t.read(WIN)
        if not T: break
        s.seek(pos); S=s.read(WIN)
        data=bytearray(); inst=bytearray(); addr=bytearray()
        i=0; n=len(T); m=len(S)
        while i<n:
            # equal run
            j=i
            while j<n and j<m and T[j]==S[j]: j+=1
            if j-i>=8:
                inst+=bytes([19])+vi(j-i); addr+=vi(i); i=j; continue
            # differing run: extend until an equal run of >=8
            k=i
            while k<n:
                if k<m and T[k:k+8]==S[k:k+8] and k+8<=min(n,m): break
                k+=1
            if k==i: k=j  # short equal run, add it
            inst+=bytes([1])+vi(k-i); data+=T[i:k]; i=k
        body=bytes([0])+vi(len(data))+vi(len(inst))+vi(len(addr))+data+inst+addr
        enc=vi(n)+body
        o.write(bytes([1])+vi(len(S))+vi(pos)+vi(len(enc))+enc)
        pos+=n
    o.close()
def decode(src,patch,out):
    s=open(src,'rb'); P=open(patch,'rb').read(); o=open(out,'wb')
    assert P[:4]==b'\xd6\xc3\xc4\x00' and P[4]==0
    p=5
    while p<len(P):
        wi=P[p]; p+=1; assert wi==1
        sl,p=rvi(P,p); sp,p=rvi(P,p); s.seek(sp); S=s.read(sl)
        el,p=rvi(P,p); end=p+el
        tl,p=rvi(P,p); p+=1
        dl,p=rvi(P,p); il,p=rvi(P,p); al,p=rvi(P,p)
        D=P[p:p+dl]; I=P[p+dl:p+dl+il]; A=P[p+dl+il:p+dl+il+al]; p=end
        T=bytearray(); di=ii=ai=0
        while ii<len(I):
            c=I[ii]; ii+=1; sz,ii=rvi(I,ii)
            if c==1: T+=D[di:di+sz]; di+=sz
            elif c==19:
                a,ai=rvi(A,ai); T+=S[a:a+sz]
            else: raise Exception('bad inst')
        assert len(T)==tl; o.write(T)
    o.close()
if __name__=='__main__':
    {'e':encode,'d':decode}[sys.argv[1]](*sys.argv[2:5])
