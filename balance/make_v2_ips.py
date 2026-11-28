# -*- coding: utf-8 -*-
"""Gera o Rebalance v2 (somente dados) a partir de v2_design.py:
  final_v2/bal24_habilidades_novas.ips  — 15 habilidades novas em slots reaproveitados + Véus do Ninja
  final_v2/bal25_contrajogo.ips         — imunidades novas em itens de loja
  final_v2/reverter/*                   — reversão de cada módulo
  final_v2/csv/*.csv                    — antes/depois
  tools/v2_text.py                      — nomes e descrições PT das habilidades novas (usados pela tradução com FFTA_V2=1)
  final_v2/FFTA_ptBR_rebalance_v2.ips   — patch único: tradução (com textos v2) + v1 (classes/itens/habilidades/magias) + v2
Uso: python3 make_v2_ips.py ROM_LIMPA.gba"""
import os, sys, csv, json, struct, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.join(HERE, '..', 'tools')
sys.path.insert(0, TOOLS)
import ips
import v2_design as V
from romdata import ABIL_BASE, ITEM_BASE, rom, abilities, items
OUT = os.path.join(HERE, 'final_v2'); os.makedirs(os.path.join(OUT, 'reverter'), exist_ok=True); os.makedirs(os.path.join(OUT, 'csv'), exist_ok=True)
RACE_PTRS = 0x6DF4D4          # tabela de ponteiros (u32) para as listas de habilidades por raça (registros de 8 bytes)
DESC_BANK_OFFSET = 105        # índice no banco de descrições 0x529514 = campo DDDD da lista de raça - 105

def write_ips(path, edits):
    out = bytearray(b'PATCH')
    for off, data in sorted(edits.items()):
        while data:
            chunk, data = data[:0xFFFF], data[0xFFFF:]
            assert off != 0x454F46 and off + len(chunk) <= 0x1000000
            out += off.to_bytes(3, 'big') + len(chunk).to_bytes(2, 'big') + bytes(chunk); off += len(chunk)
    open(path, 'wb').write(out + b'EOF')
def save(name, edits):
    ed = {o: bytes(d) for o, d in edits.items() if bytes(d) != rom[o:o + len(d)]}
    write_ips(os.path.join(OUT, name + '.ips'), ed)
    write_ips(os.path.join(OUT, 'reverter', name + '_reverter.ips'), {o: rom[o:o + len(d)] for o, d in ed.items()})
    return ed
