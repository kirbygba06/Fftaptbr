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
ST1 = {norm(x) for x in S1}; ST2 = {norm(x) for x in S2}
BATTLES = {10: 12, 25: 40, 45: 90, 50: 100}          # SUPOSIÇÃO: batalhas jogadas ao chegar no nível
STAGE_AT = {0: 0, 1: 10, 2: 20, 3: 35}                 # batalhas para o estoque 0 (inicial), 1, 2 e 3 (depois: lojas maiores e saque)
_items = {norm(t['name']): t for t in sim.load()['items']}
def stage_of(item):
    """item pode ser 'A / B' ou ter notas; usa o 1º nome reconhecível"""
    for part in re.split(r'[/,]', item):
        n = norm(part)
        if not n: continue
        if n in ST1: return 1
        if n in ST2: return 2
        t = _items.get(n)
        if t is not None: return 0 if (t['buy'] and t['buy'] <= 1200) else 3
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
