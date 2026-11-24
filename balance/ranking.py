# -*- coding: utf-8 -*-
"""Ranking das 42 classes (efeito na equipe) a partir de exp3_team_<nome>.json. Uso: python3 ranking.py <nome_final> <arquivo_saida> [descrição]"""
import json, sys, statistics as S
import sim, sim2
name = sys.argv[1]; outp = sys.argv[2]; desc = sys.argv[3] if len(sys.argv) > 3 else name
J = {str(j['id']): j for j in sim.load()['jobs']}; race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
T = {n: json.load(open(f'exp3_team_{n}.json')) for n in ('orig', 'r2', name)}
up = lambda n, lv, k: 25 * T[n][lv]['coef'][k]; se = lambda n, lv, k: 25 * T[n][lv]['se'][k]
LV = ('10', '25', '45'); PARTIAL = {'Templar': 'média (Rasp, Soul Sphere e Lifebreak sem valor no modelo)'}
def conf(c):
    A, _ = sim2.kit_for(c, 300)
    ok = [a for a in A if any(e['kind'] != 'noop' and not (e['kind'] == 'dmg' and not a.basis) for e in a.eff)]
    if not ok: return 'baixa (kit de ação não modelado)'
    if c in PARTIAL: return PARTIAL[c]
    f = len(ok) / len(A); return f"{'alta' if f >= .85 else 'média' if f >= .5 else 'baixa'} ({len(ok)}/{len(A)})"
tier = lambda v: 'S' if v >= 10 else 'A' if v >= 3 else 'B' if v > -3 else 'C' if v > -10 else 'D'
rows = []
for k, j in J.items():
    f = [up(name, lv, k) for lv in LV]
    rows.append(dict(k=k, nm=f"{j['name']} ({race[j['race']]})", f=f, mf=S.mean(f), mo=S.mean(up('orig', lv, k) for lv in LV), mr=S.mean(up('r2', lv, k) for lv in LV), conf=conf(j['name'])))
rows.sort(key=lambda r: -r['mf'])
sd = lambda n: S.mean(S.pstdev([up(n, lv, k) for k in J]) for lv in LV)
L = [f'# Ranking das 42 classes: {desc}\n', 'Efeito na equipe (5 contra 5, mapa variável): pontos percentuais a mais que a equipe vence por ter a classe, em relação a uma classe média no lugar (erro ≈ ±1). Média dos níveis 10, 25 e 45. Tier: S ≥ +10, A +3 a +10, B −3 a +3, C −10 a −3, D < −10.', '',
     f'Desvio entre classes: original {sd("orig"):.1f} pp, R2 {sd("r2"):.1f} pp, **esta versão {sd(name):.1f} pp**.', '',
     '| # | classe | tier | esta versão (10/25/45) | média | original | R2 | confiança do modelo |', '|---|---|---|---|---|---|---|---|']
for i, r in enumerate(rows, 1):
    L.append(f"| {i} | {r['nm']} | {tier(r['mf'])} | {' / '.join(f'{x:+.0f}' for x in r['f'])} | **{r['mf']:+.1f}** | {r['mo']:+.1f} | {r['mr']:+.1f} | {r['conf']} |")
cnt = {t: sum(1 for r in rows if tier(r['mf']) == t) for t in 'SABCD'}; c0 = {t: sum(1 for r in rows if tier(r['mo']) == t) for t in 'SABCD'}
L += ['', 'Tiers (original → esta versão): ' + ', '.join(f'{t} {c0[t]}→{cnt[t]}' for t in 'SABCD') + '.']
open(outp, 'w').write('\n'.join(L)); print('\n'.join(L))
