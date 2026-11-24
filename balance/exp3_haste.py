import json, sys, random, statistics as S, multiprocessing as mp
import sim, sim2, exp3
from exp3 import jj
def task(a):
    label, spec, ai, j_id, lv, n, seed = a; exp3.setp(); sim2.AI['HASTE_V'] = ai.get('HASTE_V', 1.0); sim2.reset_stats()
    s = exp3.spec_build(spec); saved = exp3.apply_ctx(s, spec); g = sim.gear(s['items']); rng = random.Random(seed); random.seed(seed + 7); JB = {j['id']: j for j in s['jobs']}; ids = [i for i in JB if i != j_id]; w = 0
    for _ in range(n):
        o = rng.sample(ids, 9); A = [sim2.mk(JB[j_id], lv, g, s['abil'])] + [sim2.mk(JB[i], lv, g, s['abil']) for i in o[:4]]; B = [sim2.mk(JB[i], lv, g, s['abil']) for i in o[4:]]
        r, _a = sim2.battle(A, B, rng); w += r
    exp3.undo_ctx(saved); st = sim2.STATS; casts = st['hcast']['Haste']; uses = sum(v for k, v in st['use'].items() if k[2] == 'Haste')
    return dict(label=label, cls=JB[j_id]['name'], race=JB[j_id]['race'], lv=lv, win=w / n, casts=casts, realized=st['hgain']['Haste'] / max(1, casts))
if __name__ == '__main__':
    V = [('normal', dict(base='orig'), {}), ('IA valoriza Haste ×0,5', dict(base='orig'), {'HASTE_V': 0.5}), ('IA valoriza Haste ×0,25', dict(base='orig'), {'HASTE_V': 0.25}), ('sem Haste', dict(base='orig', disable=['Haste']), {})]
    T = [(l, sp_, ai, i, lv, 2000, 311) for l, sp_, ai in V for c in ('Time Mage', 'Templar') for i in jj(c, 3 if c == 'Time Mage' else 2) for lv in (25, 45)]
    with mp.Pool(4) as p: R = p.map(task, T, chunksize=2)
    json.dump(R, open('exp3_haste.json', 'w'), ensure_ascii=False)
    print('| variante | classe | nível | vitória | Haste lançado por batalha-amostra | ganho realizado por Haste (valor) |\n|---|---|---|---|---|---|')
    for r in R: print(f"| {r['label']} | {r['cls']} | {r['lv']} | {r['win']*100:.0f}% | {r['casts']} | {r['realized']:.0f} |")
