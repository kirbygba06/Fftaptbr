# -*- coding: utf-8 -*-
"""Habilidades fracas de alvo único passam a atingir área (raio 1). Com 25% de chance de cada alvo extra de um efeito benéfico ser um inimigo."""
import os, json, sys
os.environ.setdefault('PROG', '2'); os.environ.setdefault('APB', '40'); os.environ.setdefault('SEC', '1')
import exp8_round as R, exp4_teams_specs as SP
SUP = ['Defense', 'First Aid', 'Chakra', 'Mog Aid', 'Boost', 'Reflect', 'Barrier', 'Quicken', 'Earth Heal', 'Cuisine']
OFF = ['Air Render', 'Toad', 'Blind', 'Tail Wag', 'Provoke', 'Powerbreak', 'Mindbreak', 'Ague', 'Oblivion', 'Demi', 'Quarter', 'Downsize', 'Heavy Dust', 'Sliprain', 'Shining Air']
SELA = ['Toad', 'Provoke', 'Downsize', 'Ague', 'Oblivion', 'Heavy Dust', 'Sliprain', 'Shining Air', 'Cuisine', 'Quicken']
def merge(a, b):
    out = {k: (dict(v) if isinstance(v, dict) else {'mp': v}) for k, v in a.items()}
    for k, v in b.items(): out.setdefault(k, {}).update(v if isinstance(v, dict) else {'mp': v})
    return out
sel = json.load(open('exp8_selected.json'))['mods']
base_mods = merge(SP.SPECS['final3']['mods'], sel)
def spec_for(which):
    sp = dict(SP.SPECS['final3'])
    ar = {ab: {'area': 'r1/v2'} for ab in (SUP if which in ('sup', 'all') else []) + (OFF if which in ('off', 'all') else []) + (SELA if which == 'sel' else [])}
    sp['mods'] = merge(base_mods, ar); return sp
if __name__ == '__main__':
    which = sys.argv[1]; label = {'base': 'v2_base', 'sup': 'v2_area_sup', 'off': 'v2_area_off', 'all': 'v2_area_all', 'sel': 'v2_area_sel'}[which]
    R.run_team_n(label, spec_for(which), {'25': 12000, '10': 4000, '45': 6000})
