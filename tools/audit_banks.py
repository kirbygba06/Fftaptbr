# -*- coding: utf-8 -*-
"""Lista entradas dos bancos do slot inglês que continuam iguais ao original (provavelmente sem tradução)."""
import sys, struct, re, os
sys.path.insert(0, os.path.dirname(__file__))
import build_patch as b, ips
from textbanks import scan_banks, to_markup
from dialogue import get_string
from ffta_lz import decompress
rom = open(sys.argv[1], 'rb').read()
pat = bytearray(rom)
for o, d in ips.parse(os.path.join(os.path.dirname(__file__), '..', 'patches', 'FFTA_ptBR_slot_ingles.ips')): pat[o:o + len(d)] = d
pat = bytes(pat)
def raw_table(r, a):
    offs = []
    while True:
        v = struct.unpack_from('<H', r, a + 2 * len(offs))[0]
        if v == 0xFFFF: break
        offs.append(v)
        if len(offs) > 2000: return None
    return offs
def text_at(r, a, off):
    p = a + off
    h = struct.unpack_from('<H', r, p)[0]
    if h & 2: body, _ = decompress(r, p + 2)
    else:
        e = p + 2
        while e + 1 < len(r) and not (r[e] == 0 and r[e + 1] == 0 and (e - p) > 2): e += 1
        body = bytes(r[p + 2:e])
    return to_markup(body, b.code01)[0]
tot = 0
lo, hi = int(sys.argv[2], 16), int(sys.argv[3], 16)
for A, o in scan_banks(rom, lo, hi):
    old = struct.pack('<I', 0x08000000 + A); p = rom.find(old); refs = []
    while p >= 0:
        if p % 4 == 0: refs.append(p)
        p = rom.find(old, p + 1)
    newA = struct.unpack_from('<I', pat, refs[0])[0] - 0x08000000 if refs else A
    no = raw_table(pat, newA)
    if not no or len(no) != len(o): print('? banco', hex(A), hex(newA)); continue
    un = []
    for i in range(len(o)):
        try: t1 = text_at(rom, A, o[i]); t2 = text_at(pat, newA, no[i])
        except Exception: continue
        tt = re.sub(r'\{[^}]*\}', '', t1)
        if t1 == t2 and re.search('[A-Za-z]{2,}', tt) and 'dummy' not in tt.lower(): un.append((i, t1[:70].replace('\n', '/')))
    un = [u for u in un if not u[1].startswith('{8a ff}') and not u[1].startswith('{11 00}')]
    if un: tot += len(un); print(hex(A), '->', hex(newA), len(o), len(un), un[:8] if len(sys.argv) < 5 else [u[0] for u in un])
print('total', tot)
