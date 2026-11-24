# -*- coding: utf-8 -*-
"""Simulador abstrato de batalha 3x3 (fórmulas do Mechanics Guide) para comparar cenários de balanceamento.
LIMITES (declarados): sem mapa/alcance/altura/facing; sem status nem habilidades de classe; IA simples (foca menor HP%);
cura = (MPow - MRes_alvo/2)*poder/100 (mesma rotina de dano, conforme o guia); equipamento por faixa = média de quartis de preço do que existe em loja.
Serve para medir distribuição de poder BASE entre classes, não para prever a campanha."""
import random, statistics as S, copy
from romdata import jobs, items, abilities
PHYS, MAGE, HEAL, UTIL = 'fis', 'mag', 'cur', 'util'
AOE = 0.45
TARGET = 'focus'   # 'focus' = menor HP%; 'random'
HEALON = True   # chance de a magia de área acertar um 2º inimigo
PROFILE = {}
for n in ['Soldier', 'Paladin', 'Fighter', 'Warrior', 'Dragoon', 'Defender', 'Gladiator', 'Templar', 'Mog Knight', 'Fencer', 'Thief', 'Ninja',
          'Assassin', 'White Monk', 'Archer', 'Hunter', 'Sniper', 'Gunner', 'Juggler', 'Gadgeteer', 'Animist', 'Beastmaster', 'Morpher', 'Blue Mage']: PROFILE[n] = PHYS
for n in ['Black Mage', 'Illusionist', 'Elementalist', 'Red Mage', 'Summoner', 'Alchemist', 'Sage']: PROFILE[n] = MAGE
for n in ['White Mage', 'Bishop']: PROFILE[n] = HEAL
PROFILE['Time Mage'] = UTIL
ROBE = {MAGE, HEAL, UTIL}
def load():
    J = [j for j in jobs() if j['race'] in (1, 2, 3, 4, 5) and j['name'] and j['name'] != '?' and j['hp'] and j['id'] < 0x39]
    return dict(jobs=J, items=[t for t in items() if t['name']], abil={a['name']: a for a in abilities() if a['name'] and a['name'] != '-'})
