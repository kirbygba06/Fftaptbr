# -*- coding: utf-8 -*-
"""Leitura de bancos de texto (tabela de offsets u16 + strings) incluindo strings comprimidas (ffta_lz)."""
import struct, re
from ffta_lz import decompress

P1 = {0x21, 0x3C, 0x3E, 0x67, 0x6C, 0x72, 0x74, 0x25}   # controles 40 xx com 1 byte de parâmetro
P2 = {0x66}                                                # 2 parâmetros
END_TOK = {(0x40, 0x61), (0x40, 0x63), (0x40, 0x77)}


def parse_table(rom, a, maxfirst=0x4000):
    first = struct.unpack_from('<H', rom, a)[0]
    if first < 4 or first > maxfirst or first % 2: return None
    n = first // 2
    offs = list(struct.unpack_from('<%dH' % n, rom, a))
    if offs[-1] != 0xFFFF: return None
    o = offs[:-1]
    if any(x > y for x, y in zip(o, o[1:])): return None
    return o


def scan_banks(rom, lo, hi, maxfirst=0x4000):
    res, a = [], lo
    while a < hi:
        o = parse_table(rom, a, maxfirst)
        if o and len(o) >= 2:
            res.append((a, o)); a += o[0]; continue
        a += 2
    return res


def string_at(rom, base, off):
    """-> (hdr u16, plain_bytes, compressed: bool, raw_len) ; plain_bytes = corpo em 80/40 sem cabeçalho"""
    p = base + off
    hdr = struct.unpack_from('<H', rom, p)[0]
    if hdr & 2:
        out, used = decompress(rom, p + 2)
        return hdr, out, True, 2 + used
    # plano: vai até o fim marcado (40 61/40 63 + 00) – fim real é dado pelo próximo offset
    return hdr, None, False, None


def tokens(plain):
    """lista de (kind, data): ('g',glyph) ('c',code,params) ('x',b0,b1) ('z',) """
    t, i = [], 0
    while i < len(plain):
        b = plain[i]
        if b == 0x80 and i + 1 < len(plain): t.append(('g', plain[i + 1])); i += 2
        elif b == 0x40 and i + 1 < len(plain):
            c = plain[i + 1]; n = 1 if c in P1 else 2 if c in P2 else 0
            t.append(('c', c, bytes(plain[i + 2:i + 2 + n]))); i += 2 + n
        elif b == 0x00: t.append(('z',)); i += 1
        elif i + 1 < len(plain): t.append(('x', b, plain[i + 1])); i += 2
        else: t.append(('z',)); i += 1
    return t
