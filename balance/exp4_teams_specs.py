import exp4_classes as C
mods = {'Nurse': {'power': 45}, 'Saint Cross': {'power': 45, 'mp': 18}, 'Holy Blade': {'mp': 24}, 'First Aid': {'power': 40}, **C.T2, **C.T3, **{x: {'power': 40} for x in ('Fire Whip', 'Shining Air', 'Heavy Dust', 'Sliprain')}}
SPECS = {'orig': dict(base='orig'), 'r2': dict(base='ref2'),
         'final3': C.sp(mods=mods, kscale=C.kb(['Assassin', 'Fencer', 'Soldier', 'Mog Knight', 'Juggler', 'Red Mage'], 1.08))}
