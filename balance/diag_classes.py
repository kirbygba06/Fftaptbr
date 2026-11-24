# -*- coding: utf-8 -*-
"""Decomposição: o que explica a taxa de vitória das classes que mais vencem? (atributos, velocidade, MP, status, kit inteiro)"""
import json, random, sys, statistics as S, multiprocessing as mp
import sim, sim2
scn0 = sim.load(); J = scn0['jobs']; G = sim.gear(scn0['items'])
def jid(name, race): return next(j for j in J if j['name'] == name and j['race'] == race)
FOCUS = [jid('Assassin', 4), jid('Gunner', 5), jid('Archer', 1), jid('Archer', 4), jid('Ninja', 1), jid('Sniper', 4), jid('Fencer', 4)]
LEVELS = (25, 45)
def field_mean(lv, key):
    return S.mean(sim2.mk(j, lv, G, scn0['abil'])[key] for j in J)
def is_status_ab(a):
    return any(e['kind'] == 'status' and any(n in sim2.HARM for n in e['names']) for e in a.eff)
XF = {'completo': lambda u, lv: None,
      'só Fight (sem habilidades)': lambda u, lv: u.__setitem__('abs', [sim2.FIGHT]),
      'sem habilidades de status': lambda u, lv: u.__setitem__('abs', [a for a in u['abs'] if not is_status_ab(a)]),
      'velocidade = média do campo': lambda u, lv: u.__setitem__('spd', FM[(lv, 'spd')]),
      'MP = média do campo': lambda u, lv: (u.__setitem__('mp', FM[(lv, 'mp')]), u.__setitem__('mp0', FM[(lv, 'mp')]))}
FM = {}
def task(args):
    xf, j, lv, n, seed = args
    sim2.P['OBS'] = 0; sim2.reset_stats(); rng = random.Random(seed); random.seed(seed + 7); w = 0; share = []
    for _ in range(n):
        others = rng.sample([x for x in J if x is not j], 5)
        me = sim2.mk(j, lv, G, scn0['abil']); XF[xf](me, lv)
        A = [me] + [sim2.mk(x, lv, G, scn0['abil']) for x in others[:2]]; B = [sim2.mk(x, lv, G, scn0['abil']) for x in others[2:]]
        r, a = sim2.battle(A, B, rng); w += r
    return dict(xf=xf, cls=f"{j['name']}/{j['race']}", lv=lv, win=w / n)
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1800
    for lv in LEVELS:
        for key in ('spd', 'mp'): FM[(lv, key)] = field_mean(lv, key)
    T = [(x, j, lv, n, 5) for x in XF for j in FOCUS for lv in LEVELS]
    with mp.Pool(4) as pool: R = pool.map(task, T, chunksize=2)
    json.dump(R, open('diag_classes_raw.json', 'w'), ensure_ascii=False)
    print('feito')
