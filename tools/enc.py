"""English -> game bytes via digraph glyphs."""
import re,textwrap
# game glyph order -> SJIS codes
def glyph_codes():
    out=[]
    def add(ku,tens):
        for ten in tens:
            b=bytes([ku+0xa0,ten+0xa0]).decode('euc_jp').encode('cp932'); out.append(b)
    add(1,range(1,95)); add(2,range(1,15))
    add(3,list(range(16,26))+list(range(33,59))+list(range(65,91)))
    add(4,range(1,84)); add(5,range(1,87))
    add(6,list(range(1,25))+list(range(33,57))); add(7,list(range(1,34))+list(range(49,82)))
    for ku in range(16,48): add(ku,range(1,95 if ku<47 else 52))
    while len(out)<3440: out.append(None)   # 22 blank slots, no sjis code
    return out
CODES=glyph_codes()
FIRST_FREE=170          # keep symbols, fullwidth digits/latin (idx<170)
SLOTS=[i for i in range(FIRST_FREE,3418)]
SPACE2=b'\x81\x40'      # fullwidth space = two half spaces

def norm(s):
    s=s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    s=s.replace('—','--').replace('…','...')
    return s
def wrap(s,width):
    lines=[]
    for para in s.split('\n'):
        lines+=textwrap.wrap(para,width,break_long_words=True,break_on_hyphens=True) or ['']
    return lines
def pairs_of(line):
    if len(line)%2: line+=' '
    return [line[i:i+2] for i in range(0,len(line),2)]
class Table:
    def __init__(self): self.map={'  ':0}; self.next=0
    def code(self,p):
        if p not in self.map:
            if self.next>=len(SLOTS): raise Exception('out of glyph slots')
            self.map[p]=SLOTS[self.next]; self.next+=1
        return CODES[self.map[p]]
    def enc_line(self,line):
        return b''.join(self.code(p) for p in pairs_of(norm(line)))
