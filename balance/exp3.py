# -*- coding: utf-8 -*-
"""Rodada 3: equipes de 5, mapa variável, efeito de cada classe na EQUIPE (regressão logística), uso das habilidades menos usadas
e testes de melhoria nas classes mais fracas. Tudo com os mesmos sorteios entre versões."""
import os, json, sys, random, copy, statistics as S, collections, multiprocessing as mp
import numpy as np
import sim, sim2, f1
scn0 = sim.load(); J = scn0['jobs']; JID = {j['id']: j for j in J}
k5 = {int(a): b for a, b in json.load(open('f1v5_k.json')).items()}
AB = {**{s: 6 for s in ('Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot')}, 'Cupid': 8}
PHANT = ['Prominence', 'Tempest', 'Freezeblink', 'Star Cross', 'Stardust', 'Deluge', 'Soil Evidence', 'Wild Tornado']
def jj(name, race=None): return [j['id'] for j in J if j['name'] == name and (race is None or j['race'] == race)]
SLOW = [i for n_ in ('Illusionist', 'Templar', 'Sage', 'Bishop', 'Summoner') for i in jj(n_)]
FINAL_MODS = {**{n: {'power': 30} for n in PHANT}, 'Haste': {'area': 'r1/v2'}}
FINAL_AP = {'Unicorn': 100, 'Cura': 100}
def spec_build(spec):
    base = spec.get('base', 'orig')
    if base == 'orig': s = dict(scn0)
    else:
        k = dict(k5)
        for i, f in (spec.get('kscale') or {}).items(): k[i] = k5[i] * f
        s = f1.build(scn0, k, mods=AB, atk_scale=1.12)
        if base == 'final': s['mods'] = {**(s.get('mods') or {}), **FINAL_MODS}; spec = dict(spec, ap={**FINAL_AP, **(spec.get('ap') or {})})
    s['jobs'] = copy.deepcopy(s['jobs'])
    for jid_, ch in (spec.get('jobmods') or {}).items():
        for j in s['jobs']:
            if j['id'] == jid_:
                for k_, v in ch.items(): j[k_] = (j[k_] + v[1] if v[0] == '+' else j[k_] * v[1]) if isinstance(v, tuple) else v
    s['mods'] = {**(s.get('mods') or {}), **(spec.get('mods') or {})}
    s['_ap'] = spec.get('ap') or {}
    return s
def apply_ctx(s, spec):
    saved = {}
    for a in sim2.CAT.values():
        if a.name in s['mods']:
            m = s['mods'][a.name]; saved[a.name] = (a.mp, a.power, a.area, a.eff)
            if isinstance(m, dict):
                a.mp = m.get('mp', a.mp); a.power = m.get('power', a.power); a.area = m.get('area', a.area)
                if 'eff' in m: a.eff = [x for x in (sim2.parse_effect(e) for e in m['eff']) if x]
            else: a.mp = m
    sim2.APMOD.clear(); sim2.APMOD.update(s.get('_ap') or spec.get('ap') or {}); sim2.DISABLE.clear(); sim2.DISABLE.update(spec.get('disable') or ())
    return saved
def undo_ctx(saved):
    for a in sim2.CAT.values():
        if a.name in saved: a.mp, a.power, a.area, a.eff = saved[a.name]
    sim2.APMOD.clear(); sim2.DISABLE.clear()
DUR0 = dict(sim2.DUR)
def setp():
    sim2.DUR.clear(); sim2.DUR.update(DUR0)
    sim2.P.update(dict(MAP=1, HASTE=2.0, DS2=1.0, NO_DS=0, NO_DC=0, OBS=0, DURM=1.0, SV=1.0, FF=0.25)); sim2.DUR['Charm'] = 4
SIZE = 5
def team_task(a):
    label, spec, lv, n, seed = a; setp(); sim2.DUR.update(spec.get('dur') or {}); sim2.reset_stats(); s = spec_build(spec); saved = apply_ctx(s, spec)
    g = sim.gear(s['items']); rng = random.Random(seed); random.seed(seed + 7); ids = [j['id'] for j in s['jobs']]; pos = {i: k for k, i in enumerate(ids)}
    X = np.zeros((n, len(ids)), dtype=np.int8); y = np.zeros(n); acts = []; JB = {j['id']: j for j in s['jobs']}
    for b in range(n):
        ta = rng.sample(ids, SIZE); tb = rng.sample(ids, SIZE)
        A = [sim2.mk(JB[i], lv, g, s['abil']) for i in ta]; B = [sim2.mk(JB[i], lv, g, s['abil']) for i in tb]
        r, ac = sim2.battle(A, B, rng); y[b] = r; acts.append(ac)
        for i in ta: X[b, pos[i]] += 1
        for i in tb: X[b, pos[i]] -= 1
    undo_ctx(saved); st = sim2.STATS
    return dict(label=label, lv=lv, X=X, y=y, acts=S.mean(acts), ids=ids, use={f'{k[0]}|{k[2]}': v for k, v in st['use'].items()}, evall={f'{k[0]}|{k[1]}': v for k, v in st['evall'].items()},
                evalln={f'{k[0]}|{k[1]}': v for k, v in st['evalln'].items()}, best={f'{k[0]}|{k[1]}': v for k, v in st['best'].items()}, n_act={f'{k[0]}': v for k, v in st['acts'].items()},
                moves=dict(st['moves']), mp={f'{c}': st['mp'][(c, l)] / max(1, st['mpn'][(c, l)]) for (c, l) in st['mp']})
