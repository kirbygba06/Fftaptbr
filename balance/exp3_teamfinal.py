import sys, exp3, exp3_fix
spec = dict(base='ref2', mods={**{n: {'power': 30} for n in exp3.PHANT}, 'Haste': {'area': 'r1/v2'}}, ap={'Unicorn': 100, 'Cura': 100})
exp3.run_team('final', spec, int(sys.argv[1]) if len(sys.argv) > 1 else 12000, 101)
