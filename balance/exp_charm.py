# -*- coding: utf-8 -*-
"""Quanto muda o jogo se Charm durar menos? (duração natural; Charm já termina ao receber dano)"""
import json, random, sys, statistics as S, multiprocessing as mp
import sim, sim2
scn0 = sim.load(); J = scn0['jobs']; G = sim.gear(scn0['items'])
def jid(name, race): return next(j for j in J if j['name'] == name and j['race'] == race)
FOC = [jid('Gunner', 5), jid('Archer', 1), jid('Archer', 4)]
SHOTS = {s: 6 for s in ('Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot')}
def task(a):
    dur, shots, j, lv, n, seed = a
    sim2.DUR['Charm'] = dur; sim2.P['OBS'] = 0; sim2.reset_stats(); saved = {}
    if shots:
        for ab in sim2.CAT.values():
            if ab.name in SHOTS: saved[ab.name] = ab.mp; ab.mp = SHOTS[ab.name]
    rng = random.Random(seed); random.seed(seed + 7); w = 0
    for _ in range(n):
        o = rng.sample([x for x in J if x is not j], 5)
        A = [sim2.mk(j, lv, G, scn0['abil'])] + [sim2.mk(x, lv, G, scn0['abil']) for x in o[:2]]; B = [sim2.mk(x, lv, G, scn0['abil']) for x in o[2:]]
        r, _a = sim2.battle(A, B, rng); w += r
    for ab in sim2.CAT.values():
        if ab.name in saved: ab.mp = saved[ab.name]
    return dict(dur=dur, shots=shots, cls=f"{j['name']}/{j['race']}", lv=lv, win=w / n, denied=sum(v for k, v in sim2.STATS['denied'].items() if k in ('Charmshot', 'Cupid')))
if __name__ == '__main__':
    T = [(d, s, j, lv, 1500, 31) for d in (4, 3, 2, 1) for s in (0, 1) for j in FOC for lv in (25, 45)]
    with mp.Pool(3) as p: R = p.map(task, T, chunksize=1)
    json.dump(R, open('exp_charm_raw.json', 'w'), ensure_ascii=False); print('feito')
