import struct
rom=b''
def load(path):
    global rom
    rom=open(path,'rb').read()
    return rom
def parse_bank(a):
    first=struct.unpack_from('<H',rom,a)[0]
    if first<4 or first>0x800 or first%2: return None
    n=first//2
    offs=list(struct.unpack_from('<%dH'%n,rom,a))
    if offs[-1]!=0xffff: return None
    o=offs[:-1]
    if any(x>=y for x,y in zip(o,o[1:])) and False: return None
    if any(x>y for x,y in zip(o,o[1:])): return None
    # text must start with 80 at o[0]+2 for most
    return o
def scan(lo,hi):
    res=[];a=lo
    while a<hi:
        o=parse_bank(a)
        if o and len(o)>=2:
            ok=sum(1 for x in o if rom[a+x+2:a+x+3]==b'\x80' or rom[a+x+2:a+x+3]==b'\x40' or rom[a+x+2:a+x+3]==b'\x00')
            if ok>=len(o)*0.8:
                res.append((a,len(o),o[-1]))
                a+=o[0]; continue
        a+=2
    return res
if __name__=='__main__':
    r=scan(0x4f9000,0x54f000)
    print(len(r),sum(n for _,n,_ in r))
    print([(hex(a),n,hex(l)) for a,n,l in r][:60])
