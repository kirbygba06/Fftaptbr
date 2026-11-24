# -*- coding: utf-8 -*-
"""python3 tools/dump_untr.py ROM.gba 0xBANCO i,j,k  -> texto cru (marcação) das entradas dadas, do banco original"""
import sys, os, struct
sys.path.insert(0, os.path.dirname(__file__))
import build_patch as b
from textbanks import to_markup
from dialogue import get_string
import banks
rom = open(sys.argv[1], 'rb').read(); banks.rom = rom
A = int(sys.argv[2], 16); idx = [int(x) for x in sys.argv[3].split(',')]
o = banks.parse_bank(A); ends = o[1:] + [o[-1] + 400]
for i in idx:
    h, body, c = get_string(rom, A, o, ends, i)
    t, sfx = to_markup(body, b.code01)
    print('%d [L%d%s]: %s   ##suf=%s' % (i, (h >> 4) & 15, ' comp' if c else '', t.replace('\n', '\\n').replace('\f', '\\f'), sfx.hex()))
