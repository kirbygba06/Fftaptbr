# -*- coding: utf-8 -*-
"""Gera o Rebalance FINAL v1 (somente dados) a partir do MESMO spec usado no simulador (final1.build).
Saídas em balance/final_v1/: 4 patches IPS modulares (bal20 classes, bal21 itens, bal22 habilidades, bal23 magias),
4 patches de reversão, CSV original/modificado de cada módulo e verificação de bytes (aplica, relê, reverte).
Uso: python3 make_final_ips.py [variante]   (padrão: F1)"""
import os, sys, csv, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import ips
import final1, exp3
from romdata import JOB_BASE, ITEM_BASE, ABIL_BASE, rom, jobs, items, abilities
from make_stats_ips import enc_job
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'final_v1')
os.makedirs(os.path.join(OUT, 'reverter'), exist_ok=True); os.makedirs(os.path.join(OUT, 'csv'), exist_ok=True)
EFF_ID = {'SType, Default, Eff1Dep: Inflict Slow': 103, '100%H, Default, Eff1Dep: Delay Unit': 27}   # IDs já usados por Sliprain / Hand Slap
TRIO = {'Fire', 'Fira', 'Firaga', 'Blizzard', 'Blizzara', 'Blizzaga', 'Thunder', 'Thundara', 'Thundaga'}

def write_ips(path, edits):
    out = bytearray(b'PATCH')
    for off, data in sorted(edits.items()):
        assert off != 0x454F46 and off + len(data) <= 0x1000000 and 0 < len(data) < 0xFFFF
        out += off.to_bytes(3, 'big') + len(data).to_bytes(2, 'big') + bytes(data)
    open(path, 'wb').write(out + b'EOF')
def save(name, edits):
    """Grava o patch e o de reversão (bytes originais nas mesmas posições). Só regiões que realmente mudam."""
    ed = {o: bytes(d) for o, d in edits.items() if bytes(d) != rom[o:o + len(d)]}
    write_ips(os.path.join(OUT, name + '.ips'), ed)
    write_ips(os.path.join(OUT, 'reverter', name + '_reverter.ips'), {o: rom[o:o + len(d)] for o, d in ed.items()})
    return ed
