# -*- coding: utf-8 -*-
"""Tabelas da ROM AFXP (Data Crystal + conferência com os guias): classes, itens, habilidades."""
from romlib import *
JOB_BASE = 0x6E5498      # 115 registros de 0x34 bytes (id 0 = vazio)
ITEM_BASE = 0x6E0BD0     # registros de 0x20 bytes, índice 0.. (índice+1 = linha 'i' da tabela antiga)
ABIL_BASE = 0x710E04     # registros de 0x1C bytes; índice = ID da habilidade (0 = vazio)
ELEM = ['-', 'Fogo', 'Vento', 'Terra', 'Água', 'Gelo', 'Raio', 'Sagrado', 'Trevas']
def s8(x): return x - 256 if x > 127 else x
def jobs():
    out = []
    for i in range(1, 115):
        a = JOB_BASE + 0x34 * i; r = rom[a:a + 0x34]
        el = u32(a + 0x12); names = ['Fogo', 'Vento', 'Terra', 'Água', 'Gelo', 'Raio', 'Sagrado', 'Trevas']
        res = {n: (el >> (3 + 3 * k)) & 7 for k, n in enumerate(names)}
        out.append(dict(id=i, name=NAMES(u16(a)), race=r[4], hp=r[0x17], mp=r[0x18], spd=r[0x19],
                        atk=((r[0x1B] & 0xF) << 8) | r[0x1A], dfn=((r[0x1C] & 0xF) << 4) | (r[0x1B] >> 4),
                        pow=((r[0x1E] & 0xF) << 8) | r[0x1D], res=((r[0x1F] & 0xF) << 4) | (r[0x1E] >> 4),
                        g_hp=r[0x20] / 10, g_mp=r[0x21] / 10, g_spd=r[0x22] / 10, g_atk=r[0x23] / 10, g_def=r[0x24] / 10,
                        g_pow=r[0x25] / 10, g_res=r[0x26] / 10, mov=r[0x28], jmp=r[0x29], eva=r[0x2A], sres=r[0x16],
                        equip=u32(0x51D0F4 + 4 * r[0x2D]) if False else r[0x2D], elem=res, raw=r.hex(' ')))
    return out
def items():
    out = []
    for i in range(0, 376):
        a = ITEM_BASE + 0x20 * i; r = rom[a:a + 0x20]
        if a + 0x20 > len(rom): break
        out.append(dict(idx=i, name=NAMES(u16(a)), buy=u16(a + 4), sell=u16(a + 6), type=r[8], elem=r[9], rng=s8(r[10]), worn=r[11],
                        atk=r[0x10], dfn=r[0x11], pow=r[0x12], res=r[0x13], spd=s8(r[0x14]), eva=s8(r[0x15]), mov=s8(r[0x16]), jmp=s8(r[0x17]),
                        fx=list(r[0x1A:0x1D]), abil=r[0x1D], raw=r.hex(' ')))
    return out
def abilities():
    out = []
    for i in range(0, 0x1C5):
        a = ABIL_BASE + 0x1C * i; r = rom[a:a + 0x1C]
        n = u16(a)
        out.append(dict(idx=i, nid=n, name=MENU(n - 1) if n else '-', elem=r[2], ap=r[3] * 10, mp=r[4], weap=r[5], rng=r[6], vrng=r[7], tgt=r[8],
                        area=r[9], varea=r[10], power=r[11], fx=list(r[12:16]), flags=u32(a + 0x10), desc=u16(a + 0x16), raw=r.hex(' ')))
    return out
if __name__ == '__main__':
    J = jobs()
    for j in J[:5]: print({k: v for k, v in j.items() if k not in ('raw', 'elem')})
    A = abilities()
    for x in A[:0x20]: print(hex(x['idx']), x['name'], ELEM[x['elem']] if x['elem'] < 9 else x['elem'], x['mp'], x['power'], x['ap'])