def race_records():
    recs = []
    for r in range(1, 6):
        b = struct.unpack_from('<I', rom, RACE_PTRS + 4 * r)[0] - 0x08000000; e = struct.unpack_from('<I', rom, RACE_PTRS + 4 * (r + 1))[0] - 0x08000000
        for i in range((e - b) // 8): recs.append(struct.unpack_from('<HHHBB', rom, b + 8 * i))
    return recs

def build_data():
    A = {a['idx']: a for a in abilities()}; RR = race_records(); E = V.E_
    e24, rows, names, descs = {}, [], {}, {}
    for s in V.SKILLS:
        slot, t = s['slot'], s['t']; a = ABIL_BASE + 0x1C * slot; ta = ABIL_BASE + 0x1C * t
        old = bytearray(rom[a:a + 0x1C]); new = bytearray(rom[ta:ta + 0x1C])
        new[0:2] = old[0:2]; new[3] = old[3]; new[0x16:0x18] = old[0x16:0x18]      # nome, AP e descrição do slot antigo
        fx = [E[k][1] for k in s['eff']] + [1] * (4 - len(s['eff'])); new[0xC:0x10] = bytes(fx)
        r = s.get('rom', {})
        for k, pos in (('mp', 4), ('rng', 6), ('vrng', 7), ('area', 9), ('varea', 0xA), ('power', 0xB), ('elem', 2)):
            if k in r: new[pos] = r[k]
        if 'anim' in s: new[0x14:0x16] = s['anim'].to_bytes(2, 'little')
        e24[a] = bytes(new)
        rec = [x for x in RR if x[2] == slot and x[3] == 1]
        assert rec, slot
        nidx, didx = rec[0][0], rec[0][1] - DESC_BANK_OFFSET
        names[nidx - 1] = s['pt']; descs[didx] = s['desc']        # nome: NNNN é 1-based na tabela 0x720D44
        rows.append(dict(id=slot, antes=s['old'], depois=s['pt'], classes=s['cls'], efeitos='+'.join(s['eff']), template=A[t]['name'],
                         mp=new[4], poder=new[0xB], alcance='arma' if new[5] else new[6], area=f'{new[9]}/{new[10]}', nome_idx=nidx, desc_idx=didx,
                         raw_antes=old.hex(' '), raw_depois=new.hex(' ')))
    for n, m in V.VEILS.items():
        x = [a for a in A.values() if a['name'] == n][0]; a = ABIL_BASE + 0x1C * x['idx']; new = bytearray(rom[a:a + 0x1C])
        new[4] = m['mp']; new[0xB] = m['power']; e24[a] = bytes(new)
        rows.append(dict(id=x['idx'], antes=n, depois=n, classes='Ninja', efeitos='buff', mp=m['mp'], poder=m['power'], raw_antes=rom[a:a + 0x1C].hex(' '), raw_depois=new.hex(' ')))
    for idx, an in V.ANIM_FIX.items():
        a = ABIL_BASE + 0x1C * idx; e24[a + 0x14] = an.to_bytes(2, 'little')
        rows.append(dict(id=idx, antes=A[idx]['name'], depois=A[idx]['name'], efeitos='animação 0x%02x' % an))
    e24 = save('bal24_habilidades_novas', e24)
    with open(os.path.join(OUT, 'csv', 'bal24_habilidades_novas.csv'), 'w', newline='') as f:
        k = list(rows[0].keys()); w = csv.DictWriter(f, k, extrasaction='ignore'); w.writeheader(); [w.writerow(r_) for r_ in rows]
    I = {t['idx']: t for t in items()}; e25 = {}; rows = []
    for idx, fx in V.ITEMS.items():
        a = ITEM_BASE + 0x20 * idx; e25[a + 0x1A] = bytes(fx)
        rows.append(dict(idx=idx, item=I[idx]['name'], efeitos_antes=rom[a + 0x1A:a + 0x1D].hex(), efeitos_depois=bytes(fx).hex()))
    e25 = save('bal25_contrajogo', e25)
    with open(os.path.join(OUT, 'csv', 'bal25_contrajogo.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); [w.writerow(r_) for r_ in rows]
    # textos para a tradução
    with open(os.path.join(TOOLS, 'v2_text.py'), 'w', encoding='utf-8') as f:
        f.write('# -*- coding: utf-8 -*-\n"""Gerado por balance/make_v2_ips.py: nomes (menu 0x720D44) e descrições (banco 0x529514) das habilidades do Rebalance v2."""\n')
        f.write('NAMES = %r\nDESCS = %r\n' % (names, descs))
    return e24, e25

def combined(clean_rom_path, e24, e25):
    """Tradução (com FFTA_V2=1) + módulos v1 + v2 -> um IPS só, gerado por diferença contra a ROM limpa."""
    tmp = os.path.join(OUT, '_traducao_v2.ips')
    env = dict(os.environ, FFTA_V2='1')
    subprocess.run([sys.executable, os.path.join(TOOLS, 'build_patch.py'), clean_rom_path, tmp], check=True, env=env, stdout=subprocess.DEVNULL)
    clean = open(clean_rom_path, 'rb').read(); r = bytearray(clean)
    layers = [tmp] + [os.path.join(HERE, 'final_v1', n + '.ips') for n in ('bal20_classes', 'bal21_itens', 'bal22_habilidades', 'bal23_magias')] + \
             [os.path.join(OUT, n + '.ips') for n in ('bal24_habilidades_novas', 'bal25_contrajogo')]
    touched = {}
    for p in layers:
        for o, d in ips.parse(p):
            for k in range(o, o + len(d)):
                if k in touched and touched[k] != p and not p.endswith('_traducao_v2.ips') and touched[k].endswith('_traducao_v2.ips'):
                    raise SystemExit('sobreposição entre tradução e rebalance em %X' % k)
                touched[k] = p
            r[o:o + len(d)] = d
    # diff -> IPS (blocos contíguos, separados por até 8 bytes iguais)
    edits, i, n = {}, 0, len(clean)
    while i < n:
        if r[i] != clean[i]:
            j = i
            while j < n and (r[j] != clean[j] or (j + 8 < n and r[j:j + 8] != clean[j:j + 8])): j += 1
            edits[i] = bytes(r[i:j]); i = j
        else: i += 1
    outp = os.path.join(OUT, 'FFTA_ptBR_rebalance_v2.ips'); write_ips(outp, edits); os.remove(tmp)
    chk = bytearray(clean)
    for o, d in ips.parse(outp): chk[o:o + len(d)] = d
    assert chk == r
    return outp, len(edits)

if __name__ == '__main__':
    e24, e25 = build_data()
    print('bal24: %d registros; bal25: %d' % (len(e24), len(e25)))
    if len(sys.argv) > 1:
        p, n = combined(sys.argv[1], e24, e25); print('patch único:', p, n, 'blocos')
