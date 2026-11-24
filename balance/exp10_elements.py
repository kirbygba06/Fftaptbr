# -*- coding: utf-8 -*-
"""Diferenciar Fire/Blizzard/Thunder (Black Mage) sem aumentar o poder total.
Fogo = dano; Gelo = controle (Slow dependente do dano, menos dano); Raio = eficiencia (MP menor)."""
import os, sys, json
os.environ.setdefault('PROG', '2'); os.environ.setdefault('APB', '40'); os.environ.setdefault('SEC', '1')
import exp8_round as R, exp9_area as A
DMG = 'AType, Default, 100% Damage'
SLOW = 'SType, Default, Eff1Dep: Inflict Slow'
import math
T = {'': (30, 6), 'ra': (40, 12), 'ga': (50, 24)}
FN = {'': 'Fire', 'ra': 'Fira', 'ga': 'Firaga'}
def trio(fire_p=1.10, ice_p=0.95, ice_eff=SLOW, thu_mp=0.75, tiers=('', 'ra', 'ga')):
    m = {}
    for t, (p, mp) in T.items():
        m[FN[t]] = {'power': round(p * fire_p)}
        m['Blizzard' if t == '' else 'Blizza' + t] = {'power': round(p * ice_p), **({'eff': [DMG, ice_eff]} if (ice_eff and t in tiers) else {})}
        m['Thunder' if t == '' else 'Thunda' + t] = {'mp': math.ceil(mp * thu_mp)}
    return m
VARS = {'e3': trio(1.20, 0.85), 'e5': {**trio(1.20, 0.85, thu_mp=1.0), 'Thunder': {'power': 27, 'area': 'r2/v1'}, 'Thundara': {'power': 36, 'area': 'r2/v2'}}, 'e1': trio(), 'e0': trio(1.0, 1.0, None, 1.0)}
if __name__ == '__main__':
    k = sys.argv[1]; sp = dict(A.spec_for('sel')); sp['mods'] = A.merge(sp['mods'], VARS[k])
    R.run_team_n('v3_' + k, sp, {'25': 12000, '45': 4000})
