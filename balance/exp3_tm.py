# -*- coding: utf-8 -*-
import json, sys, multiprocessing as mp
import exp3
from exp3 import jj
TM = jj('Time Mage')
def sp(**k): return dict(base='orig', **k)
BUD = {i: {'hp': ('*', 1.15), 'g_hp': ('*', 1.15), 'dfn': ('*', 1.15), 'g_def': ('*', 1.15)} for i in TM}
V = {'original': sp(),
     'Stop MP 16': sp(mods={'Stop': {'mp': 16}}),
     'Demi MP 16 e Quarter MP 6': sp(mods={'Demi': {'mp': 16}, 'Quarter': {'mp': 6}}),
     'Haste dura 4 turnos': sp(dur={'Haste': 4}),
     'Time Mage +15% HP e DEF': sp(jobmods=BUD),
     'Stop 16 + Demi 16 + Quarter 6': sp(mods={'Stop': {'mp': 16}, 'Demi': {'mp': 16}, 'Quarter': {'mp': 6}}),
     'Stop 16 + Demi 16 + Quarter 6 + 15% HP/DEF': sp(mods={'Stop': {'mp': 16}, 'Demi': {'mp': 16}, 'Quarter': {'mp': 6}}, jobmods=BUD)}
if __name__ == '__main__':
    T = [(lab, spec, i, lv, 2000, 411) for lab, spec in V.items() for i in TM for lv in (10, 25, 45)]
    with mp.Pool(4) as p: R = p.map(exp3.strat_task, T, chunksize=2)
    json.dump(R, open('exp3_tm_raw.json', 'w'), ensure_ascii=False)
    base = {(r['cls'], r['lv']): r['win'] for r in R if r['label'] == 'original'}
    print('| variante | classe | 10 | 25 | 45 | ações (25) | habilidades mais usadas (45) |\n|---|---|---|---|---|---|---|')
    for lab in V:
        for c in sorted({r['cls'] for r in R}):
            rr = {r['lv']: r for r in R if r['label'] == lab and r['cls'] == c}
            print(f"| {lab} | {c} | " + ' | '.join(f"{rr[lv]['win']*100:.0f}%" + ('' if lab == 'original' else f" ({(rr[lv]['win']-base[(c,lv)])*100:+.0f})") for lv in (10, 25, 45)) + f" | {rr[25]['acts']:.0f} | {rr[45]['top']} |")
