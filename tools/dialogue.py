# -*- coding: utf-8 -*-
"""Reinsere strings traduzidas nos bancos de diálogo do inglês.

Banco = tabela de offsets u16 (relativos ao início do banco, termina em FFFF) + strings
[cabeçalho 2 bytes][texto: pares 80 xx | controles 40 xx | 81 xx][sufixo de controles + 00].
Como strings comprimidas podem apontar para dentro do banco, o banco original é copiado
INTEIRO para o espaço livre e as traduções são ANEXADAS no fim; só a tabela de offsets e os
ponteiros do código (palavras de 32 bits com o endereço do banco) são alterados."""
import struct
import banks
from ffta_lz import decompress
from dialogue_translations import DIALOGUE

FREE = 0xF00000
OK_CTRL = {0x73, 0x6E, 0x70, 0x63, 0x61, 0x77}


def enc_dlg(text, code01):
    out = bytearray()
    for c in text:
        if c == '\n': out += b'\x40\x6e'
        elif c == '\f': out += b'\x40\x70\x40\x63'
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


def get_string(rom, bank, o, ends, idx):
    """(cabeçalho u16, corpo plano 80/40, comprimida?) – descomprime se o bit 1 do cabeçalho estiver ligado"""
    p = bank + o[idx]
    hdr = struct.unpack_from('<H', rom, p)[0]
    if hdr & 2:
        out, _ = decompress(rom, p + 2)
        return hdr, out, True
    return hdr, bytes(rom[p + 2:bank + ends[idx]]), False


def decode_text(body, code01):
    """bytes de corpo (sem cabeçalho) -> texto ASCII/Unicode, ou None se houver token desconhecido"""
    inv = {}
    for ch in ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?:/'()+"
               "àáâãéêíóôõúç[]\""):
        inv[code01(ch) - 1] = ch
    toks = split_tokens(body)
    lastc = max((k for k, t in enumerate(toks) if t[0] == 0x80), default=-1)
    toks = toks[:lastc + 1]
    out, k = '', 0
    while k < len(toks):
        t, p, _ = toks[k]; k += 1
        if t == 0x40 and p == 0x6E: out += '\n'; continue
        if t == 0x40 and p == 0x70:
            if k < len(toks) and toks[k][:2] == (0x40, 0x63): out += '\f'; k += 1; continue
            return None
        if t == 0x80:
            if p == 0xFE: out += '-'
            elif p in inv: out += inv[p]
            else: return None
        elif t == 0x40 and p == 0x73: out += ' '
        elif t == 0x81 and p == 8: out += '&'
        else: return None
    return out


def reflow(raw, code01, rom, cap=156):
    """'Título\nparágrafo\fparágrafo' -> texto com quebras de linha e de página"""
    title, body = raw.split('\n', 1)
    maxlines = 7
    pages_in, out_pages, lines = body.split('\f'), [], ['[' + title + ']']
    def wrap(par):
        res, cur = [], ''
        for w in par.split(' '):
            t = (cur + ' ' + w) if cur else w
            if line_px(rom, code01, t) <= cap: cur = t
            else: res.append(cur); cur = w
        res.append(cur)
        return res
    for par in pages_in:
        for ln in wrap(par):
            if len(lines) >= maxlines: out_pages.append('\n'.join(lines)); lines = []
            lines.append(ln)
        out_pages.append('\n'.join(lines)); lines = []
    return '\f'.join(out_pages)


def auto_effects(rom, code01, bank=0x521A20, ruler=None, table=None):
    from dialogue_effects import EFFECTS
    o = banks.parse_bank(bank); ends = o[1:] + [len(rom[bank:bank + o[-1] + 0x80])]
    res = {}
    for idx, (s, e) in enumerate(zip(o, ends)):
        hdr_, body, comp_ = get_string(rom, bank, o, ends, idx)
        txt = decode_text(body, code01)
        if txt is None: continue
        if table is not None:
            if idx not in table: continue
            pt = table[idx]
        elif ruler is not None:
            pt = ruler(txt)
            if pt is None: continue
        elif txt in EFFECTS: pt = EFFECTS[txt]
        elif txt.endswith('!') and txt[:-1] in EFFECTS: pt = EFFECTS[txt[:-1]] + '!'
        else: continue
        if comp_ or enc_dlg(txt, code01) in body: res[idx] = pt
    return res


