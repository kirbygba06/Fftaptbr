import json, multiprocessing as mp, os
os.environ['PROG'] = '2'
import exp3, exp4_teams_specs as SP
from exp3 import jj
F = SP.SPECS['final3']
V = {'pacote': F, 'sem Haste em área': dict(F, mods={**F['mods'], 'Haste': {'area': 'One Unit'}}), 'sem conjunto secundário': dict(F, sec=0), 'sem Haste em área e sem secundário': dict(F, mods={**F['mods'], 'Haste': {'area': 'One Unit'}}, sec=0)}
ids = jj('Templar') + jj('Blue Mage') + jj('Time Mage') + jj('White Monk') + jj('Summoner')
if __name__ == '__main__':
    T = [(l, s, i, lv, 2000, 811) for l, s in V.items() for i in ids for lv in (10, 25, 45)]
    with mp.Pool(4) as p: R = p.map(exp3.strat_task, T, chunksize=3)
    json.dump(R, open('exp6_diag.json', 'w'), ensure_ascii=False)
    print('| variante | classe | 10 | 25 | 45 |\n|---|---|---|---|---|')
    for l in V:
        for c in sorted({r['cls'] for r in R}):
            rr = {r['lv']: r for r in R if r['label'] == l and r['cls'] == c}
            print(f'| {l} | {c} | ' + ' | '.join('n/d' if rr[lv]['win'] is None else f"{rr[lv]['win']*100:.0f}%" for lv in (10, 25, 45)) + ' |')
