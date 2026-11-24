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


# ---------- marcação legível <-> bytes 80/40 ----------
import re as _re
_ACC = "àáâãéêíóôõúç"
_PUN = ".,!?:/'()+[]\"-0123456789"


def _glyph_tables(code01):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + _ACC + _PUN + "ÀÁÂÊÉÍÓÚ"
    enc, dec = {}, {}
    for ch in chars:
        try: g = code01('-' if False else ch) - 1
        except ValueError: continue
        enc[ch] = g
    enc['-'] = 0xFE            # hífen no formato 80
    for ch, g in enc.items(): dec.setdefault(g, ch)
    return enc, dec


def to_markup(plain, code01):
    """bytes 80/40 -> texto; '\\n' quebra, '\\f' página, '{..}' bytes crus; devolve (texto, sufixo_bytes)"""
    enc, dec = _glyph_tables(code01)
    toks = []
    i = 0
    while i < len(plain):
        b = plain[i]
        if b == 0x80 and i + 1 < len(plain): toks.append(bytes(plain[i:i + 2])); i += 2
        elif b == 0x40 and i + 1 < len(plain):
            c = plain[i + 1]; n = 1 if c in P1 else 2 if c in P2 else 0
            toks.append(bytes(plain[i:i + 2 + n])); i += 2 + n
        elif b == 0x00: toks.append(b'\x00'); i += 1
        else: toks.append(bytes(plain[i:i + 2])); i += 2
    # sufixo = fim de tokens de controle (40 61 / 40 63 / 40 77 / 00)
    k = len(toks)
    while k > 0 and (toks[k - 1] == b'\x00' or toks[k - 1][:2] in (b'\x40\x61', b'\x40\x63', b'\x40\x77')): k -= 1
    # preserva 40 70 40 63 (página) que ficou dentro do texto: só vale o sufixo final
    suffix = b''.join(toks[k:]); out = []
    j = 0
    body = toks[:k]
    while j < len(body):
        t = body[j]
        if t[0] == 0x80 and len(t) == 2 and t[1] in dec: out.append(dec[t[1]])
        elif t == b'\x40\x73': out.append(' ')
        elif t == b'\x40\x6e': out.append('\n')
        elif t == b'\x40\x70' and j + 1 < len(body) and body[j + 1] == b'\x40\x63': out.append('\f'); j += 1
        elif t == b'\x81\x08': out.append('&')
        else: out.append('{' + t.hex(' ') + '}')
        j += 1
    return ''.join(out), suffix


def from_markup(text, code01, suffix):
    enc, _ = _glyph_tables(code01)
    out = bytearray(); i = 0
    while i < len(text):
        c = text[i]
        if c == '{':
            j = text.index('}', i); out += bytes.fromhex(text[i + 1:j].replace(' ', '')); i = j + 1; continue
        if c == '\n': out += b'\x40\x6e'
        elif c == '\f': out += b'\x40\x70\x40\x63'
        elif c == ' ': out += b'\x40\x73'
        elif c == '&': out += b'\x81\x08'
        else: out += bytes([0x80, enc[c]])
        i += 1
    return bytes(out) + suffix
