# -*- coding: utf-8 -*-
"""Lista entradas das tabelas de menu/nomes do slot inglês que ainda apontam para o texto original."""
import sys, glob, struct, os
sys.path.insert(0, os.path.dirname(__file__))
import build_patch as b, ips
rom = open(sys.argv[1], 'rb').read()
pat = bytearray(rom)
for o, d in ips.parse(os.path.join(os.path.dirname(__file__), '..', 'patches', 'FFTA_ptBR_slot_ingles.ips')): pat[o:o + len(d)] = d
u32 = lambda r, a: struct.unpack_from('<I', r, a)[0]
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?:/'()+[]\"-%&*"
inv = {}
for c in chars:
    try: inv[b.code01(c)] = c
    except Exception: pass
def dec(r, p):
    s = bytearray(); e = p
    while r[e] != 0 and e - p < 300: s.append(r[e]); e += 1
    s = bytes(s)
    if not s: return ''
    out = ''
    if s[0] == 1:
        for g in s[1:]: out += inv.get(g, inv.get(g + 1, '{%02x}' % g))
    elif s[0] == 0x80 or s[0] in (0x40, 0x81):
        i = 0
        while i < len(s):
            if s[i] == 0x80 and i + 1 < len(s): out += inv.get(s[i + 1] + 1, '{80 %02x}' % s[i + 1]); i += 2
            elif s[i] == 0x40 and i + 1 < len(s): out += ' ' if s[i + 1] == 0x73 else '{40 %02x}' % s[i + 1]; i += 2
            else: out += '{%02x}' % s[i]; i += 1
    else:
        out = '?' + s.hex()
    return out
table = sys.argv[2]
base = int(table, 16) if table.startswith('0x') else {'menu': b.EN_MENU, 'names': b.EN_NAMES}[table]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
for i in range(n):
    po = u32(rom, base + 4 * i)
    if not (0x08000000 <= po < 0x09000000): continue
    if po == u32(pat, base + 4 * i):
        t = dec(rom, po - 0x08000000)
        if any(ch.isalpha() for ch in t): print(i, repr(t))
