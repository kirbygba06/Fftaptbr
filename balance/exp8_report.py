# -*- coding: utf-8 -*-
import json, os, statistics as S, collections
import sim, sim2
from exp8_round import underused_from, effective
J = {str(j['id']): j for j in sim.load()['jobs']}; race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
files = [('base', 'exp3_team_q2_final3.json')] + [(f'r{r}', f'exp3_team_v1_r{r}.json') for r in (1, 2, 3) if os.path.exists(f'exp3_team_v1_r{r}.json')]
D = {n: json.load(open(p)) for n, p in files}
def eff(n, lv, k): d = D[n][lv]; return 25 * d['coef'][k] if k in d['avail'] else None
out = ['## Viabilidade das habilidades pouco usadas (equipes de 5, mapa variável, progressão real)\n']
for n in D:
    d = D[n]
    cl = lambda lv: [eff(n, lv, k) for k in J if eff(n, lv, k) is not None]
    out.append(f"- **{n}**: desvio entre classes nível 25 = {S.pstdev(cl('25')):.1f} pp (n = {d['25']['n']}), nível 45 = {S.pstdev(cl('45')):.1f} pp; ações por batalha {d['25']['acts']:.0f} (25), {d['45']['acts']:.0f} (45)")
base_u = underused_from(files[0][1])
for n, p in files[1:]:
    pat = json.load(open(f'exp8_patched_r{n[1:]}.json')); us = underused_from(p)
    out.append(f"\n### Rodada {n[1:]}: {len(pat['mods'])} habilidades alteradas ({len(pat['still'])} reforçadas neste passo)\n")
    # por habilidade: melhor posição entre as classes que a usam
    rows = []
    cand = json.load(open('exp8_underused.json'))
    byab = collections.defaultdict(list)
    for u in cand:
        if u['modeled'] and u['lever'] != 'nenhuma': byab[u['ab']].append(u['cls'])
    nviable = 0
    for ab, cls in sorted(byab.items()):
        m = pat['mods'].get(ab, {}); b = max((base_u.get((c, ab), (0, 0, 0))[0] for c in cls)); a = max((us.get((c, ab), (0, 0, 0))[0] for c in cls))
        viable = a >= 0.03; nviable += viable
        rows.append((ab, cls[0] if len(cls) == 1 else f'{cls[0]} +{len(cls)-1}', m, b, a, viable))
    out.append(f'**{nviable} de {len(byab)} habilidades atingem ≥ 3% de escolha quando disponíveis.**\n')
    out.append('| habilidade | classe | nova potência / MP | escolha antes | escolha depois | viável |\n|---|---|---|---|---|---|')
    for ab, c, m, b, a, v in rows:
        mm = ' / '.join(f'{k} {v_}' for k, v_ in m.items()) or '–'
        out.append(f'| {ab} | {c} | {mm} | {100*b:.1f}% | {100*a:.1f}% | {"sim" if v else "não"} |')
    sh = sorted(((eff(n, '25', k) - eff('base', '25', k), k) for k in J if eff(n, '25', k) is not None and eff('base', '25', k) is not None))
    out.append('\n**Classes que mais mudam (nível 25, pontos de efeito na equipe):** ' + '; '.join(f"{J[k]['name']} ({race[J[k]['race']]}) {d:+.1f}" for d, k in sh[:4] + sh[-6:]))
open('exp8_result.md', 'w').write('\n'.join(out)); print('\n'.join(out)[:7000])
