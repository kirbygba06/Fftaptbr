# -*- coding: utf-8 -*-
"""F1 v2: mesmo método (forma por papel + orçamento por classe) mas ajustado no simulador v2 (habilidades e status)."""
import json, sys, statistics as S, sim, sim2, f1
UNTUNED = {'Thief', 'Beastmaster', 'Morpher', 'Blue Mage'}     # kit não modelável (steal/morph/learning): só forma, sem orçamento
def fit(scn0, iters=7, n=1400, levels=(10, 25, 45), mods=False):
    k = {j['id']: 1.0 for j in scn0['jobs']}
    for it in range(iters):
        scn = f1.build(scn0, k, mods=mods); r, _ = sim2.run(scn, levels=levels, n=n, seed=300 + it); err = []
        for j in scn['jobs']:
            if j['name'] in UNTUNED: continue
            w = S.mean(r[lv][j['id']] for lv in levels); k[j['id']] = max(0.80, min(1.20, k[j['id']] * (1 + 1.0 * (0.5 - w)))); err.append(abs(w - 0.5))
        print(f'iter {it}: erro médio {S.mean(err):.3f} máx {max(err):.3f}', flush=True)
    tuned = [k[j['id']] for j in scn0['jobs'] if j['name'] not in UNTUNED]; m = sum(tuned) / len(tuned)
    return {i: (round(v / m, 3) if True else v) for i, v in k.items()}
if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else ''
    SHOTS = ['Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot']
    mods = True if arg == 'mods' else ({**{s: 6 for s in SHOTS}, 'Cupid': 8} if arg == 'v4' else False)
    scn0 = sim.load(); k = fit(scn0, mods=mods, iters=8)
    json.dump({str(a): b for a, b in k.items()}, open({'mods': 'f1v3_k.json', 'v4': 'f1v4_k.json'}.get(arg, 'f1v2_k.json'), 'w'))
