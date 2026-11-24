# -*- coding: utf-8 -*-
"""Pacote completo (atributos + itens + habilidades) vs original, níveis 10/25/45, e separação do efeito de cada módulo."""
import json, sys, statistics as S, collections, multiprocessing as mp
import sim, sim2, f1
from exp_pacotes import CAT as ABCAT
scn0 = sim.load(); k4 = {int(a): b for a, b in json.load(open('f1v4_k.json')).items()}
SH = {s: 6 for s in ('Confushot', 'Charmshot', 'Blindshot', 'Silenshot', 'Stopshot')}; AB = {**SH, 'Cupid': 8}
def scen(name):
    if name == 'original': return scn0, 4
    if name == 'só habilidades (tiros 6 + Cupid 8)': s = dict(scn0); s['mods'] = AB; return s, 4
    if name == 'só atributos e itens': return f1.build(scn0, k4, atk_scale=1.12), 4
    if name == 'pacote completo': return f1.build(scn0, k4, mods=AB, atk_scale=1.12), 4
    if name == 'completo + Charm 2 turnos (hipotético)': return f1.build(scn0, k4, mods=AB, atk_scale=1.12), 2
VAR = ['original', 'só habilidades (tiros 6 + Cupid 8)', 'só atributos e itens', 'pacote completo', 'completo + Charm 2 turnos (hypo)']
VAR[-1] = 'completo + Charm 2 turnos (hipotético)'
def task(a):
    name, lv, n, seed, obs = a
    s, charm = scen(name); sim2.DUR['Charm'] = charm; sim2.P['OBS'] = obs; sim2.reset_stats()
    r, p = sim2.run(s, levels=(lv,), n=n, seed=seed)
    roles = collections.defaultdict(collections.Counter)
    for (c, l, ab), v in sim2.STATS['use'].items(): roles[c][ABCAT.get(ab, 'dano')] += v
    return dict(name=name, lv=lv, obs=obs, win={str(k): v for k, v in r[lv].items()}, acts=p[lv], roles={c: dict(v) for c, v in roles.items()},
                att=dict(sim2.STATS['att']), succ=dict(sim2.STATS['succ']), use={f'{k[0]}|{k[2]}': v for k, v in sim2.STATS['use'].items()})
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    T = [(v, lv, n, 41, obs) for obs in (0, 1) for v in VAR for lv in (10, 25, 45)]
    print(len(T), flush=True)
    with mp.Pool(4) as pool: R = pool.map(task, T, chunksize=1)
    json.dump(R, open('exp_final_raw.json', 'w'), ensure_ascii=False); print('feito')
