# -*- coding: utf-8 -*-
"""Gera patches IPS modulares e reversíveis (um byte por registro): custo de MP de habilidades. Aplicar sobre a ROM original ou sobre a traduzida (não há sobreposição)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import ips
from romdata import *
A = {x['name']: x for x in abilities() if x['name'] != '-'}
def mp_offset(name): return ABIL_BASE + 0x1C * A[name]['idx'] + 4
def write_ips(path, edits):
    out = bytearray(b'PATCH')
    for off, val in sorted(edits.items()):
        assert off != 0x454F46 and off < 0x1000000
        out += off.to_bytes(3, 'big') + (1).to_bytes(2, 'big') + bytes([val])
    out += b'EOF'; open(path, 'wb').write(out)
MODS = {
 'bal01_tiros_de_status_mp6': {n: 6 for n in ('Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot')},
 'bal01b_tiros_de_status_mp10': {n: 10 for n in ('Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot')},
 'bal02_cupid_mp8': {'Cupid': 8},
}
here = os.path.dirname(__file__)
for nm, m in MODS.items():
    edits = {mp_offset(n): v for n, v in m.items()}
    p = os.path.join(here, 'patches', nm + '.ips'); write_ips(p, edits)
    # verificação: aplica sobre a ROM original e relê pelo leitor de dados
    pat = bytearray(rom)
    for o, d in ips.parse(p): pat[o:o + len(d)] = d
    for n, v in m.items(): assert pat[mp_offset(n)] == v and rom[mp_offset(n)] == 0 or n == 'Fire Veil', (n, pat[mp_offset(n)])
    print(nm, {n: (rom[mp_offset(n)], v, hex(mp_offset(n))) for n, v in m.items()})
