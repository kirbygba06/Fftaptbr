# -*- coding: utf-8 -*-
import json, statistics as S
import sim, sim2, progression
J = {str(j['id']): j for j in sim.load()['jobs']}; race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
names = dict(o='q2_orig', r='q2_r2', f='q2_final3', p='q2_final3_prereq', n='q2_final3_nosec', m='q2_final3_semmistura')
T = {k: json.load(open(f'exp3_team_{v}.json')) for k, v in names.items()}
LV = ('10', '25', '45')
val = lambda n, lv, k: 25 * T[n][lv]['coef'][k] if k in T[n][lv]['avail'] else None
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
    rows.append(dict(nm=f"{j['name']} ({race[j['race']]})", f=[val('f', lv, k) for lv in LV], mf=mean_av('f', k), mo=mean_av('o', k), mr=mean_av('r', k), mp=mean_av('p', k), mn=mean_av('n', k), mm=mean_av('m', k), first=first, cost=pl[first]['cost'],
                     sec=' / '.join((pl[lv].get('sec_class') or '–') if pl[lv]['feasible'] else '–' for lv in ('10', '25', '45')), kit=[len(pl[lv]['kit_A']) if pl[lv]['feasible'] else None for lv in LV], conf=conf(j['name'])))
rows.sort(key=lambda x: -x['mf'])
sd = lambda n: S.mean(S.pstdev([val(n, lv, k) for k in J if val(n, lv, k) is not None]) for lv in LV)
fm = lambda v: 'n/d' if v is None else f'{v:+.0f}'
rk = lambda key: {r['nm']: i for i, r in enumerate(sorted(rows, key=lambda x: -x[key]), 1)}
rp, rn, rm = rk('mp'), rk('mn'), rk('mm')
L = ['# Ranking v5: conjunto secundário realista, 16 batalhas no nível 10, 40 AP por batalha\n',
     '**Modelo:** loja inicial real (24 armas) + listas de 10 e 20 batalhas; classes só existem após dominar os pré-requisitos (por raça); 40 AP por batalha; **16 batalhas no nível 10** (você chega às 20 entre o 10 e o 15), 40 no 25 e 90 no 45. **Conjunto secundário:** até o nível 15 é o de pré-requisito; depois é escolhido o mais útil entre as classes que a unidade pode usar (valor esperado medido das 3 melhores habilidades), com **preferência forte por não misturar físico e mágico** (peso 0,4 no tipo diferente; White Mage é exceção por ser suporte).',
     '**Mistura físico×mágico:** com o peso 0,4, 18 das 84 escolhas de secundário (classe × nível 25/45) misturam os tipos (ex.: Fighter, Paladin, Mog Knight, Juggler com Black Mage); a coluna "sem mistura" refaz a simulação proibindo isso quando há alternativa.\n\n**Pacote avaliado:** R2 (classes e itens) + Gunner 6 MP + Cupid 8 MP + Phantasm 30 + Unicorn e Cura a 100 AP + Haste em área + Paladin (Nurse 45, Saint Cross 45/18, Holy Blade 24) + Elementalist (4 habilidades a 40) + magias tier 2 e 3 + First Aid 40 + Illusionist ×0,8 + orçamento +8% em Assassin, Fencer, Soldier, Mog Knight, Juggler, Red Mage.',
     'Efeito na equipe (5 contra 5, mapa variável, 12.000 batalhas por nível, erro ≈ ±1): pontos percentuais que a equipe vence a mais por ter a classe; média só dos níveis em que a classe existe. Tier: S ≥ +10, A +3 a +10, B −3 a +3, C −10 a −3, D < −10.', '',
     f'Desvio entre classes: original {sd("o"):.1f} pp · R2 {sd("r"):.1f} · **pacote {sd("f"):.1f}** · só pré-requisito como secundário {sd("p"):.1f} · sem secundário {sd("n"):.1f}.', '',
     '| # | classe | tier | pacote (10/25/45) | média | 1º nível em que existe (AP de pré-requisito) | secundário 10 / 25 / 45 | habilidades de ação 10/25/45 | original | R2 | só pré-req. como secundário (posto) | sem secundário (posto) | sem mistura físico×mágico (posto) | confiança |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for i, x in enumerate(rows, 1):
    L.append(f"| {i} | {x['nm']} | {tier(x['mf'])} | {' / '.join(fm(v) for v in x['f'])} | **{x['mf']:+.1f}** | {x['first']} ({x['cost']} AP) | {x['sec']} | {' / '.join('–' if v is None else str(v) for v in x['kit'])} | {x['mo']:+.1f} | {x['mr']:+.1f} | {x['mp']:+.1f} (#{rp[x['nm']]}) | {x['mn']:+.1f} (#{rn[x['nm']]}) | {x['mm']:+.1f} (#{rm[x['nm']]}) | {x['conf']} |")
cnt = lambda key: {t: sum(1 for x in rows if tier(x[key]) == t) for t in 'SABCD'}
c1, c0 = cnt('mf'), cnt('mo')
L += ['', 'Tiers S/A/B/C/D: original ' + '/'.join(str(c0[t]) for t in 'SABCD') + ' · pacote ' + '/'.join(str(c1[t]) for t in 'SABCD') + '.']
pos = {r['nm']: i for i, r in enumerate(rows, 1)}
L.append(f"Correlação de postos: com secundário escolhido × só pré-requisito {S.correlation([pos[r['nm']] for r in rows], [rp[r['nm']] for r in rows]):.2f}; × sem secundário {S.correlation([pos[r['nm']] for r in rows], [rn[r['nm']] for r in rows]):.2f}; × sem mistura físico×mágico {S.correlation([pos[r['nm']] for r in rows], [rm[r['nm']] for r in rows]):.2f}.")
open('RANKING_CLASSES_V5.md', 'w').write('\n'.join(L)); print('\n'.join(L))
