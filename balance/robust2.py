# -*- coding: utf-8 -*-
"""Robustez do v2: troca suposições (duração/valor de status, friendly fire, alcance, tamanho do time) e compara cenários."""
import json, sys, statistics as S, sim, sim2, f1
scn0 = sim.load(); k1 = {int(a): b for a, b in json.load(open('f1_k.json')).items()}
SCN = {'ATUAL': scn0, 'F1 v1 (ajuste do modelo simples)': f1.build(scn0, k1)}
k2 = {int(a): b for a, b in json.load(open('f1v2_k.json')).items()}; SCN['F1 v2 (só atributos/itens)'] = f1.build(scn0, k2)
k3 = {int(a): b for a, b in json.load(open('f1v3_k.json')).items()}; SCN['F1 v3 (+ preço de MP dos status)'] = f1.build(scn0, k3, mods=True)
CASES = [('padrão', {}, 3), ('status duram metade', dict(DURM=0.5), 3), ('status duram o dobro', dict(DURM=2.0), 3), ('IA valoriza status ×0,5', dict(SV=0.5), 3),
         ('IA valoriza status ×1,5', dict(SV=1.5), 3), ('fogo amigo 0', dict(FF=0.0), 3), ('fogo amigo 0,5', dict(FF=0.5), 3), ('alcance: mover pesa mais', dict(REACH_MOV=0.1), 3),
         ('time de 4', {}, 4)]
if __name__ == '__main__':
    only = sys.argv[2:] or None
    print('| suposição do simulador | ' + ' | '.join(SCN) + ' |\n|---|' + '---|' * len(SCN))
    for name, cfg, size in CASES:
        old = {a: sim2.P[a] for a in cfg}; sim2.P.update(cfg); out = []
        for lab, scn in SCN.items():
            r, _ = sim2.run(scn, levels=(25, 45), n=800, seed=17, size=size)
            v = [S.mean(r[lv][j['id']] for lv in (25, 45)) for j in scn['jobs']]
            out.append(f'{min(v):.2f}–{max(v):.2f} (σ {S.pstdev(v):.3f})')
        sim2.P.update(old); print(f'| {name} | ' + ' | '.join(out) + ' |', flush=True)
