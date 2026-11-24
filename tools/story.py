# -*- coding: utf-8 -*-
"""Bancos de história (diálogos de cena). Descoberto com mGBA+GDB:
  base do grupo inglês P = 0x08BB064C; tabela de u32 em P: [0]=fim, [k+1] = offset (relativo a P) do banco k.
Para traduzir: copia o banco para espaço livre, anexa as strings traduzidas (sem compressão, cabeçalho & ~2) e troca o
offset da tabela (nada mais referencia o banco)."""
import re, struct
from textbanks import parse_table, to_markup, from_markup
from dialogue import get_string, line_px

P_EN = 0xBB064C
FREE_STORY = 0xF58000


def markup_px(rom, code01, line):
    line = re.sub(r'\{[^}]*\}', 'MMMMMM', line)    # variáveis (nomes): ~6 letras largas
    return line_px(rom, code01, line)


def trim_last(body):
    """A última entrada de um banco pode ser seguida por dados alheios; corta no primeiro 40 63 00 00."""
    i = bytes(body).find(b'\x40\x63\x00\x00')
    return body[:i + 4] if 0 <= i < len(body) - 4 and len(body) > 400 else body


def build(rom, code01, translations, base=FREE_STORY):
    recs, cursor, report, done = {}, base, [], {}
    u32 = lambda a: struct.unpack_from('<I', rom, a)[0]
    for k, tr in sorted(translations.items()):
        ent = P_EN + 4 * (k + 1)
        A = P_EN + u32(ent)
        if A in done:    # banco-alias (mesmo endereço de outro já traduzido)
            recs[ent] = struct.pack('<I', done[A] - P_EN); continue
        nxt = P_EN + u32(ent + 4) if u32(ent + 4) > u32(ent) else P_EN + u32(P_EN)
        o = parse_table(rom, A)
        if nxt - A > 0x6000: nxt = min(nxt, A + max(o) + 0x800)   # não copiar o lixo/vizinhos até o próximo banco
        ends = o[1:] + [nxt - A]
        data = bytearray(rom[A:nxt])
        # cap de largura: maior linha inglesa do banco
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
            for page in re.split('\f|\\{40 61\\}\\{40 63\\}', text):
                if page.count('\n') + 1 > maxlines:
                    report.append('B%d[%d]: %d linhas > %d: %s' % (k, idx, page.count('\n') + 1, maxlines, page.split('\n')[0]))
            for ln in re.split('[\n\f]|\\{40 61\\}\\{40 63\\}', text):
                w = markup_px(rom, code01, ln)
                if w > cap: report.append('B%d[%d]: linha %dpx > %dpx: %s' % (k, idx, w, cap, ln))
            if len(data) % 2: data += b'\0'
            off = len(data); assert off < 0xFFFF
            data += struct.pack('<H', new_hdr) + from_markup(text, code01, suffix)
            struct.pack_into('<H', data, 2 * idx, off)
        cursor = (cursor + 3) & ~3
        if cursor < 0xFE0000 <= cursor + len(data): cursor = 0xFEB000    # pula o trecho do texto/menu; usa o fim da ROM
        recs[ent] = struct.pack('<I', cursor - P_EN)
        done[A] = cursor
        recs[cursor] = bytes(data)
        cursor += len(data)
    return recs, report
