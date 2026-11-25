# -*- coding: utf-8 -*-
"""Falas de missão (início/fim de batalha). Tabela P (0x08BB064C), entrada do banco 60 = sub-tabela de 26 offsets
(u32, relativos a P) em P+0x30018; cada um aponta um banco de 240 strings (o último tem 120).
Mesma técnica da história: copia o banco, anexa as strings traduzidas (sem compressão) e troca só o offset da sub-tabela."""
import re, struct
from textbanks import parse_table, to_markup, from_markup
from dialogue import get_string
from story import P_EN, trim_last, markup_px

SUB = P_EN + 0x30018
NSUB = 26


def bank_bounds(rom, j):
    u32 = lambda a: struct.unpack_from('<I', rom, a)[0]
    A = P_EN + u32(SUB + 4 * j)
    o = parse_table(rom, A)
    nxt = P_EN + u32(SUB + 4 * (j + 1)) if j + 1 < NSUB else A + max(o) + 0x800
    if nxt - A > 0x6000 or nxt <= A: nxt = A + max(o) + 0x800
    return A, o, o[1:] + [nxt - A], nxt


def build(rom, code01, translations, base):
    recs, cursor, report = {}, base, []
    for j, tr in sorted(translations.items()):
        A, o, ends, nxt = bank_bounds(rom, j)
        data = bytearray(rom[A:nxt])
        cap = 0
        for i in range(len(o)):
            _, body, comp = get_string(rom, A, o, ends, i); body = trim_last(body)
            txt, _s = to_markup(body, code01)
            for ln in re.split('[\n\f]', txt): cap = max(cap, markup_px(rom, code01, ln)) if len(ln) < 60 else cap
        for idx, text in sorted(tr.items()):
            hdr_i, body, comp = get_string(rom, A, o, ends, idx); body = trim_last(body)
            _, suffix = to_markup(body, code01)
            new_hdr = hdr_i & ~2 if comp else hdr_i
            maxlines = max(1, (new_hdr >> 4) & 0xF)
            for page in re.split('\f', text):
                if page.count('\n') + 1 > maxlines:
                    report.append('M%d[%d]: %d linhas > %d: %s' % (j, idx, page.count('\n') + 1, maxlines, page.replace('\n', '/')))
            for ln in re.split('[\n\f]', text):
                w = markup_px(rom, code01, ln)
                if w > cap: report.append('M%d[%d]: linha %dpx > %dpx: %s' % (j, idx, w, cap, ln))
            if len(data) % 2: data += b'\0'
            off = len(data); assert off < 0xFFFF, (j, off)
            data += struct.pack('<H', new_hdr) + from_markup(text, code01, suffix)
            struct.pack_into('<H', data, 2 * idx, off)
        cursor = (cursor + 3) & ~3
        if cursor < 0xFE0000 <= cursor + len(data): cursor = 0xFEB000
        recs[SUB + 4 * j] = struct.pack('<I', cursor - P_EN)
        recs[cursor] = bytes(data)
        cursor += len(data)
    return recs, report
