# -*- coding: utf-8 -*-
"""Exporta o F1 final (classes, itens, Totema) para CSV e imprime números usados no F1.md."""
import json, csv, statistics as S, sim, f1
scn0 = sim.load(); k = {int(a): b for a, b in json.load(open('f1_k.json')).items()}; scn1 = f1.build(scn0, k)
J0 = {j['id']: j for j in scn0['jobs']}; race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
rows = []
for j in scn1['jobs']:
    o = J0[j['id']]
    rows.append(dict(id=j['id'], classe=j['name'], raca=race[j['race']], papel=f1.ROLE.get(j['name'], '?'), k=k[j['id']],
        hp=(o['hp'], j['hp']), mp=(o['mp'], j['mp']), spd=(o['spd'], j['spd']), atk=(o['atk'], j['atk']), dfn=(o['dfn'], j['dfn']), pow=(o['pow'], j['pow']), res=(o['res'], j['res']),
        g_hp=(o['g_hp'], j['g_hp']), g_mp=(o['g_mp'], j['g_mp']), g_spd=(o['g_spd'], j['g_spd']), g_atk=(o['g_atk'], j['g_atk']), g_def=(o['g_def'], j['g_def']), g_pow=(o['g_pow'], j['g_pow']), g_res=(o['g_res'], j['g_res']), eva=(o['eva'], j['eva'])))
cols = ['id', 'classe', 'raca', 'papel', 'k'] + [c for c in rows[0] if c not in ('id', 'classe', 'raca', 'papel', 'k')]
with open('f1_classes.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'classe', 'raca', 'papel', 'k'] + [f'{c}_antes,{c}_depois' for c in cols[5:]])
    for r in rows: w.writerow([r['id'], r['classe'], r['raca'], r['papel'], r['k']] + [x for c in cols[5:] for x in r[c]])
I0 = {t['idx']: t for t in scn0['items']}
with open('f1_itens.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['idx', 'nome', 'tipo', 'atk_antes', 'atk_depois', 'def_antes', 'def_depois', 'res_antes', 'res_depois', 'eva_antes', 'eva_depois', 'compra_antes', 'compra_depois', 'venda_antes', 'venda_depois'])
    for t in scn1['items']:
        o = I0[t['idx']]
        if (o['atk'], o['dfn'], o['res'], o['eva'], o['buy'], o['sell']) != (t['atk'], t['dfn'], t['res'], t['eva'], t['buy'], t['sell']):
            w.writerow([t['idx'], t['name'], t['type'], o['atk'], t['atk'], o['dfn'], t['dfn'], o['res'], t['res'], o['eva'], t['eva'], o['buy'], t['buy'], o['sell'], t['sell']])
print('itens alterados', sum(1 for t in scn1['items'] if (I0[t['idx']]['atk'], I0[t['idx']]['dfn'], I0[t['idx']]['res'], I0[t['idx']]['eva'], I0[t['idx']]['buy'], I0[t['idx']]['sell']) != (t['atk'], t['dfn'], t['res'], t['eva'], t['buy'], t['sell'])))
# correlação velocidade x vitória
def corr(scn, lv):
    r = sim.run(scn, levels=(lv,), n=3000, seed=21)[lv]; J = [j for j in scn['jobs'] if sim.PROFILE.get(j['name']) in (sim.PHYS, sim.MAGE)]
    v = [j['spd'] * 1.05 + j['g_spd'] * (lv - 1) for j in J]; w = [r[j['id']] for j in J]; mv, mw = S.mean(v), S.mean(w)
    return sum((a - mv) * (b - mw) for a, b in zip(v, w)) / (len(v) * S.pstdev(v) * S.pstdev(w))
print('corr(velocidade, vitória) ATUAL', [round(corr(scn0, l), 2) for l in (10, 25, 45)], 'F1', [round(corr(scn1, l), 2) for l in (10, 25, 45)])
r1 = sim.run(scn1, n=4000, seed=5); nm = {j['id']: j['name'] + '/' + race[j['race']] for j in scn1['jobs']}
for l in (10, 25, 45): print('L', l, 'curandeiros/tempo', {nm[i][:14]: round(w, 2) for i, w in r1[l].items() if sim.PROFILE.get(nm[i].split('/')[0]) in (sim.HEAL, sim.UTIL)})
# armadura: nu -> faixa 4
for name, scn in (('ATUAL', scn0), ('F1', scn1)):
    g = sim.gear(scn['items']); A = 440; D = 470
    nak = max(1, A - D / 2); out = []
    for t in range(4): out.append(f"{(max(1, A - (D + g['phys_def'][t]) / 2) / nak - 1) * 100:.0f}%")
    print(name, 'redução de dano físico recebido (vs sem armadura) faixas 1-4:', out, 'DEF total', [round(x) for x in g['phys_def']])
print('Totema: 85 -> 70 em Mateus, Adrammalech, Ultima, Exodus, Famfrit')