def strat_task(a):
    label, spec, j_id, lv, n, seed = a; setp(); sim2.DUR.update(spec.get('dur') or {}); sim2.reset_stats(); s = spec_build(spec); saved = apply_ctx(s, spec)
    g = sim.gear(s['items']); rng = random.Random(seed); random.seed(seed + 7); JB = {j['id']: j for j in s['jobs']}; ids = [i for i in JB if i != j_id]; w = 0; ac = []
    for _ in range(n):
        o = rng.sample(ids, 2 * SIZE - 1)
        A = [sim2.mk(JB[j_id], lv, g, s['abil'])] + [sim2.mk(JB[i], lv, g, s['abil']) for i in o[:SIZE - 1]]; B = [sim2.mk(JB[i], lv, g, s['abil']) for i in o[SIZE - 1:]]
        r, a_ = sim2.battle(A, B, rng); w += r; ac.append(a_)
    undo_ctx(saved); st = sim2.STATS; cn = JB[j_id]['name']; tot = max(1, st['acts'][(cn, lv)])
    return dict(label=label, cls=f"{cn}/{JB[j_id]['race']}", j=j_id, lv=lv, win=w / n, acts=S.mean(ac), mp=st['mp'][(cn, lv)] / max(1, st['mpn'][(cn, lv)]),
                top=[(k[2], round(v / tot * 100)) for k, v in sorted(st['use'].items(), key=lambda kv: -kv[1]) if k[0] == cn and k[1] == lv][:4], moves=st['moves'][cn] / max(1, st['mpn'][(cn, lv)]))
def logit(X, y, lam=2.0, it=25):
    n, p = X.shape; Xd = X.astype(np.float64); b = np.zeros(p); b0 = 0.0
    for _ in range(it):
        z = Xd @ b + b0; pr = 1 / (1 + np.exp(-z)); W = pr * (1 - pr) + 1e-9
        g = np.concatenate([[np.sum(y - pr)], Xd.T @ (y - pr) - lam * b]); H = np.zeros((p + 1, p + 1))
        H[0, 0] = W.sum(); H[0, 1:] = Xd.T @ W; H[1:, 0] = H[0, 1:]; H[1:, 1:] = Xd.T @ (Xd * W[:, None]) + lam * np.eye(p)
        d = np.linalg.solve(H, g); b0 += d[0]; b += d[1:]
        if np.abs(d).max() < 1e-6: break
    cov = np.linalg.inv(H); return b, np.sqrt(np.diag(cov))[1:], b0
def run_team(label, spec, n_total, seed):
    T = [(label, spec, lv, n_total // 4, seed + q * 97) for lv in (10, 25, 45) for q in range(4)]
    with mp.Pool(4) as p: R = p.map(team_task, T, chunksize=1)
    out = {}
    for lv in (10, 25, 45):
        rs = [r for r in R if r['lv'] == lv]; X = np.concatenate([r['X'] for r in rs]); y = np.concatenate([r['y'] for r in rs])
        b, se, b0 = logit(X, y); ids = rs[0]['ids']
        agg = lambda key: collections.Counter({k: sum(r[key].get(k, 0) for r in rs) for r in rs for k in r[key]})
        out[lv] = dict(coef={str(i): float(b[k]) for k, i in enumerate(ids)}, se={str(i): float(se[k]) for k, i in enumerate(ids)}, acts=S.mean(r['acts'] for r in rs), n=len(y),
                       use=dict(agg('use')), evall=dict(agg('evall')), evalln=dict(agg('evalln')), best=dict(agg('best')), n_act=dict(agg('n_act')), moves=dict(agg('moves')),
                       mp={k: S.mean(r['mp'].get(k, 0) for r in rs) for k in rs[0]['mp']})
    json.dump(out, open(f'exp3_team_{label}.json', 'w'), ensure_ascii=False); print('team', label, 'feito', flush=True)
if __name__ == '__main__':
    what = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    if what == 'team_orig': run_team('orig', dict(base='orig'), n, 101)
    if what == 'team_r2': run_team('r2', dict(base='ref2'), n, 101)
