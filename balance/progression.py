# -*- coding: utf-8 -*-
"""Modelo de progressão de habilidades: o que cada unidade já aprendeu depende de (1) a arma que ensina estar no estoque da loja
(estoque inicial, após 10 batalhas, após 20 batalhas, depois) e (2) o AP acumulado (AP por batalha x batalhas).
SUPOSIÇÕES (parâmetros): batalhas por nível, AP ganho por batalha, ordem de aprendizado (mais barata primeiro)."""
import json, os, re
import sim
here = os.path.dirname(__file__)
KIT = json.load(open(os.path.join(here, 'class_abilities.json')))
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
S1 = ['Buster Sword', 'Shadow Blade', 'Sun Blade', 'Atmos Blade', 'Samson Sword', 'Blue Saber', 'Shamshir', 'Apocalypse', 'Lionheart', 'Ragnarok', 'Ninja Knife', 'Murasame', 'Ashura', 'Osafune', 'Kotetsu',
      'Pure Staff', 'Bless Staff', 'Firewheel Rod', 'Thunder Rod', 'Sleet Rod', 'Terre Rod', 'Silver Bow', 'Javelin', 'Kaiser Knuckles', 'Sick Knuckles', 'Dream Claws', 'Silver Cannon', 'Conch Shell', 'Earth Bell', 'Black Quena', 'Satyr Flute']
S2 = ['Burglar Sword', 'Flametongue', 'Air Blade', 'Icebrand', 'Kwigon Blade', 'Ogun Blade', 'Defender', 'Striborg', 'Predator', 'Lohengrin', 'Kris Knife', 'Khukuri', 'Kard', 'Rondell Dagger', 'Mage Masher',
      'Kikuichimonji', "Heaven's Cloud", 'Cure Staff', 'Garnet Staff', 'Force Rod', 'Nail Bow', 'Twin Bow', 'Gae Bolg', 'Dragon Whisker']
S0 = ['Shortsword', 'Silver Sword', 'Sweep Blade', 'Barong', 'Falchion', 'Jack Knife', 'Scramasax', 'Jambiya', 'Stinger', 'Fleuret', 'Scarlette', 'White Staff', 'Guard Staff', 'Judge Staff', 'Rod',
      'Longbow', 'Char Bow', 'Thorn Bow', 'Demon Bell', 'Glass Bell', 'War Trumpet', 'Hard Knuckles', 'Rising Sun', 'Aiot Gun']
ST0 = {norm(x) for x in S0}; ST1 = {norm(x) for x in S1}; ST2 = {norm(x) for x in S2}
BATT_MULT = 1.0
MIX_W = float(os.environ.get('MIXW', '0.4'))
BATTLES = {10: 16, 25: 40, 45: 90, 50: 100}      # 20 batalhas já na luta contra Famfrit (nível 10–15)          # SUPOSIÇÃO: batalhas jogadas ao chegar no nível
STAGE_AT = {0: 0, 1: 10, 2: 20, 3: 35}                 # batalhas para o estoque 0 (inicial), 1, 2 e 3 (depois: lojas maiores e saque)
_items = {norm(t['name']): t for t in sim.load()['items']}
def stage_of(item):
    """item pode ser 'A / B' ou ter notas; usa o 1º nome reconhecível"""
    for part in re.split(r'[/,]', item):
        n = norm(part)
        if not n: continue
        if n in ST0: return 0
        if n in ST1: return 1
        if n in ST2: return 2
    return 3
_cache = {}
def kit_prog(cls_name, level, ap_per_battle=40, apmod=None, cat=None):
    key = (cls_name, level, ap_per_battle, tuple(sorted((apmod or {}).items())))
    if key not in _cache: _cache[key] = _kit_prog(cls_name, level, ap_per_battle, apmod)
    return _cache[key]
def _kit_prog(cls_name, level, ap_per_battle=40, apmod=None):
    """Retorna (lista de nomes de habilidades de ação aprendidas, lista de suportes) ao nível dado."""
    apmod = apmod or {}
    b = BATTLES.get(level) or int(round(level * 1.9)); budget = b * ap_per_battle
    avail = []
    for i, k in enumerate(KIT):
        if norm(k['cls']) != norm(cls_name) or k['type'] not in ('A', 'S'): continue
        if b < STAGE_AT[stage_of(k['item'])]: continue
        avail.append((apmod.get(k['name'], k['ap']), i, k))
    avail.sort(key=lambda x: (x[0], x[1])); A, S = [], []; used = 0
    for cost, i, k in avail:
        if used + cost > budget: continue
        used += cost
        (A if k['type'] == 'A' else S).append(k['name'])
    return A, S
if __name__ == '__main__':
    from collections import Counter
    c = Counter(); items_ = Counter()
    for k in KIT:
        if k['type'] in ('A', 'S'): c[stage_of(k['item'])] += 1
    print('habilidades por estágio de arma (0 inicial, 1 após 10, 2 após 20, 3 depois):', dict(c))
    for cn in ('Summoner', 'Bishop', 'Time Mage', 'Illusionist', 'Black Mage', 'Soldier', 'Fighter'):
        for lv in (10, 25, 45):
            for ap in (15, 40, 80):
                A, Sp = kit_prog(cn, lv, ap); print(cn, lv, 'AP/batalha', ap, len(A), A[:9])

