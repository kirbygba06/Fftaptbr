# -*- coding: utf-8 -*-
"""Extensão do simulador v2: JP e Combo (fórmula do Mechanics Guide). Não altera sim2.py (monkeypatch em tempo de execução).
Combo: o iniciador precisa de JP>=1; golpe final com 100% de acerto, ignora reações, usa o dano de Fight.
Cadeia: cada aliado com Combo no alcance acerta com seu Hit% e soma seu Poder%; multiplicador = (1 + soma) * (10 + K*JP)/10 se a cadeia acertar >=1.
SUPOSIÇÕES: quanto JP as unidades têm (varrido), consumo de JP, chance de o aliado estar no alcance."""
import sim2, random, re
COMBO = {  # classe -> (poder, alcance, hit)
 'Soldier': (.10, 1, 1.0), 'Paladin': (.10, 1, 1.0), 'Fighter': (.15, 1, .70), 'Thief': (.05, 2, 1.0), 'Ninja': (.05, 2, 1.0), 'White Mage': (.05, 4, .60), 'Black Mage': (.05, 4, .60),
 'Illusionist': (.10, 4, .40), 'Blue Mage': (.10, 4, .40), 'Archer': (.05, 6, .40), 'Hunter': (.08, 4, .50), 'Warrior': (.10, 1, 1.0), 'Dragoon': (.10, 2, 1.0), 'Defender': (.15, 1, .70),
 'Gladiator': (.10, 1, 1.0), 'White Monk': (.12, 2, .90), 'Bishop': (.08, 4, .60), 'Templar': (.12, 1, 1.0), 'Time Mage': (.05, 4, .60), 'Alchemist': (.10, 2, .60), 'Beastmaster': (.12, 1, 1.0),
 'Morpher': (.10, 2, 1.0), 'Sage': (.10, 2, .60), 'Fencer': (.10, 1, 1.0), 'Elementalist': (.10, 3, .60), 'Red Mage': (.10, 2, .70), 'Summoner': (.10, 4, .40), 'Assassin': (.10, 2, 1.0),
 'Sniper': (.08, 4, .50), 'Animist': (.12, 1, 1.0), 'Mog Knight': (.15, 1, .70), 'Gunner': (.05, 5, .40), 'Juggler': (.10, 3, .70), 'Gadgeteer': (.12, 6, .30)}
IN_RANGE = {1: .35, 2: .5, 3: .6, 4: .7, 5: .75, 6: .8}
CFG = dict(on=False, jp0=0, jpt=0.0, K=4, cap=None, consume=1.0, hunt_jp=10, ko_jp=1)
CB = sim2.Ab(); CB.name = 'Combo'; CB.basis = 'W'; CB.power = None; CB.mp = 0; CB.rng = 'As Weapon'; CB.area = 'One Unit'; CB.eff = [dict(hit='100%H', tgt='Enemy', dep=False, kind='combo', m=1.0)]
def mult(jp, chain):
    if chain <= 0: return 1.0
    j = min(jp, CFG['cap']) if CFG['cap'] else jp
    return (1 + chain) * (10 + CFG['K'] * j) / 10
def chain_of(u, own, rng):
    c = 0.0; n = 0
    for x in own:
        if x is u or x['hp'] <= 0 or sim2.has(x, 'Stop') or sim2.has(x, 'Sleep') or sim2.has(x, 'Petrify') or sim2.has(x, 'Charm') or sim2.has(x, 'Confusion'): continue
        cd = COMBO.get(x['name'])
        if cd and rng.random() < IN_RANGE.get(cd[1], .5) and rng.random() < cd[2]: c += cd[0]; n += 1
    return c, n
_mk = sim2.mk
def mk(j, level, g, abil, cfg=None, scenario_mp=None):
    u = _mk(j, level, g, abil)
    if CFG['on']: u['jp'] = CFG['jp0']; u['abs'] = u['abs'] + [CB]
    return u
_score = sim2.score_ability
def score_ability(u, a, own, foes, rng):
    if a is CB:
        if u.get('jp', 0) < 1: return 0, None
        live = [f for f in foes if f['hp'] > 0 and not sim2.has(f, 'Petrify')]
        if not live: return 0, None
        r = sim2.reach(u, sim2.FIGHT); best = (0, None)
        # cadeia esperada: média de duas amostras
        ch = [chain_of(u, own, rng)[0] for _ in range(3)]; ec = sum(ch) / 3
        for t in live:
            dm = sim2.base_dmg(u, t, sim2.FIGHT, dict(m=1.0)) * (mult(u['jp'], ec) if ec > 0 else 1.0)
            v = min(dm, t['hp']) + (t.get('dps', 100) * 2 if dm >= t['hp'] else 0)
            if v * r > best[0]: best = (v * r, t)
        return best
    return _score(u, a, own, foes, rng)
_do = sim2.do_effects
def do_effects(u, t, a, own, foes, rng, e1ok):
    if a is CB:
        c, n = chain_of(u, own, rng); m = mult(u['jp'], c); dm = sim2.base_dmg(u, t, sim2.FIGHT, dict(m=1.0)) * m * rng.uniform(.9, 1.1)
        if sim2.has(t, 'Expert Guard'): dm = 0
        t['hp'] -= dm; sim2.STATS['impact']['Combo'] += min(dm, max(0, t['hp'] + dm)); sim2.STATS['cmb']['mult'] += m; sim2.STATS['cmb']['n'] += 1
        for _s in ('Sleep', 'Charm'): t['st'].pop(_s, None)
        u['jp'] = u['jp'] * (1 - CFG['consume'])
        if t['hp'] <= 0: u['jp'] = u.get('jp', 0) + CFG['ko_jp']
        return
    hp0 = t['hp']; _do(u, t, a, own, foes, rng, e1ok)
    if CFG['on'] and hp0 > 0 and t['hp'] <= 0 and t in foes:
        u['jp'] = u.get('jp', 0) + (CFG['hunt_jp'] if a.name == 'Hunting' else CFG['ko_jp'])
_tt = sim2.take_turn
def take_turn(u, own, foes, rng):
    if CFG['on']: u['jp'] = u.get('jp', 0) + CFG['jpt']
    _tt(u, own, foes, rng)
def install():
    sim2.mk = mk; sim2.score_ability = score_ability; sim2.do_effects = do_effects; sim2.take_turn = take_turn
    import collections; sim2.STATS['cmb'] = collections.Counter()
