# -*- coding: utf-8 -*-
"""Rebalance v2: F3 (final v1) + habilidades novas. Mesmo simulador (com dreno, empurrão e acerto modificado) para base e v2."""
import os, sys, copy
os.environ.setdefault('PROG', '2'); os.environ.setdefault('APB', '40'); os.environ.setdefault('SEC', '1')
import exp8_round as R, exp9_area as A, final1 as F, v2_design as V
def spec(k, extra=None):
    sp = F.build3()
    if k != 'base':
        m = V.sim_mods()
        if k == 'noveil': [m.pop(n) for n in V.VEILS]
        sp['mods'] = A.merge(sp['mods'], m)
    if extra: sp['mods'] = A.merge(sp['mods'], extra)
    return sp
if __name__ == '__main__':
    k = sys.argv[1]; R.run_team_n('v2_' + k, spec(k), {'25': 12000, '10': 4000, '45': 6000})