# ---------- pré-requisitos de classe (A-abilities de outras classes), por raça ----------
INIT = {1: ['Soldier', 'Thief', 'Archer', 'White Mage', 'Black Mage'], 2: ['Warrior', 'White Monk'], 3: ['White Mage', 'Black Mage', 'Beastmaster'], 4: ['Fencer', 'White Mage', 'Archer'], 5: ['Thief', 'Black Mage', 'Animist']}
PREREQ = {
 1: {'Fighter': [('Soldier', 2)], 'Paladin': [('Soldier', 2)], 'Ninja': [('Thief', 2)], 'Hunter': [('Archer', 2)], 'Blue Mage': [('White Mage', 1), ('Black Mage', 1)], 'Illusionist': [('White Mage', 3), ('Black Mage', 5)]},
 2: {'Bishop': [('White Monk', 2)], 'Templar': [('White Monk', 2)], 'Dragoon': [('Warrior', 2)], 'Defender': [('Warrior', 2)], 'Gladiator': [('Warrior', 2)]},
 3: {'Time Mage': [('Black Mage', 5)], 'Illusionist': [('White Mage', 3), ('Black Mage', 5)], 'Alchemist': [('White Mage', 3), ('Black Mage', 5)], 'Sage': [('White Mage', 3), ('Beastmaster', 2)], 'Morpher': [('Beastmaster', 5)]},
 4: {'Red Mage': [('Fencer', 1)], 'Elementalist': [('Fencer', 1), ('White Mage', 1)], 'Sniper': [('Archer', 2)], 'Summoner': [('White Mage', 2), ('Elementalist', 2)], 'Assassin': [('Elementalist', 2), ('Sniper', 1)]},
 5: {'Time Mage': [('Black Mage', 5)], 'Gunner': [('Animist', 1)], 'Mog Knight': [('Animist', 1)], 'Juggler': [('Thief', 2)], 'Gadgeteer': [('Thief', 2)]}}
def _pool(cls, battles, apmod, kinds=('A',)):
    out = []
    for i, k in enumerate(KIT):
        if norm(k['cls']) != norm(cls) or k['type'] not in kinds: continue
        if battles < STAGE_AT[stage_of(k['item'])]: continue
        out.append((apmod.get(k['name'], k['ap']), i, k))
    out.sort(key=lambda x: (x[0], x[1])); return out
_cache2 = {}
EV = json.load(open(os.path.join(here, 'ability_ev.json')))
import sim as _sim
_ROLE = {}
def role(c):
    if not _ROLE:
        import sim as s_
        for k, v in s_.__dict__.items(): pass
    return 'mag' if c in ('White Mage', 'Black Mage', 'Illusionist', 'Alchemist', 'Sage', 'Time Mage', 'Red Mage', 'Elementalist', 'Summoner', 'Bishop', 'Blue Mage', 'Beastmaster', 'Morpher', 'Animist') else 'fis'
def plan(race, cls, level, ap_per_battle=40, apmod=None, battles=None, sec_rule='auto'):
    """Retorna dict(feasible, cost, kit_A, kit_S, prereq): custo para liberar a classe + habilidades próprias com o AP que sobra."""
    apmod = apmod or {}; b = battles if battles else int(round((BATTLES.get(level) or int(round(level * 1.9))) * BATT_MULT))
    key = (race, cls, b, ap_per_battle, tuple(sorted(apmod.items())), sec_rule)
    if key in _cache2: return _cache2[key]
    budget = b * ap_per_battle; learned = {}; cost = [0]; ok = [True]
    def unlock(c, seen=()):
        if c in seen: return
        for pc, n in PREREQ.get(race, {}).get(c, []):
            unlock(pc, seen + (c,))
            have = learned.setdefault(pc, [])
            pool = [x for x in _pool(pc, b, apmod) if x[2]['name'] not in have]
            need = n - len(have)
            if need > len(pool): ok[0] = False; return
            for cst, i, k in pool[:max(0, need)]: have.append(k['name']); cost[0] += cst
    if cls not in INIT.get(race, []): unlock(cls)
    res = dict(feasible=ok[0] and cost[0] <= budget, cost=cost[0], kit_A=[], kit_S=[], prereq=dict(learned))
    if res['feasible']:
        left = budget - cost[0]; A, S = [], []
        for cst, i, k in sorted(_pool(cls, b, apmod, ('A', 'S')), key=lambda x: (x[0], x[1])):
            if cst <= left: left -= cst; (A if k['type'] == 'A' else S).append(k['name'])
        res['kit_A'] = A; res['kit_S'] = S
        pre = PREREQ.get(race, {}).get(cls, [])
        res['kit_A_own'] = list(A); sec = None; secA = []
        prereq_cls = max(pre, key=lambda x: x[1])[0] if pre else None
        if sec_rule == 'prereq' or (sec_rule == 'auto' and level <= 15):
            if prereq_cls: sec = prereq_cls; secA = [a for a in learned.get(prereq_cls, []) if a not in A]
        elif sec_rule == 'auto':
            best = (-1, None, [])
            for c2 in set(INIT.get(race, [])) | set(learned.keys()):
                if c2 == cls: continue
                have = list(learned.get(c2, [])); lft = left
                for cst, i, k in _pool(c2, b, apmod):
                    if k['name'] in have: continue
                    if cst <= lft: lft -= cst; have.append(k['name'])
                top = sorted((EV.get(a, 0) for a in have), reverse=True)[:3]
                sc = sum(top) * (1.0 if role(c2) == role(cls) or c2 == 'White Mage' else MIX_W)
                if sc > best[0]: best = (sc, c2, have)
            if best[1]: sec = best[1]; secA = [a for a in best[2] if a not in A]
        res['sec_class'] = sec; res['kit_A'] = A + secA
    _cache2[key] = res; return res
