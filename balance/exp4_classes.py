# -*- coding: utf-8 -*-
"""Melhorias nas classes 16–38 do ranking. Base = pacote final com o Illusionist recalibrado (orçamento ×0,8 sobre o R2).
Estratificado 5 contra 5, mapa variável; a classe sempre no time A. Variantes de dado isoladas, depois combinadas."""
import json, sys, multiprocessing as mp
import exp3
from exp3 import jj
ILL = {i: 0.8 for i in jj('Illusionist')}
def sp(**k):
    d = dict(base='final', kscale=dict(ILL)); ks = k.pop('kscale', None)
    if ks: d['kscale'].update(ks)
    d.update(k); return d
def kb(names, f): return {i: f for n in names for i in jj(n)}
T2 = {n: {'mp': 14, 'power': 46} for n in ('Fira', 'Thundara', 'Blizzara')}; T3 = {n: {'mp': 30, 'power': 68} for n in ('Firaga', 'Thundaga', 'Blizzaga')}
BREAK = {'Powerbreak': {'eff': ['AType, Default, Inflict WAtk DOWN/WDef DOWN']}, 'Mindbreak': {'eff': ['AType, Default, Inflict MPow DOWN/MRes DOWN']}}
V = {  # nome: (spec, [classes avaliadas])
 'magias tier 2 e 3 (46/14, 68/30)': (sp(mods={**T2, **T3}), ['Black Mage']),
 'Paladin: Nurse 45': (sp(mods={'Nurse': {'power': 45}}), ['Paladin']),
 'Paladin: Saint Cross 45 e MP 18': (sp(mods={'Saint Cross': {'power': 45, 'mp': 18}}), ['Paladin']),
 'Paladin: Holy Blade MP 24': (sp(mods={'Holy Blade': {'mp': 24}}), ['Paladin']),
 'Paladin: os três': (sp(mods={'Nurse': {'power': 45}, 'Saint Cross': {'power': 45, 'mp': 18}, 'Holy Blade': {'mp': 24}}), ['Paladin']),
 'Powerbreak e Mindbreak = debuff duplo (ATK+DEF, PM+RM)': (sp(mods=BREAK), ['Soldier', 'Warrior']),
 'First Aid poder 40': (sp(mods={'First Aid': {'power': 40}}), ['Soldier', 'Warrior']),
 'Mog Aid poder 50': (sp(mods={'Mog Aid': {'power': 50}}), ['Mog Knight']),
 'Elementalist: Fire Whip, Shining Air, Heavy Dust, Sliprain poder 40': (sp(mods={n: {'power': 40} for n in ('Fire Whip', 'Shining Air', 'Heavy Dust', 'Sliprain')}), ['Elementalist']),
 'Juggler: Dagger 42, Firebomb 45': (sp(mods={'Dagger': {'power': 42}, 'Firebomb': {'power': 45}}), ['Juggler']),
 'Cupid MP 4': (sp(mods={'Cupid': {'mp': 4}}), ['Archer']),
 'Cupid MP 0 (reverter)': (sp(mods={'Cupid': {'mp': 0}}), ['Archer']),
 'Stop em área (raio 1)': (sp(mods={'Stop': {'area': 'r1/v2'}}), ['Time Mage']),
 'Frogsong MP 12': (sp(mods={'Frogsong': {'mp': 12}}), ['Animist']),
 'orçamento +8% (classes em tier C)': (sp(kscale=kb(['Assassin', 'Fencer', 'Soldier', 'Mog Knight', 'Red Mage', 'Juggler', 'Paladin', 'Black Mage'], 1.08)), ['Assassin', 'Fencer', 'Soldier', 'Mog Knight', 'Red Mage', 'Juggler', 'Paladin', 'Black Mage']),
}
CLASSES = ['Black Mage', 'Archer', 'Elementalist', 'Warrior', 'Sage', 'Alchemist', 'Sniper', 'Ninja', 'Animist', 'Paladin', 'Fencer', 'Juggler', 'Assassin', 'Red Mage', 'Soldier', 'Mog Knight', 'Time Mage']
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    T = [('base', sp(), i, lv, n, 711) for c in CLASSES for i in jj(c) for lv in (10, 25, 45)]
    for lab, (spec, who) in V.items():
        T += [(lab, spec, i, lv, n, 711) for c in who for i in jj(c) for lv in (10, 25, 45)]
    print(len(T), 'tarefas', flush=True)
    with mp.Pool(4) as p: R = p.map(exp3.strat_task, T, chunksize=3)
    json.dump(R, open('exp4_classes_raw.json', 'w'), ensure_ascii=False); print('feito', flush=True)
