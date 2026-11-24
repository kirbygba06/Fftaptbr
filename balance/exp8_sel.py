import os, json, sys
os.environ.setdefault('PROG', '2'); os.environ.setdefault('APB', '40'); os.environ.setdefault('SEC', '1')
import exp8_round as R, exp4_teams_specs as SP
r1 = json.load(open('exp8_patched_r1.json'))['mods']
SEL = ['Earth Render', 'Far Fist', 'Air Render', 'Body Slam', 'Tremor', 'Whirlwind', 'Heavy Dust', 'Sliprain', 'Shining Air', 'White Flame', 'Holy', 'Water', 'Aero', 'Chocobo Rush', 'Cuisine',
       'Silenshot', 'Blindshot', 'Sheep Count', 'Toad', 'Last Breath', 'Nightmare', 'Ague', 'Carbuncle', 'Tail Wag', 'Quicken']
mods = {ab: r1[ab] for ab in SEL if ab in r1}
spec = dict(SP.SPECS['final3']); spec['mods'] = {**spec['mods'], **mods}
json.dump(dict(mods=mods), open('exp8_selected.json', 'w'), ensure_ascii=False)
print(len(mods), 'habilidades alteradas (seletivo, passo 1)', flush=True)
R.run_team_n('v1_sel', spec, {'25': 12000, '10': 4000, '45': 6000})
