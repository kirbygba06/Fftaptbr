# -*- coding: utf-8 -*-
"""Rodada 2: evidências para a tabela de propostas. Cada experimento = original/isolado/combinado, mesmas sementes."""
import os, json, sys, random, statistics as S, collections, multiprocessing as mp
import sim, sim2, f1
from exp_pacotes import CAT as ABCAT
scn0 = sim.load(); G0 = sim.gear(scn0['items']); J = scn0['jobs']
k4 = {int(a): b for a, b in json.load(open('f1v4_k.json')).items()}
k5 = {int(a): b for a, b in json.load(open('f1v5_k.json')).items()} if os.path.exists('f1v5_k.json') else k4
AB = {**{s: 6 for s in ('Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot')}, 'Cupid': 8}
def scen(spec):
    kind = spec['base']
    if kind == 'orig': s = dict(scn0)
    elif kind == 'ref2': s = f1.build(scn0, k5, mods=AB, atk_scale=1.12, **spec.get('build', {}))
    else: s = f1.build(scn0, k4, mods=AB, atk_scale=1.12, **spec.get('build', {}))
    if spec.get('mods'): s['mods'] = {**(s.get('mods') or {}), **spec['mods']}
    if spec.get('disable'): s['disable'] = set(spec['disable'])
    return s
def setparams(p):
    sim2.P.update({'HASTE': 2.0, 'DS2': 1.0, 'NO_DS': 0, 'NO_DC': 0, 'OBS': 0, 'DURM': 1.0, 'SV': 1.0, 'FF': 0.25}); sim2.DUR['Charm'] = 4
    for k, v in (p or {}).items():
        if k == 'CHARM': sim2.DUR['Charm'] = v
        else: sim2.P[k] = v
def gtask(a):
    label, spec, params, lv, n, seed = a
    setparams(params); sim2.reset_stats(); s = scen(spec)
    r, p = sim2.run(s, levels=(lv,), n=n, seed=seed); st = sim2.STATS
    roles = collections.defaultdict(collections.Counter)
    for (c, l, ab), v in st['use'].items(): roles[c][ABCAT.get(ab, 'dano')] += v
    mpu = {c: st['mp'][(c, l)] / max(1, st['mpn'][(c, l)]) for (c, l) in st['mp']}
    return dict(label=label, lv=lv, win={str(k): v for k, v in r[lv].items()}, acts=p[lv], roles={c: dict(v) for c, v in roles.items()},
                use={f'{k[0]}|{k[2]}': v for k, v in st['use'].items()}, att=dict(st['att']), succ=dict(st['succ']), impact=dict(st['impact']), denied=dict(st['denied']),
                n_act={c: v for (c, l), v in st['acts'].items()}, mp_unit=mpu)
def jid(name, race=None): return next(j for j in J if j['name'] == name and (race is None or j['race'] == race))
def stask(a):
    label, spec, params, j_id, ab, mode, lv, n, seed = a
    setparams(params); sim2.reset_stats(); s = scen(spec); j = next(x for x in J if x['id'] == j_id)
    sim2.FORCE.clear(); dis = set(s.get('disable', ()))
    if mode == 'ablacao': dis.add(ab)
    if mode == 'forcado': sim2.FORCE[j_id] = ab
    sim2.DISABLE.clear(); sim2.DISABLE.update(dis)
    saved = {}
    for x in sim2.CAT.values():
        if x.name in (s.get('mods') or {}):
            m = s['mods'][x.name]; saved[x.name] = (x.mp, x.power)
            if isinstance(m, dict): x.mp = m.get('mp', x.mp); x.power = m.get('power', x.power)
            else: x.mp = m
    g = sim.gear(s['items']); rng = random.Random(seed); random.seed(seed + 7); w = 0; ac = []
    for _ in range(n):
        o = rng.sample([x for x in s['jobs'] if x['id'] != j_id], 5)
        A = [sim2.mk(j, lv, g, s['abil'])] + [sim2.mk(x, lv, g, s['abil']) for x in o[:2]]; B = [sim2.mk(x, lv, g, s['abil']) for x in o[2:]]
        r, a_ = sim2.battle(A, B, rng); w += r; ac.append(a_)
    for x in sim2.CAT.values():
        if x.name in saved: x.mp, x.power = saved[x.name]
    sim2.DISABLE.clear(); sim2.FORCE.clear(); st = sim2.STATS; cls = j['name']
    uses = sum(v for (c, l, nme), v in st['use'].items() if nme == ab); acts = max(1, st['acts'][(cls, lv)])
    fu = sum(v for (c, l, nme), v in st['use'].items() if nme == 'Fight' and c == cls)
    return dict(label=label, ab=ab, mode=mode, cls=f"{cls}/{j['race']}", lv=lv, win=w / n, acts=S.mean(ac), share=st['use'][(cls, lv, ab)] / acts, uses=uses,
                ev=st['ev'][ab] / max(1, st['evn'][ab]), ev_fight=st['ev']['Fight'] / max(1, st['evn']['Fight']), impact=st['impact'][ab] / max(1, uses), denied=st['denied'][ab] / max(1, uses),
                att=st['att'][ab], succ=st['succ'][ab], impact_fight=st['impact']['Fight'] / max(1, sum(v for (c, l, nme), v in st['use'].items() if nme == 'Fight')))
