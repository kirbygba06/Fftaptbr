# -*- coding: utf-8 -*-
"""Robustez do pacote completo: troca as suposições do simulador e compara original x pacote."""
import json, statistics as S, multiprocessing as mp
import sim, sim2, f1
scn0 = sim.load(); k4 = {int(a): b for a, b in json.load(open('f1v4_k.json')).items()}
AB = {**{s: 6 for s in ('Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot')}, 'Cupid': 8}
S1 = f1.build(scn0, k4, mods=AB, atk_scale=1.12)
CASES = [('padrão', {}, 3), ('status duram metade', dict(DURM=0.5), 3), ('status duram o dobro', dict(DURM=2.0), 3), ('IA valoriza status ×0,5', dict(SV=0.5), 3), ('IA valoriza status ×1,5', dict(SV=1.5), 3),
         ('fogo amigo 0', dict(FF=0.0), 3), ('fogo amigo 0,5', dict(FF=0.5), 3), ('mover pesa mais no alcance', dict(REACH_MOV=0.1), 3), ('imunidade a status dobrada', dict(IMM={10: 0.0, 25: 0.2, 45: 0.5}), 3),
         ('precisão registrada (modo B)', dict(OBS=1), 3), ('times de 4', {}, 4)]
def task(a):
    ci, which = a; name, cfg, size = CASES[ci]; sim2.P.update(cfg)
    s = scn0 if which == 0 else S1
    r, _ = sim2.run(s, levels=(25, 45), n=900, seed=51, size=size)
    v = [S.mean(r[lv][j['id']] for lv in (25, 45)) for j in s['jobs']]
    return ci, which, min(v), max(v), S.pstdev(v), sum(1 for x in v if x < .4 or x > .6)
if __name__ == '__main__':
    with mp.Pool(4) as p: R = p.map(task, [(i, w) for i in range(len(CASES)) for w in (0, 1)], chunksize=1)
    out = ['| suposição do simulador | original | pacote completo |\n|---|---|---|']
    for i, (name, _, _) in enumerate(CASES):
        a = next(r for r in R if r[0] == i and r[1] == 0); b = next(r for r in R if r[0] == i and r[1] == 1)
        out.append(f'| {name} | {a[2] * 100:.0f}–{a[3] * 100:.0f}% (σ {a[4]:.3f}, {a[5]} fora de 40–60%) | {b[2] * 100:.0f}–{b[3] * 100:.0f}% (σ {b[4]:.3f}, {b[5]} fora) |')
    open('robust_final_result.md', 'w').write('\n'.join(out)); print('\n'.join(out))
