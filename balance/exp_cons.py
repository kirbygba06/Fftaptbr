# -*- coding: utf-8 -*-
"""Experimentos conservadores (um parâmetro por vez): custo de MP das habilidades prioritárias, comparado ao original, níveis 10/25/45.
Amostragem estratificada: a classe que usa a habilidade sempre está no time A; os demais 5 lugares são aleatórios."""
import json, random, sys, statistics as S, collections, multiprocessing as mp
import sim, sim2
scn0 = sim.load(); J = scn0['jobs']; G = sim.gear(scn0['items'])
def jid(name, race): return next(j for j in J if j['name'] == name and j['race'] == race)
CLS = {'Rockseal': [jid('Assassin', 4)], 'Charmshot': [jid('Gunner', 5)], 'Cupid': [jid('Archer', 1), jid('Archer', 4)], 'Fire Veil': [jid('Ninja', 1)],
       'Death Sickle': [jid('Sniper', 4)], 'Checkmate': [jid('Fencer', 4)]}
BASEMP = {'Rockseal': 32, 'Charmshot': 0, 'Cupid': 0, 'Fire Veil': 4, 'Death Sickle': 0, 'Checkmate': 0}
STEPS = {'Charmshot': (4, 8, 12), 'Cupid': (4, 8, 12), 'Fire Veil': (8, 12, 16), 'Death Sickle': (8, 12, 16), 'Checkmate': (8, 12, 16)}
LEVELS = (10, 25, 45)
def task(args):
    variant, ab, mods, disable, obs, j, lv, n, seed = args
    sim2.P['OBS'] = obs; sim2.reset_stats()
    scn = dict(scn0); scn['mods'] = mods; scn['disable'] = disable
    rng = random.Random(seed); sim2.DISABLE.clear(); sim2.DISABLE.update(disable)
    saved = {}
    for a in sim2.CAT.values():
        if a.name in mods: saved[a.name] = a.mp; a.mp = mods[a.name]
    random.seed(seed + 7); w = 0; acts = []
    for _ in range(n):
        others = rng.sample([x for x in J if x is not j], 5)
        A = [sim2.mk(j, lv, G, scn0['abil'])] + [sim2.mk(x, lv, G, scn0['abil']) for x in others[:2]]
        B = [sim2.mk(x, lv, G, scn0['abil']) for x in others[2:]]
        r, a = sim2.battle(A, B, rng); w += r; acts.append(a)
    for a in sim2.CAT.values():
        if a.name in saved: a.mp = saved[a.name]
    sim2.DISABLE.clear()
    st = sim2.STATS; cls = j['name']
    uses_ab = sum(v for (c, l, nme), v in st['use'].items() if nme == ab); my_acts = max(1, st['acts'][(cls, lv)])
    my_uses = st['use'][(cls, lv, ab)]; att = st['att'][ab]; succ = st['succ'][ab]
    res = dict(variant=variant, ab=ab, obs=obs, cls=f"{cls}/{j['race']}", lv=lv, win=w / n, share=my_uses / my_acts, att=att, succ=succ,
               impact=st['impact'][ab] / max(1, uses_ab), denied=st['denied'][ab] / max(1, uses_ab), acts=S.mean(acts),
               top=[(k[2], round(v / my_acts, 3)) for k, v in sorted(st['use'].items(), key=lambda kv: -kv[1]) if k[0] == cls and k[1] == lv][:4])
    return res
def build_tasks(n, seed=11):
    T = []
    for obs in (0, 1):
        for ab, jl in CLS.items():
            variants = [('original', {}, set())]
            variants.append((f'sem {ab}', {}, {ab}))
            if ab in STEPS:
                for m in STEPS[ab]: variants.append((f'{ab} MP {m}', {ab: m}, set()))
            for name, mods, dis in variants:
                for j in jl:
                    for lv in LEVELS: T.append((name, ab, mods, dis, obs, j, lv, n, seed))
    return T
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    T = build_tasks(n); print(len(T), 'tarefas', flush=True)
    with mp.Pool(4) as pool: R = pool.map(task, T, chunksize=2)
    json.dump(R, open('exp_cons_raw.json', 'w'), ensure_ascii=False)
    print('feito')
