import sys, exp3, exp4_classes as C
from exp3 import jj
nome = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
if nome == 'final2': spec = C.sp()
if nome == 'final3':
    mods = {'Nurse': {'power': 45}, 'Saint Cross': {'power': 45, 'mp': 18}, 'Holy Blade': {'mp': 24}, 'First Aid': {'power': 40}, **C.T2, **C.T3,
            **{x: {'power': 40} for x in ('Fire Whip', 'Shining Air', 'Heavy Dust', 'Sliprain')}}
    spec = C.sp(mods=mods, kscale=C.kb(['Assassin', 'Fencer', 'Soldier', 'Mog Knight', 'Juggler', 'Red Mage'], 1.08))
exp3.run_team(nome, spec, n, 101)
