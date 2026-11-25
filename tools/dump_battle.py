# -*- coding: utf-8 -*-
"""Exporta as falas de missão (grupo 60 da tabela P: sub-tabela de 26 bancos) em marcação:
python3 tools/dump_battle.py ROM.gba [banco] > saida.txt"""
import sys, struct, os
sys.path.insert(0, os.path.dirname(__file__))
import build_patch as b
from textbanks import parse_table, to_markup
from dialogue import get_string
from story import P_EN, trim_last
SUB = P_EN + 0x30018        # tabela P, entrada 61 (banco 60) -> lista de offsets (relativos a P) dos bancos de missão
NSUB = 26
def banks(rom):
    u32 = lambda a: struct.unpack_from('<I', rom, a)[0]
    out = []
    for j in range(NSUB):
        A = P_EN + u32(SUB + 4 * j)
        nxt = P_EN + u32(SUB + 4 * (j + 1)) if j + 1 < NSUB else None
        o = parse_table(rom, A)
        if nxt is None: nxt = A + max(o) + 0x800
        out.append((j, A, o, o[1:] + [nxt - A]))
    return out
if __name__ == '__main__':
    rom = open(sys.argv[1], 'rb').read()
    sel = int(sys.argv[2]) if len(sys.argv) > 2 else None
    n = tot = 0
    for j, A, o, ends in banks(rom):
        if sel is not None and j != sel: continue
        print('### banco', j, hex(A), len(o), 'entradas')
        for i in range(len(o)):
            hdr, body, comp = get_string(rom, A, o, ends, i); body = trim_last(body)
            txt, _ = to_markup(body, b.code01)
            if txt.strip() and 'dummy' not in txt.lower():
                print('%d[%d] L%d %s' % (j, i, (hdr >> 4) & 15, txt.replace('\n', '/').replace('\f', ' ¶ ')))
                n += 1; tot += len(txt)
    print('# strings', n, 'caracteres', tot, file=sys.stderr)
