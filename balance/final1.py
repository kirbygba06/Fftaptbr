# -*- coding: utf-8 -*-
"""Rebalance FINAL v1 (somente dados, sem ASM). Monta o spec completo e roda variantes/ablações.
Camadas: classes (f1 k5 + orçamento por classe), itens (f1_items, atk×1,12), habilidades (final3 + Rodada 8 + área seletiva),
magias (tier 2/3 + trio Fogo/Gelo/Raio)."""
import os, sys, copy
os.environ.setdefault('PROG', '2'); os.environ.setdefault('APB', '40'); os.environ.setdefault('SEC', '1')
import exp8_round as R, exp9_area as A, exp4_classes as C, exp11_trio as T
TRIO = T.trio(1.10, 0.80, 0.90)
ELEM_AREA = {n: {'power': 40, 'mp': 10} for n in ('Heavy Dust', 'Sliprain', 'Shining Air')}  # compensação da área (Elementalist)
HASTE1 = {'Haste': {'area': 'One Unit', 'mp': 20}}          # desfaz a área do Haste (Templar S), MP 24 -> 20
ROCK = {'Rockseal': {'mp': 40}}                               # Assassin usava Rockseal em 63% das ações no nível 45
NUDGE = {**C.kb(['Paladin'], 1.06), **C.kb(['Defender', 'Fighter', 'Archer', 'Ninja', 'Sniper'], 1.05)}
def build(trio=True, rm=True, elem=True, haste=True, rock=True, nudge=True):
    sp = copy.deepcopy(A.spec_for('sel')); m = sp['mods']
    if trio: m = A.merge(m, TRIO)
    if elem: m = A.merge(m, ELEM_AREA)
    if haste: m = A.merge(m, HASTE1)
    if rock: m = A.merge(m, ROCK)
    sp['mods'] = m; ks = dict(sp['kscale'])
    if rm: ks.update(C.kb(['Red Mage'], 1.0))
    if nudge: ks.update(NUDGE)
    sp['kscale'] = ks; return sp
HASTE2 = {'Haste': {'area': 'One Unit', 'mp': 24}}
F2_ABIL = {'Toad': {'area': 'r1/v2', 'mp': 36}, 'Last Breath': {'mp': 32}, **{n: {'mp': 4} for n in ('Confushot', 'Charmshot', 'Stopshot', 'Blindshot', 'Silenshot')}}
NUDGE2 = {**C.kb(['Paladin'], 1.10), **C.kb(['Defender', 'Fighter'], 1.05), **C.kb(['Archer', 'Ninja', 'Sniper'], 1.08), **C.kb(['Fencer'], 1.12),
          **C.kb(['Illusionist'], 0.85), **C.kb(['Templar'], 0.95)}
def build2():
    sp = build(); sp['mods'] = A.merge(A.merge(sp['mods'], HASTE2), F2_ABIL); sp['kscale'] = {**sp['kscale'], **NUDGE2}; return sp
import exp3
UNMOD = ['Blue Mage', 'Thief', 'Morpher', 'Beastmaster', 'Gadgeteer']   # kits não modelados: só o ajuste global (atk×1,12), sem orçamento próprio
def build3():
    sp = build2(); ks = dict(sp['kscale'])
    for n in UNMOD:
        for i in C.jj(n): ks[i] = 1.0 / exp3.k5[i]
    ks.update(C.kb(['Time Mage'], 0.85)); ks.update(C.kb(['Alchemist'], 0.92)); ks.update(C.kb(['Templar'], 0.90))
    sp['kscale'] = ks; return sp
VARS = {'F0': dict(haste=False, rock=False, nudge=False), 'F1': {}, 'F1_semhaste': dict(haste=False), 'F1_semnudge': dict(nudge=False)}
if __name__ == '__main__':
    k = sys.argv[1]; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 101; tag = sys.argv[3] if len(sys.argv) > 3 else ''
    sp = build2() if k == 'F2' else build3() if k == 'F3' else build(**VARS[k])
    R.run_team_n('fin_' + k + tag, sp, {'25': 12000, '10': 4000, '45': 6000}, seed=seed)
