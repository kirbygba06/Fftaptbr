# -*- coding: utf-8 -*-
"""Calibra o orçamento do Illusionist dentro do pacote final (R2 + Phantasm 30 + Unicorn/Cura AP100 + Haste em área)."""
import json, sys, multiprocessing as mp
import exp3, f1, sim
from exp3 import jj, k5, AB, scn0
FINAL = dict(mods={**{n: {'power': 30} for n in exp3.PHANT}, 'Haste': {'area': 'r1/v2'}}, ap={'Unicorn': 100, 'Cura': 100})
ILL = jj('Illusionist')
def spec_k(factor):
    sp = dict(base='ref2', **FINAL); sp['kscale'] = {i: factor for i in ILL}; return sp
# exp3.spec_build não conhece kscale: reconstrói aqui
_orig = exp3.spec_build
def spec_build(spec):
    if 'kscale' not in spec: return _orig(spec)
    k = dict(k5)
    for i, f in spec['kscale'].items(): k[i] = k5[i] * f
    s = f1.build(scn0, k, mods=AB, atk_scale=1.12); import copy
    s['mods'] = {**(s.get('mods') or {}), **(spec.get('mods') or {})}; return s
exp3.spec_build = spec_build
if __name__ == '__main__':
    print('k5 Illusionist:', {i: round(k5[i], 3) for i in ILL})
    FACT = (1.0, 0.9, 0.8, 0.7)
    T = [(f'orçamento ×{f}', spec_k(f), i, lv, 2500, 611) for f in FACT for i in ILL for lv in (10, 25, 45)]
    with mp.Pool(4) as p: R = p.map(exp3.strat_task, T, chunksize=2)
    json.dump(R, open('exp4_ill_raw.json', 'w'), ensure_ascii=False)
    print('| fator sobre o orçamento do R2 | classe | 10 | 25 | 45 | média | ações (25) |\n|---|---|---|---|---|---|---|')
    for f in FACT:
        for i in ILL:
            rr = {r['lv']: r for r in R if r['label'] == f'orçamento ×{f}' and r['j'] == i}
            m = sum(rr[lv]['win'] for lv in (10, 25, 45)) / 3 * 100
            print(f"| ×{f} (k={k5[i]*f:.2f}) | {rr[10]['cls']} | " + ' | '.join(f"{rr[lv]['win']*100:.0f}%" for lv in (10, 25, 45)) + f" | **{m:.0f}%** | {rr[25]['acts']:.0f} |")
