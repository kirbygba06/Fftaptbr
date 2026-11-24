import json, statistics as S
R = json.load(open('exp4_classes_raw.json'))
base = {(r['cls'], r['lv']): r['win'] for r in R if r['label'] == 'base'}
labs = []; [labs.append(r['label']) for r in R if r['label'] not in labs and r['label'] != 'base']
out = ['| variante | classe | nível 10 | 25 | 45 | média Δ | conclusivo (|Δ médio| ≥ 4 e sinal igual em ≥2 níveis) | habilidades mais usadas (45) |', '|---|---|---|---|---|---|---|---|']
res = {}
for lab in labs:
    for c in sorted({r['cls'] for r in R if r['label'] == lab}):
        rr = {r['lv']: r for r in R if r['label'] == lab and r['cls'] == c}
        d = [(rr[lv]['win'] - base[(c, lv)]) * 100 for lv in (10, 25, 45)]; m = S.mean(d)
        same = sum(1 for x in d if x * m > 0 and abs(x) >= 2) >= 2
        res[(lab, c)] = (d, m, abs(m) >= 4 and same)
        out.append(f"| {lab} | {c} | " + ' | '.join(f'{x:+.0f}' for x in d) + f" | **{m:+.1f}** | {'sim' if abs(m) >= 4 and same else 'não'} | {rr[45]['top']} |")
out.append('\n**Base (pacote final com Illusionist ×0,8), vitória % por nível 10/25/45**\n\n| classe | 10 | 25 | 45 | média |\n|---|---|---|---|---|')
for c in sorted({r['cls'] for r in R if r['label'] == 'base'}):
    w = [base[(c, lv)] * 100 for lv in (10, 25, 45)]; out.append(f'| {c} | ' + ' | '.join(f'{x:.0f}%' for x in w) + f' | {S.mean(w):.0f}% |')
open('exp4_result.md', 'w').write('\n'.join(out)); print('\n'.join(out))
json.dump({f'{k[0]}||{k[1]}': v for k, v in res.items()}, open('exp4_res.json', 'w'))
