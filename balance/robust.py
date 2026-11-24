# -*- coding: utf-8 -*-
"""Teste fora da amostra: o F1 foi ajustado com a configuração padrão; aqui muda-se o simulador (área, tamanho de time, mira, nível, sem cura)."""
import json, statistics as S, sim, f1
scn0 = sim.load(); k = {int(a): b for a, b in json.load(open('f1_k.json')).items()}; scn1 = f1.build(scn0, k)
CASES = [('padrão (n=3, níveis 10/25/45)', dict(), (10, 25, 45), 3), ('níveis não ajustados 18 e 35', dict(), (18, 35), 3), ('time de 2', dict(), (25, 45), 2), ('time de 4', dict(), (25, 45), 4),
         ('mira aleatória', dict(TARGET='random'), (25, 45), 3), ('magia sem área', dict(AOE=0.0), (25, 45), 3), ('magia com muita área', dict(AOE=0.9), (25, 45), 3), ('sem curas', dict(HEALON=False), (25, 45), 3)]
print('| cenário do simulador | ATUAL min–max (σ) | F1 min–max (σ) |\n|---|---|---|')
for name, cfg, lvs, size in CASES:
    old = {a: getattr(sim, a) for a in cfg}
    for a, v in cfg.items(): setattr(sim, a, v)
    out = []
    for scn in (scn0, scn1):
        r = sim.run(scn, levels=lvs, n=2500, seed=11, size=size)
        v = [S.mean(r[lv][j['id']] for lv in lvs) for j in scn['jobs']]
        v2 = [S.mean(r[lv][j['id']] for lv in lvs) for j in scn['jobs'] if sim.PROFILE.get(j['name']) in (sim.PHYS, sim.MAGE)]
        out.append(f'{min(v):.2f}–{max(v):.2f} (σ {S.pstdev(v):.3f}) · só dano: {min(v2):.2f}–{max(v2):.2f} (σ {S.pstdev(v2):.3f})')
    for a, v in old.items(): setattr(sim, a, v)
    print(f'| {name} | {out[0]} | {out[1]} |', flush=True)
