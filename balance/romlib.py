# -*- coding: utf-8 -*-
"""Leitura da ROM original (AFXP, slot inglês) para análise de balanceamento."""
import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import build_patch as b
ROM_PATH = os.environ.get('FFTA_ROM', '/root/.claude/uploads/6dcaf6bb-9c86-5e3f-87bb-4a1f8b634504/92a5e87c-Final_Fantasy_Tactics_Advance_USA_patched.gba')
rom = open(ROM_PATH, 'rb').read()
u8 = lambda a: rom[a]
u16 = lambda a: struct.unpack_from('<H', rom, a)[0]
s16 = lambda a: struct.unpack_from('<h', rom, a)[0]
u32 = lambda a: struct.unpack_from('<I', rom, a)[0]
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?:/'()+[]\"-%&*"
inv = {}
for c in chars:
    try: inv[b.code01(c)] = c
    except Exception: pass
def dec(p):
    s = bytearray(); e = p
    while rom[e] != 0 and e - p < 300: s.append(rom[e]); e += 1
    s = bytes(s); out = ''
    if not s: return ''
    if s[0] == 1:
        for g in s[1:]: out += inv.get(g, inv.get(g + 1, '?'))
    else:
        i = 0
        while i < len(s):
            if s[i] == 0x80 and i + 1 < len(s): out += inv.get(s[i + 1] + 1, '?'); i += 2
            elif s[i] == 0x40 and i + 1 < len(s): out += ' ' if s[i + 1] == 0x73 else ''; i += 2
            else: i += 1
    return out
def tbl(base, i):
    p = u32(base + 4 * i)
    return dec(p - 0x08000000) if 0x08000000 <= p < 0x09000000 else ''
MENU = lambda i: tbl(b.EN_MENU, i)
NAMES = lambda i: tbl(b.EN_NAMES, i)
