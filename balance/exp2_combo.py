# -*- coding: utf-8 -*-
"""JP / Combo / Hunting no simulador (modelo paramétrico: não se sabe quanto JP as unidades têm em jogo real)."""
import json, sys, random, statistics as S, collections, multiprocessing as mp
import sim, sim2, combo, exp2
combo.install()
scn0 = exp2.scn0
def reset_cfg(): combo.CFG.update(on=False, jp0=0, jpt=0.0, K=4, cap=None, consume=1.0, hunt_jp=10, ko_jp=1)
def gtask(a):
    label, cfg, lv, n, seed = a
    reset_cfg(); exp2.setparams({}); combo.CFG.update(cfg); sim2.reset_stats(); sim2.STATS['cmb'] = collections.Counter()
    r, p = sim2.run(scn0, levels=(lv,), n=n, seed=seed); st = sim2.STATS
    uses = sum(st['use'].values()); cu = sum(v for k, v in st['use'].items() if k[2] == 'Combo')
    cw = collections.Counter()
    for (c, l, ab), v in st['use'].items():
        if ab == 'Combo': cw[c] += v
    return dict(label=label, cfg=cfg, lv=lv, win={str(k): v for k, v in r[lv].items()}, acts=p[lv], combo_share=cu / max(1, uses), mult=st['cmb']['mult'] / max(1, st['cmb']['n']),
                combos_per_battle=st['cmb']['n'] / n, combo_by_class=dict(cw), n_act={c: v for (c, l), v in st['acts'].items()})
def htask(a):
    label, cfg, j_id, lv, n, seed = a
    reset_cfg(); exp2.setparams({}); combo.CFG.update(cfg); sim2.reset_stats(); sim2.STATS['cmb'] = collections.Counter()
    j = next(x for x in scn0['jobs'] if x['id'] == j_id); g = sim.gear(scn0['items']); rng = random.Random(seed); random.seed(seed + 7); w = 0; jpend = []
    for _ in range(n):
        o = rng.sample([x for x in scn0['jobs'] if x['id'] != j_id], 5)
        A = [sim2.mk(j, lv, g, scn0['abil'])] + [sim2.mk(x, lv, g, scn0['abil']) for x in o[:2]]; B = [sim2.mk(x, lv, g, scn0['abil']) for x in o[2:]]
        r, a_ = sim2.battle(A, B, rng); w += r; jpend.append(A[0].get('jp', 0))
    st = sim2.STATS; cn = j['name']
    return dict(label=label, lv=lv, cls=cn, win=w / n, jp_end=S.mean(jpend), hunting_share=st['use'][(cn, lv, 'Hunting')] / max(1, st['acts'][(cn, lv)]), combo_share=st['use'][(cn, lv, 'Combo')] / max(1, st['acts'][(cn, lv)]))
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    F = {'original K=4': dict(K=4), 'K=2': dict(K=2), 'JP útil ≤5': dict(K=4, cap=5), 'K=2 e JP ≤5': dict(K=2, cap=5)}
    T = []
    for jp0 in (0, 3, 5, 10):
        for fl, fc in F.items():
            for lv in (25, 45):
                T.append((f'JP inicial {jp0} | {fl}', dict(on=True, jp0=jp0, **fc), lv, n, 81))
    T += [('JP inicial 5 | original, consome metade', dict(on=True, jp0=5, K=4, consume=0.5), lv, n, 81) for lv in (25, 45)]
    with mp.Pool(4) as pl: R = pl.map(gtask, T, chunksize=1)
    json.dump(R, open('exp2_combo.json', 'w'), ensure_ascii=False); print('combo feito', len(R), flush=True)
    hj = next(j for j in scn0['jobs'] if j['name'] == 'Hunter')['id']
    H = [(f'Hunting {h} JP', dict(on=True, jp0=0, K=4, hunt_jp=h), hj, 45, 2500, 91) for h in (10, 3, 1)]
    with mp.Pool(3) as pl: R2 = pl.map(htask, H, chunksize=1)
    json.dump(R2, open('exp2_hunting.json', 'w'), ensure_ascii=False); print('hunting feito', flush=True)
