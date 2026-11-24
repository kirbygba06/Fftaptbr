# -*- coding: utf-8 -*-
"""Exporta um banco de texto simples (região 1): python3 tools/dump_bank.py ROM.gba 0xENDERECO"""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import build_patch as b, banks
from textbanks import to_markup
from dialogue import get_string
rom = open(sys.argv[1], 'rb').read(); banks.rom = rom
A = int(sys.argv[2], 16)
o = banks.parse_bank(A)
ends = o[1:] + [o[-1] + 400]
for i in range(len(o)):
    try:
        h, body, c = get_string(rom, A, o, ends, i); t, _ = to_markup(body, b.code01)
    except Exception as e: continue
    if re.search('[A-Za-z]{3}', re.sub(r'\{[^}]*\}', '', t)): print('%d: %s' % (i, t.replace('\n', '/').replace('\f', ' ¶ ')))
