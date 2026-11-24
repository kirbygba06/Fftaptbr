# -*- coding: utf-8 -*-
"""Trio final: Fogo = dano; Gelo = Slow dependente do dano (menos dano); Raio = Delay Unit dependente do dano (menos dano).
Valores relativos ao pacote atual (T2/T3 do final3). Efeitos já existentes na ROM: Slow dep = 103 (Sliprain), Delay dep = 27 (Hand Slap)."""
import os, sys, math
os.environ.setdefault('PROG', '2'); os.environ.setdefault('APB', '40'); os.environ.setdefault('SEC', '1')
import exp8_round as R, exp9_area as A, exp4_classes as C, sim2
DMG = 'AType, Default, 100% Damage'; SLOW = 'SType, Default, Eff1Dep: Inflict Slow'; DELAY = '100%H, Default, Eff1Dep: Delay Unit'
NAMES = {'F': ('Fire', 'Fira', 'Firaga'), 'B': ('Blizzard', 'Blizzara', 'Blizzaga'), 'T': ('Thunder', 'Thundara', 'Thundaga')}
BASE = A.spec_for('sel')['mods']
def cur(n):
    m = BASE.get(n, {}); a = sim2.CAT[sim2.norm(n)]
    return m.get('power', a.power), m.get('mp', a.mp)
def trio(fp, bp, tp, slow=(0, 1, 2), delay=(0, 1, 2), rm=None):
    out = {}
    for el, f, eff, tiers in (('F', fp, None, ()), ('B', bp, SLOW, slow), ('T', tp, DELAY, delay)):
        for i, n in enumerate(NAMES[el]):
            p, mp = cur(n); out[n] = {'power': int(round(p * f)), 'mp': mp}
            if eff and i in tiers: out[n]['eff'] = [DMG, eff]
    return out
VARS = {'t1': (trio(1.15, 0.80, 0.85), None), 't2': (trio(1.15, 0.80, 0.75), None),
        't3': (trio(1.15, 0.80, 0.85), 1.0)}  # t3 = t1 com Red Mage sem o +8% de orçamento
def spec(k):
    mods, rm = VARS[k]; sp = dict(A.spec_for('sel')); sp['mods'] = A.merge(sp['mods'], mods)
    if rm is not None: sp['kscale'] = {**sp['kscale'], **C.kb(['Red Mage'], rm)}
    return sp
if __name__ == '__main__':
    k = sys.argv[1]; R.run_team_n('v4_' + k, spec(k), {'25': 12000, '45': 4000})
