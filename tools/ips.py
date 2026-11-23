import sys
def parse(p):
    d=open(p,'rb').read(); assert d[:5]==b'PATCH'; i=5; out=[]
    while d[i:i+3]!=b'EOF':
        off=int.from_bytes(d[i:i+3],'big'); sz=int.from_bytes(d[i+3:i+5],'big'); i+=5
        if sz==0:
            rl=int.from_bytes(d[i:i+2],'big'); out.append((off,bytes([d[i+2]])*rl)); i+=3
        else: out.append((off,d[i:i+sz])); i+=sz
    return out
if __name__=='__main__':
    for off,b in parse(sys.argv[1]): print(hex(off),len(b),b[:48].hex())
