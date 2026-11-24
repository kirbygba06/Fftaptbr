# -*- coding: utf-8 -*-
"""Variantes de melhoria das classes fracas (somente dados), isoladas e combinadas. Estratificado: a classe sempre no time A (5 vs 5, mapa variável)."""
import json, sys, multiprocessing as mp
import exp3
from exp3 import jj, PHANT, SLOW
def sp(**k): return dict(base=k.pop('base', 'orig'), **k)
PH = lambda **v: {n: v for n in PHANT}
V = {
 'original': sp(),
 'Phantasm poder 30': sp(mods=PH(power=30)),
 'Phantasm MP 24': sp(mods=PH(mp=24)),
 'Phantasm poder 30 e MP 24': sp(mods=PH(power=30, mp=24)),
 'Haste MP 16': sp(mods={'Haste': {'mp': 16}}),
 'Haste AP 100': sp(ap={'Haste': 100}),
 'Haste MP 16 e AP 100': sp(mods={'Haste': {'mp': 16}}, ap={'Haste': 100}),
 'Unicorn e Cura AP 100': sp(ap={'Unicorn': 100, 'Cura': 100}),
 'piso de velocidade (+10 base, +0,3 cresc.)': sp(jobmods={i: {'spd': ('+', 10), 'g_spd': ('+', 0.3)} for i in SLOW}),
}
ALLV = dict(V); ALLV['pacote de correções'] = sp(mods={**PH(power=30, mp=24), 'Haste': {'mp': 16}}, ap={'Haste': 100, 'Unicorn': 100, 'Cura': 100},
                                                 jobmods={i: {'spd': ('+', 10), 'g_spd': ('+', 0.3)} for i in SLOW})
CL = {'Illusionist': jj('Illusionist'), 'Time Mage': jj('Time Mage'), 'Summoner': jj('Summoner'), 'Bishop': jj('Bishop'), 'Templar': jj('Templar'), 'Sage': jj('Sage')}
WHO = {'original': ['Illusionist', 'Time Mage', 'Summoner', 'Bishop', 'Templar', 'Sage'], 'Phantasm poder 30': ['Illusionist'], 'Phantasm MP 24': ['Illusionist'], 'Phantasm poder 30 e MP 24': ['Illusionist'],
       'Haste MP 16': ['Time Mage'], 'Haste AP 100': ['Time Mage'], 'Haste MP 16 e AP 100': ['Time Mage'], 'Unicorn e Cura AP 100': ['Summoner', 'Bishop'],
       'piso de velocidade (+10 base, +0,3 cresc.)': ['Illusionist', 'Templar', 'Sage', 'Bishop', 'Summoner'], 'pacote de correções': ['Illusionist', 'Time Mage', 'Summoner', 'Bishop', 'Templar', 'Sage']}
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    T = [(lab, ALLV[lab], i, lv, n, 211) for lab, who in WHO.items() for c in who for i in CL[c] for lv in (10, 25, 45)]
    print(len(T), 'tarefas', flush=True)
    with mp.Pool(4) as p: R = p.map(exp3.strat_task, T, chunksize=2)
    json.dump(R, open('exp3_fix_raw.json', 'w'), ensure_ascii=False); print('feito', flush=True)
