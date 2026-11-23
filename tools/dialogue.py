# -*- coding: utf-8 -*-
"""Reinsere strings traduzidas nos bancos de diálogo do inglês.

Banco = tabela de offsets u16 (relativos ao início do banco, termina em FFFF) + strings
[cabeçalho 2 bytes][texto: pares 80 xx | controles 40 xx | 81 xx][sufixo de controles + 00].
Como strings comprimidas podem apontar para dentro do banco, o banco original é copiado
INTEIRO para o espaço livre e as traduções são ANEXADAS no fim; só a tabela de offsets e os
ponteiros do código (palavras de 32 bits com o endereço do banco) são alterados."""
import struct
import banks
from dialogue_translations import DIALOGUE

FREE = 0xF00000
OK_CTRL = {0x73, 0x6E, 0x70, 0x63, 0x61, 0x77}


def enc_dlg(text, code01):
    out = bytearray()
    for c in text:
        if c == '\n': out += b'\x40\x6e'
        elif c == ' ': out += b'\x40\x73'
        elif c == '-': out += b'\x80\xfe'
        elif c == '&': out += b'\x81\x08'
        else: out += bytes([0x80, code01(c) - 1])
    return bytes(out)


def split_tokens(b):
    toks, i = [], 0
    while i < len(b):
        if b[i] in (0x80, 0x40, 0x81) and i + 1 < len(b):
            toks.append((b[i], b[i + 1], i)); i += 2
        else:
            toks.append((b[i], None, i)); i += 1
    return toks


def line_px(rom, code01, line):
    return sum(4 if c == ' ' else 7 if c == '&' else rom[0x4F885B + (0xFF if c == '-' else code01(c))] for c in line)


def build(rom, code01):
    banks.rom = bytes(rom)
    starts = sorted({a for a, _, _ in banks.scan(0x4F9000, 0x54F000)})
    recs, cursor, report = {}, FREE, []
    for bank, trans in DIALOGUE.items():
        o = banks.parse_bank(bank)
        nxt = next(s for s in starts if s > bank)
        data = bytearray(rom[bank:nxt])
        ends = o[1:] + [len(data)]
        # largura máxima de linha nos textos ingleses simples do banco (caixa de ajuda)
        cap = 0
        for s_, e_ in zip(o, ends):
            for line in bytes(rom[bank + s_ + 2:bank + e_]).split(b'\x40\x6e'):
                px, k = 0, 0
                while k + 1 < len(line):
                    if line[k] == 0x80: px += rom[0x4F885B + line[k + 1] + 1]; k += 2
                    elif line[k] in (0x40, 0x81): px += 4 if line[k:k + 2] == b'\x40\x73' else 0; k += 2
                    else: break
                cap = max(cap, px) if px < 400 else cap
        for idx, text in sorted(trans.items()):
            s, e = o[idx], ends[idx]
            orig = bytes(rom[bank + s:bank + e])
            hdr, body = orig[:2], orig[2:]
            toks = split_tokens(body)
            for t in toks:
                assert t[0] not in (0x40, 0x81) or t[1] in OK_CTRL or (t[0] == 0x81 and t[1] == 8), \
                    'controle não suportado em %X[%d]: %02x %02x' % (bank, idx, t[0], t[1] or 0)
            last = max(k for k, t in enumerate(toks) if t[0] == 0x80)
            suffix = body[toks[last][2] + 2:]
            new = hdr + enc_dlg(text, code01) + suffix
            if len(data) % 2: data += b'\0'
            off = len(data)
            assert off < 0xFFFF
            data += new
            struct.pack_into('<H', data, 2 * idx, off)
            for ln in text.split('\n'):
                if line_px(rom, code01, ln) > cap:
                    report.append('%X[%d]: linha %dpx > %dpx: %s' % (bank, idx, line_px(rom, code01, ln), cap, ln))
            nl_o = body.count(b'\x40\x6e') + 1; nl_n = text.count('\n') + 1
            if nl_n > nl_o: report.append('%X[%d]: %d linhas > %d originais' % (bank, idx, nl_n, nl_o))
        # ponteiros de código para o banco
        old = struct.pack('<I', 0x08000000 + bank)
        refs, p = [], rom.find(old)
        while p >= 0:
            if p % 4 == 0: refs.append(p)
            p = rom.find(old, p + 1)
        assert refs, 'nenhum ponteiro para o banco %X' % bank
        cursor = (cursor + 3) & ~3
        for r in refs: recs[r] = struct.pack('<I', 0x08000000 + cursor)
        recs[cursor] = bytes(data)
        cursor += len(data)
    return recs, report
