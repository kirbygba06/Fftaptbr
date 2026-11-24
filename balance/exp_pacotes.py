# -*- coding: utf-8 -*-
"""Pacotes conservadores de ajuste (só custo de MP), comparados ao original nos níveis 10/25/45, população inteira."""
import json, random, sys, statistics as S, collections, multiprocessing as mp
import sim, sim2
scn0 = sim.load(); J = scn0['jobs']; G = sim.gear(scn0['items'])
VEIL = ['Wood Veil', 'Fire Veil', 'Earth Veil', 'Metal Veil', 'Water Veil']
SHOTS = ['Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot']
PACK = {'original': {}, 'A: só Cupid MP 8': {'Cupid': 8}, 'B: Cupid 8 + Veils 8': dict({'Cupid': 8}, **{v: 8 for v in VEIL}),
        'C: B + tiros de status MP 6': dict({'Cupid': 8}, **{v: 8 for v in VEIL}, **{s: 6 for s in SHOTS}),
        'D: B + tiros de status MP 10': dict({'Cupid': 8}, **{v: 8 for v in VEIL}, **{s: 10 for s in SHOTS})}
HARM = sim2.HARM
def category(a):
    if a.name == 'Fight': return 'dano'
    kinds = [e['kind'] for e in a.eff]
    if any(e['kind'] == 'status' and any(n in HARM for n in e['names']) for e in a.eff) and not any(k in ('dmg', 'hpfrac', 'flat') for k in kinds): return 'controle'
    if any(e['kind'] == 'status' and any(n in HARM for n in e['names']) for e in a.eff): return 'dano+controle'
    if any(k in ('heal', 'healfull', 'revive', 'esuna') for k in kinds) or any(e['kind'] == 'status' for e in a.eff): return 'apoio'
    return 'dano'
CAT = {a.name: category(a) for a in sim2.CAT.values()}; CAT['Fight'] = 'dano'
def task(args):
    name, mods, lv, n, seed, obs = args
    sim2.P['OBS'] = obs; sim2.reset_stats(); saved = {}
    for a in sim2.CAT.values():
        if a.name in mods: saved[a.name] = a.mp; a.mp = mods[a.name]
    rng = random.Random(seed); random.seed(seed + 7); W = {j['id']: [0, 0] for j in J}; ac = []
    for _ in range(n):
        ta = rng.sample(J, 3); tb = rng.sample(J, 3)
        A = [sim2.mk(j, lv, G, scn0['abil']) for j in ta]; B = [sim2.mk(j, lv, G, scn0['abil']) for j in tb]
        r, a = sim2.battle(A, B, rng); ac.append(a)
        for j in ta: W[j['id']][0] += r; W[j['id']][1] += 1
        for j in tb: W[j['id']][0] += 1 - r; W[j['id']][1] += 1
    for a in sim2.CAT.values():
        if a.name in saved: a.mp = saved[a.name]
    st = sim2.STATS; roles = collections.defaultdict(collections.Counter)
    for (c, l, ab), v in st['use'].items(): roles[c][CAT.get(ab, 'dano')] += v
    return dict(name=name, lv=lv, obs=obs, win={j['id']: W[j['id']][0] / max(1, W[j['id']][1]) for j in J}, acts=S.mean(ac),
                roles={c: dict(v) for c, v in roles.items()}, use={f'{k[0]}|{k[2]}': v for k, v in st['use'].items()}, att=dict(st['att']), succ=dict(st['succ']),
                impact=dict(st['impact']), denied=dict(st['denied']), n_act={f'{k[0]}': v for k, v in st['acts'].items()})
PACK2 = {'E: Cupid 8 + tiros de status MP 6': dict({'Cupid': 8}, **{s_: 6 for s_ in SHOTS}), 'F: só tiros de status MP 6': {s_: 6 for s_ in SHOTS}}
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    extra = len(sys.argv) > 2 and sys.argv[2] == 'extra'
    if extra:
        T = [(nm, m, lv, n, 21, obs) for obs in (0, 1) for nm, m in PACK2.items() for lv in (10, 25, 45)] + [('original (outra semente)', {}, lv, n, 22, obs) for obs in (0, 1) for lv in (10, 25, 45)]
    else:
        T = [(nm, m, lv, n, 21, obs) for obs in (0, 1) for nm, m in PACK.items() for lv in (10, 25, 45)]
    print(len(T), 'tarefas', flush=True)
    with mp.Pool(4) as pool: R = pool.map(task, T, chunksize=1)
    json.dump(R, open('exp_pacotes_raw2.json' if extra else 'exp_pacotes_raw.json', 'w'), ensure_ascii=False); print('feito')
