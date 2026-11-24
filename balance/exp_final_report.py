# -*- coding: utf-8 -*-
import json, statistics as S
import sim
R = json.load(open('exp_final_raw.json')); J = {str(j['id']): j for j in sim.load()['jobs']}
names = []; [names.append(r['name']) for r in R if r['name'] not in names]
race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
out = []
for obs, title in ((0, 'Modo A (status pela fórmula)'), (1, 'Modo B (precisão registrada pela comunidade)')):
    out.append(f'\n## {title}\n\n### Equilíbrio global (42 classes)\n| pacote | nível | faixa de vitória | desvio padrão | classes fora de 40–60% | ações/batalha |\n|---|---|---|---|---|---|')
    for nm in names:
        for lv in (10, 25, 45):
            r = next(x for x in R if x['name'] == nm and x['lv'] == lv and x['obs'] == obs); v = list(r['win'].values())
            out.append(f"| {nm} | {lv} | {min(v) * 100:.0f}%–{max(v) * 100:.0f}% | {S.pstdev(v):.3f} | {sum(1 for x in v if x < .4 or x > .6)} | {r['acts']:.0f} |")
base = {lv: next(x for x in R if x['name'] == 'original' and x['lv'] == lv and x['obs'] == 0) for lv in (10, 25, 45)}
full = {lv: next(x for x in R if x['name'] == 'pacote completo' and x['lv'] == lv and x['obs'] == 0) for lv in (10, 25, 45)}
out.append('\n### Cada classe: original → pacote completo (Modo A, média dos níveis 10/25/45)\n| classe | raça | original | completo | variação |\n|---|---|---|---|---|')
rows = []
for k, j in J.items():
    o = S.mean(base[lv]['win'][k] for lv in (10, 25, 45)); f = S.mean(full[lv]['win'][k] for lv in (10, 25, 45)); rows.append((o, j['name'], race[j['race']], f))
for o, n, rc, f in sorted(rows, reverse=True): out.append(f'| {n} | {rc} | {o * 100:.0f}% | {f * 100:.0f}% | {(f - o) * 100:+.0f} |')
open('exp_final_result.md', 'w').write('\n'.join(out)); print('\n'.join(out)[:3500])