def wcsv(name, rows, keys):
    with open(os.path.join(OUT, 'csv', name), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(keys); [w.writerow([r.get(k, '') for k in keys]) for r in rows]

def main(var='F1'):
    spec = final1.build3() if var == 'F3' else final1.build2() if var == 'F2' else final1.build(**final1.VARS[var]); s = exp3.spec_build(spec)
    # ---------- bal20 classes ----------
    J0 = {j['id']: j for j in jobs()}; e20 = {}; rows = []
    JK = ('hp', 'mp', 'spd', 'atk', 'dfn', 'pow', 'res', 'g_hp', 'g_mp', 'g_spd', 'g_atk', 'g_def', 'g_pow', 'g_res', 'eva')
    for j in s['jobs']:
        a = JOB_BASE + 0x34 * j['id']; raw = rom[a:a + 0x34]; new = enc_job(j, raw)
        e20[a + 0x17] = new[0x17:0x28]; e20[a + 0x2A] = new[0x2A:0x2B]
        o = J0[j['id']]
        if any(o[k] != j[k] for k in JK):
            rows.append({'id': j['id'], 'classe': j['name'], 'raca': j['race'], **{k + '_orig': o[k] for k in JK}, **{k + '_novo': j[k] for k in JK}})
    e20 = save('bal20_classes', e20)
    wcsv('bal20_classes.csv', rows, ['id', 'classe', 'raca'] + [k + s_ for k in JK for s_ in ('_orig', '_novo')])
    # ---------- bal21 itens ----------
    I0 = {t['idx']: t for t in items()}; e21 = {}; rows = []
    for t in s['items']:
        o = I0[t['idx']]; a = ITEM_BASE + 0x20 * t['idx']
        if (o['buy'], o['sell']) != (t['buy'], t['sell']): e21[a + 4] = t['buy'].to_bytes(2, 'little') + t['sell'].to_bytes(2, 'little')
        if (o['atk'], o['dfn'], o['res'], o['eva']) != (t['atk'], t['dfn'], t['res'], t['eva']):
            r = bytearray(rom[a + 0x10:a + 0x16]); r[0] = t['atk']; r[1] = t['dfn']; r[3] = t['res']; r[5] = t['eva'] & 0xFF; e21[a + 0x10] = bytes(r)
        if any(o[k] != t[k] for k in ('buy', 'sell', 'atk', 'dfn', 'res', 'eva')):
            rows.append({'idx': t['idx'], 'item': t['name'], **{k + '_orig': o[k] for k in ('buy', 'sell', 'atk', 'dfn', 'res', 'eva')}, **{k + '_novo': t[k] for k in ('buy', 'sell', 'atk', 'dfn', 'res', 'eva')}})
    e21 = save('bal21_itens', e21)
    wcsv('bal21_itens.csv', rows, ['idx', 'item'] + [k + s_ for k in ('buy', 'sell', 'atk', 'dfn', 'res', 'eva') for s_ in ('_orig', '_novo')])
    # ---------- bal22 habilidades / bal23 magias ----------
    A = {x['name']: x for x in abilities() if x['name'] not in ('-', '')}
    mods = {n: (m if isinstance(m, dict) else {'mp': m}) for n, m in s['mods'].items()}
    for n, ap in (s.get('_ap') or {}).items(): mods.setdefault(n, {})['ap'] = ap
    e22, e23, r22, r23 = {}, {}, [], []
    for n, m in sorted(mods.items()):
        x = A[n]; a = ABIL_BASE + 0x1C * x['idx']; r = bytearray(rom[a:a + 0x1C])
        if 'mp' in m: r[4] = int(m['mp'])
        if 'power' in m: r[0xB] = int(m['power'])
        if 'ap' in m: r[3] = int(m['ap']) // 10
        if 'area' in m:
            ar = m['area']
            if ar == 'One Unit': r[9], r[0xA] = 1, 0
            else:
                assert ar.startswith('r1/v'), ar; assert (x['area'], x['varea']) == (1, 0), (n, x['area'])
                r[9], r[0xA] = 5, int(ar[4:])
        if 'eff' in m:
            assert x['fx'] == [63, 1, 1, 1] and n in TRIO, (n, x['fx']); r[0xD] = EFF_ID[m['eff'][1]]
        row = {'id': x['idx'], 'habilidade': n, 'mp_orig': rom[a + 4], 'mp_novo': r[4], 'poder_orig': rom[a + 0xB], 'poder_novo': r[0xB],
               'ap_orig': rom[a + 3] * 10, 'ap_novo': r[3] * 10, 'area_orig': f'{rom[a + 9]}/{rom[a + 10]}', 'area_novo': f'{r[9]}/{r[10]}',
               'efeito2_orig': rom[a + 0xD], 'efeito2_novo': r[0xD]}
        if bytes(r) == rom[a:a + 0x1C]: continue
        tgt = e23 if n in TRIO else e22; tgt[a + 3] = bytes(r[3:0xE]); (r23 if n in TRIO else r22).append(row)
    e22 = save('bal22_habilidades', e22); e23 = save('bal23_magias', e23)
    K = ['id', 'habilidade', 'mp_orig', 'mp_novo', 'poder_orig', 'poder_novo', 'ap_orig', 'ap_novo', 'area_orig', 'area_novo', 'efeito2_orig', 'efeito2_novo']
    wcsv('bal22_habilidades.csv', r22, K); wcsv('bal23_magias.csv', r23, K)
    # patch único (os 4 módulos juntos) e o de reversão correspondente
    allm = {**e20, **e21, **e22, **e23}; write_ips(os.path.join(OUT, 'FFTA_rebalance_final_v1.ips'), allm)
    write_ips(os.path.join(OUT, 'reverter', 'FFTA_rebalance_final_v1_reverter.ips'), {o: rom[o:o + len(d)] for o, d in allm.items()})
    # ---------- verificação ----------
    names = ['bal20_classes', 'bal21_itens', 'bal22_habilidades', 'bal23_magias']
    spans = []
    for nm in names:
        for o, d in ips.parse(os.path.join(OUT, nm + '.ips')): spans.append((o, o + len(d), nm))
    spans.sort(); over = [(a, b) for a, b in zip(spans, spans[1:]) if b[0] < a[1]]
    pat = bytearray(rom)
    for nm in names:
        for o, d in ips.parse(os.path.join(OUT, nm + '.ips')): pat[o:o + len(d)] = d
    bad = 0
    for j in s['jobs']:
        a = JOB_BASE + 0x34 * j['id']; r = pat[a:a + 0x34]
        got = dict(hp=r[0x17], mp=r[0x18], spd=r[0x19], atk=((r[0x1B] & 0xF) << 8) | r[0x1A], dfn=(r[0x1C] << 4) | (r[0x1B] >> 4),
                   pow=((r[0x1E] & 0xF) << 8) | r[0x1D], res=(r[0x1F] << 4) | (r[0x1E] >> 4), eva=r[0x2A])
        bad += sum(1 for k, v in got.items() if v != j[k])
        bad += sum(1 for k_, key in zip(range(0x20, 0x27), ('g_hp', 'g_mp', 'g_spd', 'g_atk', 'g_def', 'g_pow', 'g_res')) if r[k_] != int(round(j[key] * 10)))
    for t in s['items']:
        a = ITEM_BASE + 0x20 * t['idx']; r = pat[a:a + 0x20]
        bad += (int.from_bytes(r[4:6], 'little'), int.from_bytes(r[6:8], 'little'), r[0x10], r[0x11], r[0x13]) != (t['buy'], t['sell'], t['atk'], t['dfn'], t['res'])
    for n, m in mods.items():
        a = ABIL_BASE + 0x1C * A[n]['idx']
        bad += ('mp' in m and pat[a + 4] != int(m['mp'])) + ('power' in m and pat[a + 0xB] != int(m['power'])) + ('ap' in m and pat[a + 3] * 10 != int(m['ap']))
    # reversão: aplica os 4 de reversão por cima e compara com a ROM original
    for nm in names:
        for o, d in ips.parse(os.path.join(OUT, 'reverter', nm + '_reverter.ips')): pat[o:o + len(d)] = d
    rev_ok = bytes(pat) == bytes(rom)
    # independência: cada patch sozinho só toca a sua tabela
    zones = {'bal20_classes': (JOB_BASE, JOB_BASE + 0x34 * 115), 'bal21_itens': (ITEM_BASE, ITEM_BASE + 0x20 * 400), 'bal22_habilidades': (ABIL_BASE, ABIL_BASE + 0x1C * 400), 'bal23_magias': (ABIL_BASE, ABIL_BASE + 0x1C * 400)}
    out_zone = [(nm, hex(a)) for a, b, nm in spans if not (zones[nm][0] <= a and b <= zones[nm][1])]
    rep = dict(variante=var, registros={nm: len(list(ips.parse(os.path.join(OUT, nm + '.ips')))) for nm in names},
               bytes={nm: sum(len(d) for _, d in ips.parse(os.path.join(OUT, nm + '.ips'))) for nm in names},
               classes=len(open(os.path.join(OUT, 'csv', 'bal20_classes.csv')).read().splitlines()) - 1, itens=len(open(os.path.join(OUT, 'csv', 'bal21_itens.csv')).read().splitlines()) - 1,
               habilidades=len(r22), magias=len(r23), divergencias=int(bad), sobreposicoes=len(over), fora_da_tabela=out_zone, reversao_identica=rev_ok)
    json.dump(rep, open(os.path.join(OUT, 'verificacao.json'), 'w'), ensure_ascii=False, indent=1); print(json.dumps(rep, ensure_ascii=False))
if __name__ == '__main__': main(*(sys.argv[1:] or ['F3']))
