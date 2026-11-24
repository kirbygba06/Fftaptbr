# -*- coding: utf-8 -*-
"""Rodadas de viabilidade: habilidades pouco usadas ganham mais poder (só as de dano) e/ou menos MP, em passos crescentes.
Rodada 1: poder x1,15 e MP x0,8; rodada 2: x1,30 e x0,6; rodada 3: x1,50 e x0,4 (apenas para as que continuam pouco usadas)."""
import os, sys, json, collections, statistics as S, multiprocessing as mp
os.environ.setdefault('PROG', '2'); os.environ.setdefault('APB', '40'); os.environ.setdefault('SEC', '1')
import numpy as np
import sim2, exp3, exp4_teams_specs as SP
from exp8_list import effective
STEPS = {1: (1.15, 0.8), 2: (1.30, 0.6), 3: (1.50, 0.4)}
def underused_from(path, thr=0.03):
    T = json.load(open(path)); rows = {}
    for lv in ('25', '45'):
        d = T[lv]
        for key, n in d['evalln'].items():
            if n < 200: continue
            c, ab = key.split('|', 1)
            if ab == 'Fight' or sim2.norm(ab) not in sim2.CAT: continue
            rows.setdefault((c, ab), {})[lv] = (d['best'].get(key, 0) / n, d['evall'].get(key, 0) / n, n)
    res = {}
    for (c, ab), v in rows.items():
        lv = '25' if '25' in v else '45'; res[(c, ab)] = v[lv]
    return res
def levers(name):
    a = sim2.CAT[sim2.norm(name)]; mp, pw, _ = effective(name)
    dmg = any(e['kind'] in ('dmg', 'hpfrac') for e in a.eff) and a.basis is not None
    return mp, pw, dmg
def candidates():
    """habilidades modeladas pouco usadas no pacote atual que têm alavanca (MP > 0 ou poder fixo de dano)"""
    U = json.load(open('exp8_underused.json')); out = {}
    for u in U:
        if not u['modeled'] or u['lever'] == 'nenhuma': continue
        out.setdefault(u['ab'], []).append(u['cls'])
    return out
def patch_mods(names, rnd):
    fp, fm = STEPS[rnd]; mods = {}
    for ab in names:
        mp, pw, dmg = levers(ab); m = {}
        base_mp = effective_base_mp(ab); base_pw = effective_base_pw(ab)
        if dmg and base_pw is not None: m['power'] = int(round(base_pw * fp))
        if base_mp > 0: m['mp'] = max(1, int(round(base_mp * fm)))
        if m: mods[ab] = m
    return mods
def effective_base_mp(ab): return effective(ab)[0]
def effective_base_pw(ab): return effective(ab)[1]
def run_team_n(label, spec, ns, seed=101):
    T = [(label, spec, int(lv), n // 4, seed + q * 97) for lv, n in ns.items() for q in range(4)]
    with mp.Pool(4) as p: R = p.map(exp3.team_task, T, chunksize=1)
    out = {}
    for lv in ns:
        rs = [r for r in R if r['lv'] == int(lv)]; X = np.concatenate([r['X'] for r in rs]); y = np.concatenate([r['y'] for r in rs])
        b, se, b0 = exp3.logit(X, y); ids = rs[0]['ids']
        agg = lambda key: collections.Counter({k: sum(r[key].get(k, 0) for r in rs) for r in rs for k in r[key]})
        out[lv] = dict(avail=[str(i) for i in rs[0]['pool']], coef={str(i): float(b[k]) for k, i in enumerate(ids)}, se={str(i): float(se[k]) for k, i in enumerate(ids)},
                       acts=S.mean(r['acts'] for r in rs), n=len(y), use=dict(agg('use')), evall=dict(agg('evall')), evalln=dict(agg('evalln')), best=dict(agg('best')),
                       n_act=dict(agg('n_act')), mp={k: S.mean(r['mp'].get(k, 0) for r in rs) for k in rs[0]['mp']})
    json.dump(out, open(f'exp3_team_{label}.json', 'w'), ensure_ascii=False); print('rodada', label, 'feita', flush=True)
if __name__ == '__main__':
    rnd = int(sys.argv[1]); prev = sys.argv[2]            # arquivo da rodada anterior (ex.: exp3_team_q2_final3.json)
    cand = candidates()
    if rnd == 1: names = sorted(cand)
    else:
        us = underused_from(prev)
        names = sorted(ab for ab, cls in cand.items() if any(us.get((c, ab), (1, 0, 0))[0] < 0.03 for c in cls) or ab in json.load(open(f'exp8_patched_r{rnd-1}.json'))['viable'])
    prevmods = json.load(open(f'exp8_patched_r{rnd-1}.json'))['mods'] if rnd > 1 else {}
    # só reforça quem continua pouco usado; quem virou viável mantém o passo anterior
    if rnd > 1:
        us = underused_from(prev); still = [ab for ab, cls in cand.items() if any(us.get((c, ab), (1, 0, 0))[0] < 0.03 for c in cls)]
        viable = [ab for ab in prevmods if ab not in still]
        mods = {ab: prevmods[ab] for ab in viable}; mods.update(patch_mods(still, rnd))
    else:
        still = names; viable = []; mods = patch_mods(names, 1)
    spec = dict(SP.SPECS['final3']); spec['mods'] = {**spec['mods'], **mods}
    json.dump(dict(round=rnd, still=still, viable=viable, mods=mods), open(f'exp8_patched_r{rnd}.json', 'w'), ensure_ascii=False)
    print('rodada', rnd, ': reforçadas', len(still), '| mantidas', len(viable), flush=True)
    run_team_n(f'v1_r{rnd}', spec, {'25': 12000, '10': 4000, '45': 6000})
