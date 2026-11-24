# -*- coding: utf-8 -*-
"""F1 (somente dados): constrói o cenário proposto e ajusta o 'orçamento de poder' de cada classe com o simulador."""
import copy, json, sys, statistics as S
import sim
ROLE = {}
for n in ['Paladin', 'Templar', 'Defender', 'Warrior', 'Mog Knight', 'Soldier', 'Gadgeteer']: ROLE[n] = 'guardiao'
for n in ['Fighter', 'Dragoon', 'Gladiator', 'Sniper', 'Hunter', 'Archer', 'Gunner']: ROLE[n] = 'atacante'
for n in ['Thief', 'Ninja', 'Assassin', 'Fencer', 'White Monk', 'Juggler']: ROLE[n] = 'agil'
for n in ['Black Mage', 'Red Mage', 'Illusionist', 'Elementalist', 'Summoner', 'Alchemist', 'Sage']: ROLE[n] = 'mago'
for n in ['White Mage', 'Bishop', 'Animist', 'Time Mage', 'Beastmaster', 'Morpher', 'Blue Mage']: ROLE[n] = 'apoio'
# forma (identidade) por papel – multiplicadores de crescimento: hp, atk, def, pow, res (orçamento é ajustado depois)
SHAPE = {'guardiao': (1.10, 0.97, 1.12, 0.92, 1.05), 'atacante': (0.98, 1.08, 0.95, 0.92, 0.96), 'agil': (0.93, 1.02, 0.93, 0.98, 0.96),
         'mago': (1.0, 0.90, 1.0, 1.05, 1.05), 'apoio': (1.0, 0.93, 1.0, 1.05, 1.10)}
CAPSTONE = {'Ninja', 'Red Mage', 'Assassin', 'Hunter', 'Gladiator', 'Sage', 'Mog Knight'}   # têm habilidade de 999 AP -> baseline um pouco menor
def target(name):
    if name == 'Time Mage': return 0.45
    return 0.48 if name in CAPSTONE else 0.50
def build(scn0, k=None, spd=(0.7, 0.5), eva=0.6, shape=True, gearmod=True, mp_caster=0.7, mods=False):
    scn = copy.deepcopy(scn0); k = k or {}
    if mods:
        import sim2; scn['mods'] = sim2.price_mods()
    if gearmod:
        import f1_items as fi
        scn['items'] = fi.items_f1(scn['items']); scn['abil'] = fi.abil_f1(scn['abil'])
    for j in scn['jobs']:
        r = ROLE.get(j['name'], 'atacante'); sh = SHAPE[r] if shape else (1,) * 5
        kk = k.get(j['id'], 1.0)
        for key, gk, m in (('hp', 'g_hp', sh[0]), ('atk', 'g_atk', sh[1]), ('dfn', 'g_def', sh[2]), ('pow', 'g_pow', sh[3]), ('res', 'g_res', sh[4])):
            j[gk] = min(25.5, round(j[gk] * m * kk, 1)); j[key] = min(255 if key in ('hp', 'dfn', 'res') else 4095, round(j[key] * kk))
        if r in ('mago',): j['g_mp'] = round(j['g_mp'] * mp_caster, 1); j['mp'] = round(j['mp'] * (0.5 + 0.5 * mp_caster))
        j['spd'] = round(100 + spd[0] * (j['spd'] - 100)); j['g_spd'] = round(1.2 + spd[1] * (j['g_spd'] - 1.2), 1)
        j['eva'] = round(50 + eva * (j['eva'] - 50))
    return scn
def fit(scn0, iters=7, n=2200, levels=(10, 25, 45), **kw):
    k = {j['id']: 1.0 for j in scn0['jobs']}
    for it in range(iters):
        scn = build(scn0, k, **kw); r = sim.run(scn, levels=levels, n=n, seed=100 + it)
        err = []
        for j in scn['jobs']:
            w = S.mean(r[lv][j['id']] for lv in levels); t = target(j['name'])
            if sim.PROFILE.get(j['name']) in (sim.HEAL, sim.UTIL): err.append(0); continue   # curandeiros/utilidade: sem ajuste (suposições do simulador)
            k[j['id']] = max(0.85, min(1.15, k[j['id']] * (1 + 1.0 * (t - w)))); err.append(abs(w - t))
        print(f'iter {it}: erro médio {S.mean(err):.3f} máx {max(err):.3f}', flush=True)
    dm = [k[j['id']] for j in scn0['jobs'] if sim.PROFILE.get(j['name']) in (sim.PHYS, sim.MAGE)]; mk_ = sum(dm) / len(dm)
    k = {i: round(v / mk_, 3) if True else v for i, v in k.items()}
    return k
if __name__ == '__main__':
    scn0 = sim.load(); k = fit(scn0)
    json.dump({str(a): b for a, b in k.items()}, open('f1_k.json', 'w'))
    scn = build(scn0, k); r = sim.run(scn, n=5000, seed=7); sim.summarize(r, scn['jobs'], 'F1')
    r0 = sim.run(scn0, n=5000, seed=7); sim.summarize(r0, scn0['jobs'], 'ATUAL')