def run_pool(fn, T, name):
    with mp.Pool(4) as p: R = p.map(fn, T, chunksize=1)
    json.dump(R, open(f'exp2_{name}.json', 'w'), ensure_ascii=False); print(name, 'feito', len(R), flush=True)
LV = (10, 25, 45)
if __name__ == '__main__':
    which = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    ORIG = dict(base='orig'); REF = dict(base='ref')
    if which == 'base':
        T = [(f'{b}', sp, {}, lv, n, 61) for b, sp in (('original', ORIG), ('referencia', REF)) for lv in (10, 25, 45, 50)]
        run_pool(gtask, T, 'base')
    if which == 'base2':
        T = [('referencia2', dict(base='ref2'), {}, lv, n, 61) for lv in (10, 25, 45, 50)]
        run_pool(gtask, T, 'base2')
    if which == 'velocidade':
        T = [(f'ref spd {sp}', dict(base='ref', build=dict(spd=sp)), {}, lv, n, 61) for sp in ((0.5, 0.35), (0.35, 0.2)) for lv in LV]
        run_pool(gtask, T, 'velocidade')
    if which == 'haste':
        T = [(f'haste {h}', ORIG, {'HASTE': h}, lv, n, 61) for h in (1.5, 1.25) for lv in LV]
        run_pool(gtask, T, 'haste')
    if which == 'capstones':
        T = [('DS2 0.65', ORIG, {'DS2': 0.65}, 50, n, 61), ('sem DS', ORIG, {'NO_DS': 1}, 50, n, 61), ('sem Doublecast', ORIG, {'NO_DC': 1}, 50, n, 61),
             ('DS2 0.65 sem Quicken', dict(base='orig', disable=['Quicken']), {'DS2': 0.65}, 50, n, 61),
             ('sem Quicken', dict(base='orig', disable=['Quicken']), {}, 45, n, 61), ('sem Quicken', dict(base='orig', disable=['Quicken']), {}, 50, n, 61), ('sem Quicken', dict(base='orig', disable=['Quicken']), {}, 25, n, 61)]
        run_pool(gtask, T, 'capstones')
    if which == 'magias':
        T2 = {n_: {'mp': 14, 'power': 46} for n_ in ('Fira', 'Thundara', 'Blizzara')}; T3 = {n_: {'mp': 30, 'power': 68} for n_ in ('Firaga', 'Thundaga', 'Blizzaga')}
        V = [('tier2 46/14', T2), ('tier3 68/30', T3), ('tier2+tier3', {**T2, **T3})]
        T = [(l_, dict(base='orig', mods=m_), {}, lv, n, 61) for l_, m_ in V for lv in (25, 45)]
        run_pool(gtask, T, 'magias')
    if which == 'buffs':
        L = [('Soldier', 1, ['Powerbreak', 'Mindbreak', 'Magicbreak']), ('Warrior', 2, ['Powerbreak', 'Mindbreak', 'Magicbreak']), ('Fighter', 1, ['Wild Swing']), ('Gladiator', 2, ['Wild Swing']),
             ('White Monk', 2, ['Whirlwind', 'Holy Sign']), ('Paladin', 1, ['Saint Cross']), ('Defender', 2, ['Tremor', 'Expert Guard']), ('Fencer', 4, ['Swallowtail', 'Manastrike']),
             ('Bishop', 2, ['Dispel', 'Barrier', 'Water', 'Aero']), ('Summoner', 4, ['Carbuncle']), ('Alchemist', 3, ['Rasp']), ('Templar', 2, ['Rasp'])]
        T = []
        for cn, rc, abs_ in L:
            jid_ = jid(cn, rc)['id']
            for ab in abs_:
                for mode in ('normal', 'ablacao', 'forcado'):
                    for lv in (25, 45): T.append((f'{cn} {ab}', ORIG, {}, jid_, ab, mode, lv, n, 71))
        run_pool(stask, T, 'buffs')
