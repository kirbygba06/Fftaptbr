# -*- coding: utf-8 -*-
"""Descompressor/compressor dos textos longos do FFTA (rotina da ROM em 0x54A0, descoberta via mGBA+GDB).

Formato (a partir do byte seguinte ao cabeçalho de 2 bytes da string, quando o bit 1 do cabeçalho está ligado):
  tamanho descomprimido: 4 bytes big-endian; depois opcodes:
    1xxxxyyy nnnnnnnn   cópia  len=xxxx+3, dist=(yyy<<8|n)+1  (distância contada para trás na saída)
    01nnnnnn ...        literais: nnnnnn+1 bytes
    001nnnnn            zeros:    nnnnn+2 bytes
    0001xxxx aabbbbbb cccccccc   cópia len=(xxxx|(aa<<4))+4, dist=(bbbbbb<<8|c)+1
    00000000 L hh ll    cópia len=L+5, dist=(hh<<8|ll)+1
    00000001 n          0xFF x (n+3)
    00000010 n          0x00 x (n+3)
"""
def decompress(data, off):
    size = int.from_bytes(data[off:off + 4], 'big'); i = off + 4; out = bytearray()
    while len(out) < size:
        b = data[i]; i += 1
        if b & 0x80:
            n = ((b >> 3) & 0xF) + 3; d = ((b & 7) << 8 | data[i]) + 1; i += 1
            for _ in range(n): out.append(out[-d])
        elif b & 0x40:
            n = (b & 0x3F) + 1; out += data[i:i + n]; i += n
        elif b & 0x20:
            out += bytes((b & 0x1F) + 2)
        elif b & 0x10:
            c = data[i]; i += 1
            n = ((b & 0xF) | ((c >> 2) & 0x30)) + 4; d = ((c & 0x3F) << 8 | data[i]) + 1; i += 1
            for _ in range(n): out.append(out[-d])
        elif b == 0:
            n = data[i] + 5; d = (data[i + 1] << 8 | data[i + 2]) + 1; i += 3
            for _ in range(n): out.append(out[-d])
        elif b == 1:
            out += b'\xff' * (data[i] + 3); i += 1
        elif b == 2:
            out += bytes(data[i] + 3); i += 1
    return bytes(out[:size]), i


def compress(raw):
    """compressor simples (literais + cópias curtas gulosas); o jogo aceita qualquer fluxo válido"""
    out = bytearray(len(raw).to_bytes(4, 'big')); i = 0; lit = bytearray()
    def flush():
        while lit:
            chunk = lit[:64]; del lit[:64]
            out.append(0x40 | (len(chunk) - 1)); out.extend(chunk)
    while i < len(raw):
        best_n = best_d = 0
        for d in range(1, min(i, 0x7FF) + 1):
            n = 0
            while i + n < len(raw) and n < 18 and raw[i + n - d] == raw[i + n] if i + n - d >= 0 else False: n += 1
            if n > best_n: best_n, best_d = n, d
        if best_n >= 3:
            flush(); dd = best_d - 1
            out.append(0x80 | ((best_n - 3) << 3) | (dd >> 8)); out.append(dd & 0xFF); i += best_n
        else:
            lit.append(raw[i]); i += 1
    flush()
    return bytes(out)
