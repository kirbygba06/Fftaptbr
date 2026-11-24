# -*- coding: utf-8 -*-
"""Quais habilidades a IA do simulador v2 realmente usa, por classe e nível; marca as nunca usadas e as dominantes."""
import collections, random, json, sim, sim2
scn = sim.load(); g = sim.gear(scn['items']); J = scn['jobs']
use = collections.defaultdict(collections.Counter); turns = collections.Counter(); wins = collections.defaultdict(lambda: [0, 0])
orig = sim2.pick_action
def pa(u, own, foes, rng):
    r = orig(u, own, foes, rng)
    if r[1] is not None: use[(u['name'], u['lvl'])][r[1].name] += 1
    turns[(u['name'], u['lvl'])] += 1
    return r
sim2.pick_action = pa
rng = random.Random(4)
for lv in (10, 25, 45):
    for _ in range(1500):
        ta = rng.sample(J, 3); tb = rng.sample(J, 3)
        A = [sim2.mk(j, lv, g, scn['abil']) for j in ta]; B = [sim2.mk(j, lv, g, scn['abil']) for j in tb]
        r, _a = sim2.battle(A, B, rng)
        for j in ta: wins[(j['name'], lv)][0] += r; wins[(j['name'], lv)][1] += 1
        for j in tb: wins[(j['name'], lv)][0] += 1 - r; wins[(j['name'], lv)][1] += 1
out = {}
for cls in sorted({j['name'] for j in J}):
    for lv in (10, 25, 45):
        kit, _s = sim2.kit_for(cls, sim2.cap_for(lv)); names = [a.name for a in kit]
        c = use[(cls, lv)]; tot = max(1, turns[(cls, lv)])
        w = wins[(cls, lv)]
        out[f'{cls}|{lv}'] = dict(win=round(w[0] / max(1, w[1]), 3), share={k: round(v / tot, 3) for k, v in c.most_common()}, unused=[n for n in names if c[n] == 0])
json.dump(out, open('ability_usage.json', 'w'), ensure_ascii=False, indent=1)
# resumo: nunca usadas em nenhum nível
never = collections.defaultdict(list)
for cls in sorted({j['name'] for j in J}):
    kit, _s = sim2.kit_for(cls, 999)
    for a in kit:
        if all(a.name in out[f'{cls}|{lv}']['unused'] or a.ap_hidden for lv in (45,)) if False else all(a.name not in out[f'{cls}|{lv}']['share'] for lv in (25, 45)):
            never[cls].append(a.name)
print('NUNCA escolhidas (níveis 25 e 45):'); [print(' ', c, v) for c, v in never.items() if v]
print('\nDOMINANTES (>35% das ações da classe no nível 45):')
for key, d in out.items():
    cls, lv = key.split('|')
    if lv == '45':
        top = [(k, v) for k, v in d['share'].items() if v >= 0.35 and k != 'Fight']
        if top: print(' ', cls, top, 'vitória', d['win'])
