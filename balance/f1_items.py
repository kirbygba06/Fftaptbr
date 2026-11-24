# -*- coding: utf-8 -*-
"""F1: transformações de itens e magias (somente dados)."""
import copy
def new_atk(a):
    """Armas de loja (≤45 ATK) ficam como estão; só o topo de saque é comprimido (45 + 0,55·excesso): 87→68, 77→62, 65→56."""
    return int(round(a if a <= 45 else 45 + 0.55 * (a - 45)))
def fix_dominated(out):
    """Preço passa a ser crescente com o ATK dentro de cada tipo de arma de loja (regressão isotônica = menor mudança total de preços)."""
    changed = 0
    for ty in range(1, 20):
        L = sorted([t for t in out if t['type'] == ty and t['buy']], key=lambda t: (t['atk'], t['buy']))
        blocks = [[t['buy'], 1, [t]] for t in L]            # PAV
        k = 0
        while k < len(blocks) - 1:
            if blocks[k][0] / blocks[k][1] > blocks[k + 1][0] / blocks[k + 1][1] + 1e-9:
                a, b = blocks[k], blocks[k + 1]; blocks[k:k + 2] = [[a[0] + b[0], a[1] + b[1], a[2] + b[2]]]; k = max(0, k - 1)
            else: k += 1
        prev = 0
        for tot, n, ts in blocks:
            for t in ts:
                p = max(int(round(tot / n / 50.0) * 50), prev + 50, 150); prev = p
                if p != t['buy']: t['buy'] = p; changed += 1
    return changed
DEF_SLOTS = (20, 21, 22, 23, 24, 25, 26, 27, 28)
RES_SLOTS = (21, 22, 23, 24, 25, 26, 27, 28, 29)
def items_f1(items, wdef=2.0, wres=1.0, shield_eva=2.0):
    out = copy.deepcopy(items)
    mx = {}
    for t in out:
        mx[t['type']] = (max(mx.get(t['type'], (1, 1))[0], t['dfn']), max(mx.get(t['type'], (1, 1))[1], t['res']))
    for t in out:
        ty = t['type']
        if 1 <= ty <= 19:
            t['atk'] = new_atk(t['atk'])
        else:
            if ty in DEF_SLOTS: t['dfn'] = min(255, round(t['dfn'] * (1 + wdef * (t['dfn'] / mx[ty][0]) ** 4)))   # convexo: itens fracos quase iguais, topo ×3
            if ty in RES_SLOTS: t['res'] = min(255, round(t['res'] * (1 + wres * (t['res'] / mx[ty][1]) ** 4)))
            if ty == 20: t['eva'] = min(100, round(t['eva'] * shield_eva))
    fix_dominated(out)
    for t in out:
        if t['buy']: t['sell'] = t['buy'] // 2
    return out
SPELL = {}   # F1 NÃO mexe em poder/custo das magias: por ação já estão em 0,9–1,5× do ataque físico (ver metrics_result.md)
def abil_f1(abil, spell=SPELL):
    out = copy.deepcopy(abil)
    for n, (p, mp) in spell.items():
        if n in out: out[n]['power'] = p; out[n]['mp'] = mp
    return out
