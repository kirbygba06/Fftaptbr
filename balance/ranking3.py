# -*- coding: utf-8 -*-
"""Ranking v4: progressão com estoque inicial real, pré-requisitos de classe por raça e 40 AP por batalha."""
import json, sys, statistics as S
import sim, sim2, progression
J = {str(j['id']): j for j in sim.load()['jobs']}; race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
names = dict(o='q_orig', r='q_r2', f='q_final3', b='q_final3_b15', n='q_final3_nosec')
T = {k: json.load(open(f'exp3_team_{v}.json')) for k, v in names.items()}
LV = ('10', '25', '45')
def val(n, lv, k):
    d = T[n][lv]; return 25 * d['coef'][k] if k in d['avail'] else None
def mean_av(n, k):
    v = [val(n, lv, k) for lv in LV if val(n, lv, k) is not None]; return S.mean(v) if v else None
tier = lambda v: 'S' if v >= 10 else 'A' if v >= 3 else 'B' if v > -3 else 'C' if v > -10 else 'D'
def conf(c):
    A, _ = sim2.kit_for(c, 300)
    ok = [a for a in A if any(e['kind'] != 'noop' and not (e['kind'] == 'dmg' and not a.basis) for e in a.eff)]
    if not ok: return 'baixa (kit não modelado)'
    if c == 'Templar': return 'média (Rasp, Soul Sphere, Lifebreak sem valor)'
    q = len(ok) / len(A); return 'alta' if q >= .85 else 'média' if q >= .5 else 'baixa'
rows = []
for k, j in J.items():
    pl = {lv: progression.plan(j['race'], j['name'], int(lv)) for lv in LV}
    first = next(lv for lv in LV if pl[lv]['feasible'])
    rows.append(dict(nm=f"{j['name']} ({race[j['race']]})", f=[val('f', lv, k) for lv in LV], mf=mean_av('f', k), mb=mean_av('b', k), mo=mean_av('o', k), mr=mean_av('r', k), mn=mean_av('n', k),
                     first=first, cost=pl[first]['cost'], kit=[len(pl[lv]['kit_A']) if pl[lv]['feasible'] else None for lv in LV], conf=conf(j['name'])))
rows.sort(key=lambda x: -x['mf'])
def sd(n): return S.mean(S.pstdev([val(n, lv, k) for k in J if val(n, lv, k) is not None]) for lv in LV)
fm = lambda v: 'n/d' if v is None else f'{v:+.0f}'
rank_b = {r['nm']: i for i, r in enumerate(sorted(rows, key=lambda x: -(x['mb'] if x['mb'] is not None else -99)), 1)}
L = ['# Ranking v4: progressão com estoque real da loja, pré-requisitos de classe e 40 AP por batalha\n',
     '**O que mudou no modelo:** (1) estoque inicial = a loja base que você enviou (24 armas); armas das listas de 10 e 20 batalhas liberam depois; o resto só após ~35 batalhas. (2) **Cada classe só existe depois que a unidade domina as A-abilities exigidas** (tabela por raça que você enviou); esse AP sai do mesmo orçamento de **40 AP por batalha**, e o AP que sobra compra as habilidades da própria classe, do mais barato ao mais caro. (3) As habilidades dominadas como pré-requisito ficam disponíveis como conjunto secundário (a coluna "sem conjunto secundário" mostra o ranking sem essa suposição). (4) Classes cujo custo de pré-requisito excede o AP acumulado **não entram nas lutas daquele nível**.',
     'Batalhas até o nível: 12 (nível 10), 40 (25), 90 (45) (suposição). No nível 10 ficam indisponíveis (AP insuficiente): Illusionist ×2 (custo 1.200 AP), Alchemist (1.200), Morpher (1.000), Sage (900), Assassin (800), Summoner (700), Time Mage ×2 (700). A partir do nível 25 todas existem.',
     '**Pacote avaliado:** R2 (classes e itens) + Gunner 6 MP + Cupid 8 MP + Phantasm 30 + Unicorn e Cura 100 AP + Haste em área + Paladin (Nurse 45, Saint Cross 45/18, Holy Blade 24) + Elementalist (4 habilidades a 40) + magias tier 2 e 3 + First Aid 40 + Illusionist ×0,8 + orçamento +8% em Assassin, Fencer, Soldier, Mog Knight, Juggler, Red Mage.',
     'Efeito na equipe (5 contra 5, mapa variável, 12.000 batalhas por nível, erro ≈ ±1): pontos percentuais que a equipe vence a mais por ter a classe; média só dos níveis em que a classe existe. Tier: S ≥ +10, A +3 a +10, B −3 a +3, C −10 a −3, D < −10.', '',
     f'Desvio entre classes: original {sd("o"):.1f} pp · R2 {sd("r"):.1f} · **pacote {sd("f"):.1f}** · pacote com 50% mais batalhas por nível {sd("b"):.1f}.', '',
     '| # | classe | tier | pacote (10/25/45) | média | 1º nível em que existe (custo de pré-requisito) | habilidades de ação no kit 10/25/45 | original | R2 | com +50% de batalhas (posto) | sem conjunto secundário | confiança |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for i, x in enumerate(rows, 1):
    L.append(f"| {i} | {x['nm']} | {tier(x['mf'])} | {' / '.join(fm(v) for v in x['f'])} | **{x['mf']:+.1f}** | {x['first']} ({x['cost']} AP) | {' / '.join('–' if v is None else str(v) for v in x['kit'])} | {x['mo']:+.1f} | {x['mr']:+.1f} | {x['mb']:+.1f} (#{rank_b[x['nm']]}) | {x['mn']:+.1f} | {x['conf']} |")
cnt = lambda key: {t: sum(1 for x in rows if x[key] is not None and tier(x[key]) == t) for t in 'SABCD'}
c1, c0 = cnt('mf'), cnt('mo')
L += ['', 'Tiers S/A/B/C/D: original ' + '/'.join(str(c0[t]) for t in 'SABCD') + ' · pacote ' + '/'.join(str(c1[t]) for t in 'SABCD') + '.']
a = [r['mf'] for r in rows]; b = [rank_b[r['nm']] for r in rows]
import statistics
rho = statistics.correlation(list(range(1, len(rows) + 1)), b)
L += [f'Correlação de postos entre o ranking e o de +50% de batalhas: {rho:.2f}.']
open('RANKING_CLASSES_V4.md', 'w').write('\n'.join(L)); print('\n'.join(L))
