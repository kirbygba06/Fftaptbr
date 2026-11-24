# -*- coding: utf-8 -*-
"""Exporta a tabela de itens (0x6E0BC0, 32 bytes/registro, 375 itens) da ROM original."""
import sys, csv, os
sys.path.insert(0, os.path.dirname(__file__))
from romlib import *
B = 0x6E0BC0
def items():
    out = []
    for i in range(1, 376):
        r = rom[B + 32 * i:B + 32 * i + 32]
        out.append(dict(id=i, name=NAMES(u16(B + 32 * i + 16)), pw=r[0], res=r[1], b=list(r[2:8]), sub=r[24], cat=r[27],
                        buy=u16(B + 32 * i + 20), sell=u16(B + 32 * i + 22), raw=r.hex(' ')))
    return out
if __name__ == '__main__':
    its = items()
    with open(os.path.join(os.path.dirname(__file__), 'items.csv'), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['id', 'nome', 'pw', 'res', 'b2-7', 'sub', 'cat', 'compra', 'venda'])
        for t in its: w.writerow([t['id'], t['name'], t['pw'], t['res'], ' '.join(map(str, t['b'])), t['sub'], t['cat'], t['buy'], t['sell']])
    print(len(its))