def quart(lst, key):
    lst = sorted(lst, key=lambda t: t['buy'])
    if not lst: return [0, 0, 0, 0]
    n = len(lst); out = []
    for q in range(4):
        part = lst[q * n // 4:(q + 1) * n // 4] or [lst[min(n - 1, q * n // 4)]]
        out.append(S.mean(key(t) for t in part))
    return out
def gear(items_):
    shop = lambda lo, hi: [t for t in items_ if lo <= t['type'] <= hi and t['buy']]
    g = {}
    g['wep'] = quart(shop(1, 19), lambda t: t['atk'])
    g['rod_pow'] = quart(shop(10, 12), lambda t: t['pow'])
    body = shop(24, 25); head = shop(21, 23); feet = shop(27, 27); shield = shop(20, 20); robe = shop(26, 26)
    g['phys_def'] = [a + b + c + d for a, b, c, d in zip(quart(body, lambda t: t['dfn']), quart(head, lambda t: t['dfn']), quart(feet, lambda t: t['dfn']), quart(shield, lambda t: t['dfn']))]
    g['phys_res'] = [a + b for a, b in zip(quart(body, lambda t: t['res']), quart(head, lambda t: t['res']))]
    g['phys_eva'] = quart(shield, lambda t: t['eva'])
    g['mage_def'] = [a + b for a, b in zip(quart(robe, lambda t: t['dfn']), quart(head, lambda t: t['dfn']))]
    g['mage_res'] = [a + b + c for a, b, c in zip(quart(robe, lambda t: t['res']), quart(head, lambda t: t['res']), quart(feet, lambda t: t['res']))]
    return g
def tier(level): return 0 if level <= 12 else 1 if level <= 25 else 2 if level <= 38 else 3
def spells(abil):
    pick = lambda n: (abil[n]['power'], abil[n]['mp'])
    return [pick('Fire'), pick('Fira'), pick('Firaga')], [pick('Cure'), pick('Cura'), pick('Curaga')]
def mk(j, level, gear_, abil, cfg):
    t = tier(level); prof = PROFILE.get(j['name'], PHYS); rob = prof in ROBE
    L = lambda b, g: b * 1.05 + g * (level - 1)
    u = dict(name=j['name'], id=j['id'], prof=prof, lvl=level,
             hp=L(j['hp'], j['g_hp']) + 0, mp=L(j['mp'], j['g_mp']), spd=L(j['spd'], j['g_spd']),
             atk=L(j['atk'], j['g_atk']), dfn=L(j['dfn'], j['g_def']), pw=L(j['pow'], j['g_pow']), rs=L(j['res'], j['g_res']),
             eva=j['eva'] + (0 if rob else gear_['phys_eva'][t]))
    u['wep'] = gear_['wep'][t] * (0.8 if rob else 1.0)
    u['dfn'] += gear_['mage_def'][t] if rob else gear_['phys_def'][t]
    u['rs'] += gear_['mage_res'][t] if rob else gear_['phys_res'][t]
    u['pw'] += gear_['rod_pow'][t] if rob else 0
    u['hp'] = u['hp'] * cfg.get('hp_scale', 1) ; u['mp0'] = u['mp']; u['maxhp'] = u['hp']; u['cnt'] = 0
    return u
def fight_dmg(a, d):
    base = max(1, a['atk'] + a['wep'] - (d['dfn']) / 2)
    return max(1, base * a['wep'] / 100)
def act(u, own, foes, sp, hl, rng):
    live = [f for f in foes if f['hp'] > 0]
    if not live: return
    tgt = min(live, key=lambda f: f['hp'] / f['maxhp']) if TARGET == 'focus' else rng.choice(live)
    hit = lambda d: rng.random() * 100 < min(95, max(5, 100 - d['eva']))
    p = u['prof']
    if p == HEAL:
        hurt = [a for a in own if a['hp'] > 0 and a['hp'] / a['maxhp'] < 0.5]
        if hurt and HEALON:
            pw, mp = hl[min(2, tier(u['lvl']))]
            if u['mp'] >= mp:
                t2 = min(hurt, key=lambda a: a['hp'] / a['maxhp']); u['mp'] -= mp
                t2['hp'] = min(t2['maxhp'], t2['hp'] + max(1, u['pw'] - t2['rs'] / 2) * pw / 100 * rng.uniform(.9, 1.1)); return
    if p in (MAGE, UTIL, HEAL) and True:
        pw, mp = sp[min(2, tier(u['lvl']))]
        if p == UTIL: pw *= 0.6
        if p == HEAL: pw = pw * 0.5
        if u['mp'] >= mp and hit(tgt):
            dm = max(1, u['pw'] - tgt['rs'] / 2) * pw / 100
            tgt['hp'] -= dm * rng.uniform(.9, 1.1)
            others = [f for f in live if f is not tgt]
            if others and rng.random() < AOE and hit(others[0]):   # área r1: 2º alvo adjacente
                o = rng.choice(others); o['hp'] -= max(1, u['pw'] - o['rs'] / 2) * pw / 100 * rng.uniform(.9, 1.1)
            u['casts'] = u.get('casts', 0) + 1; return
        if u['mp'] >= mp: u['mp'] -= mp; return
        u['dry'] = u.get('dry', 0) + 1
    if hit(tgt): tgt['hp'] -= fight_dmg(u, tgt) * rng.uniform(.9, 1.1)
LAST = {'acts': 0}
def battle(A, B, sp, hl, rng, maxturn=400):
    units = A + B; LAST['acts'] = 0; order = {id(u): i for i, u in enumerate(units)}
    for u in units: u['cnt'] = 0
    for _ in range(maxturn * 40):
        for u in units:
            if u['hp'] > 0: u['cnt'] += u['spd']
        ready = sorted([u for u in units if u['hp'] > 0 and u['cnt'] >= 1000], key=lambda u: (-u['cnt'], order[id(u)]))
        for u in ready:
            if u['hp'] <= 0: continue
            own, foe = (A, B) if u in A else (B, A)
            act(u, own, foe, sp, hl, rng); u['cnt'] -= 1000; LAST['acts'] += 1
            if all(f['hp'] <= 0 for f in foe): return 1 if u in A else 0
        if all(u['hp'] <= 0 for u in B): return 1
        if all(u['hp'] <= 0 for u in A): return 0
    return 0.5
def run(scn, levels=(10, 25, 45), n=4000, seed=1, size=3):
    rng = random.Random(seed); g = gear(scn['items']); sp, hl = spells(scn['abil']); J = scn['jobs']; cfg = scn.get('cfg', {})
    res = {}
    for lv in levels:
        W = {j['id']: [0, 0] for j in J}
        for _ in range(n):
            ta = rng.sample(J, size); tb = rng.sample(J, size)
            A = [mk(j, lv, g, scn['abil'], cfg) for j in ta]; B = [mk(j, lv, g, scn['abil'], cfg) for j in tb]
            r = battle(A, B, sp, hl, rng)
            for j in ta: W[j['id']][0] += r; W[j['id']][1] += 1
            for j in tb: W[j['id']][0] += 1 - r; W[j['id']][1] += 1
        res[lv] = {i: w / c for i, (w, c) in W.items() if c}
    return res
def summarize(res, J, label=''):
    nm = {j['id']: j['name'] + '/' + str(j['race']) for j in J}
    for lv, d in res.items():
        v = sorted(d.items(), key=lambda kv: -kv[1]); vals = [x for _, x in v]
        print(f'{label} L{lv}: min {min(vals):.2f} max {max(vals):.2f} desvio {S.pstdev(vals):.3f}  | topo {[(nm[i][:10], round(w, 2)) for i, w in v[:4]]} | base {[(nm[i][:10], round(w, 2)) for i, w in v[-4:]]}')
if __name__ == '__main__':
    scn = load(); r = run(scn, n=3000); summarize(r, scn['jobs'], 'ATUAL')
