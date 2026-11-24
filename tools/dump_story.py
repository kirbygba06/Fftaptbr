# -*- coding: utf-8 -*-
"""Exporta o texto inglês dos bancos de história para tradução: python3 tools/dump_story.py ROM.gba [banco] > saida.txt"""
import sys, struct, re, os
sys.path.insert(0, os.path.dirname(__file__))
import build_patch as b
from textbanks import parse_table, to_markup
from dialogue import get_string
from story import P_EN
rom = open(sys.argv[1], 'rb').read()
u32 = lambda a: struct.unpack_from('<I', rom, a)[0]
ks = [int(sys.argv[2])] if len(sys.argv) > 2 else range((u32(P_EN + 4) - 4) // 4)
tot = n = 0
for k in ks:
    ent = P_EN + 4 * (k + 1); A = P_EN + u32(ent)
    nxt = P_EN + u32(ent + 4) if u32(ent + 4) > u32(ent) else P_EN + u32(P_EN)
    o = parse_table(rom, A)
    if not o: continue
    ends = o[1:] + [nxt - A]
    print('### banco', k, hex(A), len(o), 'entradas')
    for i in range(len(o)):
        hdr, body, comp = get_string(rom, A, o, ends, i)
        txt, _ = to_markup(body, b.code01)
        if txt.strip() and 'dummy' not in txt:
            print('%d[%d] L%d %s' % (k, i, (hdr >> 4) & 15, txt.replace('\n', '/').replace('\f', ' ¶ ')))
            n += 1; tot += len(txt)
print('# strings', n, 'caracteres', tot, file=sys.stderr)