def _split_lines(raw):
    import re
    return re.split(b'\x40\x6e|\x40\x70\x40\x63', raw)


def build(rom, code01):
    banks.rom = bytes(rom)
    starts = sorted({a for a, _, _ in banks.scan(0x4F9000, 0x54F000)})
    recs, cursor, report = {}, FREE, []
    plan = dict(DIALOGUE)
    plan[0x521A20] = auto_effects(rom, code01)
    from dialogue_desc import DESC, pen
    from dialogue_misc import MISC
    for bk, tb in MISC.items():
        plan[bk] = auto_effects(rom, code01, bk, table=tb)
        assert len(plan[bk]) == len(tb), '%X: %s' % (bk, sorted(set(tb) - set(plan[bk])))
    from dialogue_news import NEWS
    plan[0x513A8C] = auto_effects(rom, code01, 0x513A8C, table={k: reflow(v, code01, rom) for k, v in NEWS.items()})
    assert len(plan[0x513A8C]) == len(NEWS), sorted(set(NEWS) - set(plan[0x513A8C]))
    plan[0x529514] = auto_effects(rom, code01, 0x529514, table=DESC)
    from dialogue_items import item_rule
    _o = banks.parse_bank(0x534D9C); _ends = _o[1:] + [len(rom[0x534D9C:0x534D9C + _o[-1] + 0x80])]
    _tab = {}
    for _i in range(len(_o)):
        _t = decode_text(get_string(rom, 0x534D9C, _o, _ends, _i)[1], code01)
        _pt = item_rule(_i, _t) if _t is not None else None
        if _pt: _tab[_i] = _pt
    plan[0x534D9C] = auto_effects(rom, code01, 0x534D9C, table=_tab)
    plan[0x54382C] = auto_effects(rom, code01, 0x54382C, ruler=pen)
    for bank, trans in plan.items():
        o = banks.parse_bank(bank)
        nxt = next(s for s in starts if s > bank)
        if nxt - bank > 0x6000: nxt = min(nxt, bank + max(o) + 0x600)   # offsets são u16: não copiar vizinhos inteiros
        data = bytearray(rom[bank:nxt])
        ends = o[1:] + [len(data)]
        # largura máxima de linha nos textos ingleses simples do banco (caixa de ajuda)
        cap = 0
        for i_, (s_, e_) in enumerate(zip(o, ends)):
            for line in _split_lines(get_string(rom, bank, o, ends, i_)[1]):
                px, k = 0, 0
                while k + 1 < len(line):
                    if line[k] == 0x80: px += rom[0x4F885B + line[k + 1] + 1]; k += 2
                    elif line[k] in (0x40, 0x81): px += 4 if line[k:k + 2] == b'\x40\x73' else 0; k += 2
                    else: break
                cap = max(cap, px) if px < 400 else cap
        for idx, text in sorted(trans.items()):
            s, e = o[idx], ends[idx]
            hdr_i, body, comp = get_string(rom, bank, o, ends, idx)
            hdr = struct.pack('<H', hdr_i & ~2 if comp else hdr_i)
            toks = split_tokens(body)
            last = max(k for k, t in enumerate(toks) if t[0] == 0x80)
            suffix = body[toks[last][2] + 2:]
            for t in toks[:last + 1]:
                assert t[0] not in (0x40, 0x81) or t[1] in OK_CTRL or (t[0] == 0x81 and t[1] == 8), \
                    'controle não suportado em %X[%d]: %02x %02x' % (bank, idx, t[0], t[1] or 0)

            new = hdr + enc_dlg(text, code01) + suffix
            if len(data) % 2: data += b'\0'
            off = len(data)
            assert off < 0xFFFF
            data += new
            struct.pack_into('<H', data, 2 * idx, off)
            import re as _re
            for ln in _re.split('[\n\f]', text):
                if line_px(rom, code01, ln) > cap:
                    report.append('%X[%d]: linha %dpx > %dpx: %s' % (bank, idx, line_px(rom, code01, ln), cap, ln))
            nl_o = body.count(b'\x40\x6e') + body.count(b'\x40\x70') + 1; nl_n = text.count('\n') + text.count('\f') + 1
            if nl_n > nl_o and bank != 0x513A8C: report.append('%X[%d]: %d linhas > %d originais' % (bank, idx, nl_n, nl_o))
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
