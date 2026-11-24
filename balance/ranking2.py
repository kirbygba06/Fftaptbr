# -*- coding: utf-8 -*-
"""Ranking com o modelo de progressão por estoque de loja + AP acumulado. Uso: python3 ranking2.py <orig> <r2> <final> <v2_anterior> <saida>"""
import json, sys, statistics as S
import sim, sim2, progression
o, r, f, prev, outp = sys.argv[1:6]
J = {str(j['id']): j for j in sim.load()['jobs']}; race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
T = {n: json.load(open(f'exp3_team_{n}.json')) for n in (o, r, f, prev)}
up = lambda n, lv, k: 25 * T[n][lv]['coef'][k]; LV = ('10', '25', '45')
tier = lambda v: 'S' if v >= 10 else 'A' if v >= 3 else 'B' if v > -3 else 'C' if v > -10 else 'D'
def conf(c):
    A, _ = sim2.kit_for(c, 300)
    ok = [a for a in A if any(e['kind'] != 'noop' and not (e['kind'] == 'dmg' and not a.basis) for e in a.eff)]
    if not ok: return 'baixa (kit não modelado)'
    if c == 'Templar': return 'média (Rasp, Soul Sphere, Lifebreak sem valor)'
    q = len(ok) / len(A); return 'alta' if q >= .85 else 'média' if q >= .5 else 'baixa'
rows = []
for k, j in J.items():
    fl = [up(f, lv, k) for lv in LV]
    n10 = len(progression.kit_prog(j['name'], 10, 40)[0])
    rows.append(dict(nm=f"{j['name']} ({race[j['race']]})", f=fl, mf=S.mean(fl), mp=S.mean(up(prev, lv, k) for lv in LV), mo=S.mean(up(o, lv, k) for lv in LV), mr=S.mean(up(r, lv, k) for lv in LV), conf=conf(j['name']), n10=n10))
rows.sort(key=lambda x: -x['mf'])
sd = lambda n: S.mean(S.pstdev([up(n, lv, k) for k in J]) for lv in LV)
cnt = lambda key: {t: sum(1 for x in rows if tier(x[key]) == t) for t in 'SABCD'}
L = ['# Ranking v3: progressão de habilidades por estoque da loja e AP acumulado\n',
     '**Modelo:** a habilidade só existe se a arma que a ensina estiver no estoque (inicial; após 10 batalhas; após 20; depois) e se o AP acumulado (40 AP por batalha, 12 batalhas no nível 10, 40 no 25, 90 no 45) cobrir o custo; aprende-se do mais barato ao mais caro. **Não há mais corte "AP ≤ 100 no nível 10".** Estoque das armas: lista que você mandou (10 e 20 batalhas); armas não listadas contam como estoque inicial se custam ≤ 1.200 e como estoque tardio (após 35 batalhas) nas demais.',
     '**Pacote avaliado:** R2 (classes e itens) + Gunner 6 MP + Cupid 8 MP + Phantasm 30 + Unicorn e Cura a 100 AP + Haste em área + Paladin (Nurse 45, Saint Cross 45/18 MP, Holy Blade 24 MP) + Elementalist (4 habilidades a 40) + magias tier 2 e 3 + First Aid 40 + Illusionist ×0,8 + orçamento +8% em Assassin, Fencer, Soldier, Mog Knight, Juggler, Red Mage.',
     'Efeito na equipe (5 contra 5, mapa variável, 12.000 batalhas por nível, erro ≈ ±1): pontos percentuais que a equipe vence a mais por ter a classe. Tier: S ≥ +10, A +3 a +10, B −3 a +3, C −10 a −3, D < −10.', '',
     f'Desvio entre classes: original (neste modelo) {sd(o):.1f} pp · R2 {sd(r):.1f} · **pacote {sd(f):.1f}** · (pacote no modelo antigo de AP: {sd(prev):.1f}).', '',
     '| # | classe | tier | pacote (10/25/45) | média | no modelo antigo (AP ≤ corte) | original neste modelo | R2 neste modelo | habilidades no nível 10 | confiança |', '|---|---|---|---|---|---|---|---|---|---|']
for i, x in enumerate(rows, 1):
    L.append(f"| {i} | {x['nm']} | {tier(x['mf'])} | {' / '.join(f'{v:+.0f}' for v in x['f'])} | **{x['mf']:+.1f}** | {x['mp']:+.1f} | {x['mo']:+.1f} | {x['mr']:+.1f} | {x['n10']} | {x['conf']} |")
c1, c0, cp = cnt('mf'), cnt('mo'), cnt('mp')
L += ['', 'Tiers S/A/B/C/D: original ' + '/'.join(str(c0[t]) for t in 'SABCD') + ' · pacote ' + '/'.join(str(c1[t]) for t in 'SABCD') + ' · pacote no modelo antigo ' + '/'.join(str(cp[t]) for t in 'SABCD') + '.']
open(outp, 'w').write('\n'.join(L)); print('\n'.join(L))
