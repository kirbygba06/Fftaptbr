# -*- coding: utf-8 -*-
"""Métricas ATUAL vs F1: escala do equipamento, eficiência de magia, MP, duração de batalha."""
import json, random, statistics as S, sim, f1
scn0 = sim.load(); k = {int(a): b for a, b in json.load(open('f1_k.json')).items()}; scn1 = f1.build(scn0, k)
def avg(scn, prof, lv, key):
    J = [j for j in scn['jobs'] if sim.PROFILE.get(j['name']) == prof]
    return S.mean(j[{'atk': 'atk', 'dfn': 'dfn', 'pw': 'pow', 'rs': 'res', 'hp': 'hp'}[key]] * 1.05 + j[{'atk': 'g_atk', 'dfn': 'g_def', 'pw': 'g_pow', 'rs': 'g_res', 'hp': 'g_hp'}[key]] * (lv - 1) for j in J)
print('## Equipamento: dano causado e recebido pelo mesmo personagem ao subir de faixa de loja (faixa 1 = 100%)')
for name, scn in (('ATUAL', scn0), ('F1', scn1)):
    g = sim.gear(scn['items']); row = []
    for lv in (10, 25, 38, 45):
        t = sim.tier(lv)
        A, D = avg(scn, sim.PHYS, lv, 'atk'), avg(scn, sim.PHYS, lv, 'dfn')
        off = lambda tt: max(1, A + g['wep'][tt] - D / 2) * g['wep'][tt] / 100
        dm = lambda tt: max(1, A - (D + g['phys_def'][tt]) / 2) * 0.35     # dano recebido de uma arma 35 de mesmo nível
        row.append(f'L{lv}: ataque {off(t) / off(0) * 100:.0f}% · dano recebido {dm(t) / dm(0) * 100:.0f}%')
    print(f'- {name}:', ' | '.join(row))
print('\n## Magia (mago nível 25 e 45 contra alvo de RM médio): dano por ação relativo a um ataque físico de atacante do mesmo nível')
for name, scn in (('ATUAL', scn0), ('F1', scn1)):
    g = sim.gear(scn['items']); sp, hl = sim.spells(scn['abil']); out = []
    for lv in (10, 25, 45):
        t = sim.tier(lv); PM = avg(scn, sim.MAGE, lv, 'pw') + g['rod_pow'][t]; RS = avg(scn, sim.PHYS, lv, 'rs') + g['phys_res'][t]
        A, D = avg(scn, sim.PHYS, lv, 'atk'), avg(scn, sim.PHYS, lv, 'dfn') + g['phys_def'][t]
        phys = max(1, A + g['wep'][t] - D / 2) * g['wep'][t] / 100
        tiers = [max(1, PM - RS / 2) * p / 100 / phys for p, _ in sp]
        out.append(f'L{lv}: Fire {tiers[0]:.2f}× / Fira {tiers[1]:.2f}× / Firaga {tiers[2]:.2f}×')
    print(f'- {name}:', ' | '.join(out))
print('\n## MP: magias de tier 3 que um mago consegue lançar (MP total / custo) e % de turnos sem MP em batalha')
for name, scn in (('ATUAL', scn0), ('F1', scn1)):
    sp, _ = sim.spells(scn['abil']); g = sim.gear(scn['items']); rng = random.Random(5); res = []
    for lv in (25, 45):
        MG = [j for j in scn['jobs'] if sim.PROFILE.get(j['name']) == sim.MAGE]
        mp = S.mean(j['mp'] * 1.05 + j['g_mp'] * (lv - 1) for j in MG)
        dry = act_ = 0
        for _ in range(500):
            A = [sim.mk(j, lv, g, scn['abil'], {}) for j in rng.sample(MG, 3)]; B = [sim.mk(j, lv, g, scn['abil'], {}) for j in rng.sample(scn['jobs'], 3)]
            sim.battle(A, B, sp, sim.spells(scn['abil'])[1], rng)
            for u in A: dry += u.get('dry', 0); act_ += u.get('dry', 0) + u.get('casts', 0)
        res.append(f'L{lv}: MP {mp:.0f} → {mp / sp[2][1]:.0f} Firaga · {100 * dry / max(1, act_):.0f}% das ações de mago sem MP')
    print(f'- {name}:', ' | '.join(res))
print('\n## Duração de batalha 3x3 (ações totais até o fim)')
for name, scn in (('ATUAL', scn0), ('F1', scn1)):
    rng = random.Random(9); g = sim.gear(scn['items']); sp, hl = sim.spells(scn['abil']); o = []
    for lv in (10, 25, 45):
        v = []
        for _ in range(600):
            A = [sim.mk(j, lv, g, scn['abil'], {}) for j in rng.sample(scn['jobs'], 3)]; B = [sim.mk(j, lv, g, scn['abil'], {}) for j in rng.sample(scn['jobs'], 3)]
            sim.battle(A, B, sp, hl, rng); v.append(sim.LAST['acts'])
        o.append(f'L{lv}: {S.mean(v):.0f}')
    print(f'- {name}:', ' | '.join(o))
print('\n## Velocidade: ações por 1000 ticks (nível 45) – mais rápida / mais lenta')
for name, scn in (('ATUAL', scn0), ('F1', scn1)):
    v = [j['spd'] * 1.05 + j['g_spd'] * 44 for j in scn['jobs']]; print(f'- {name}: {max(v) / 1:.0f} / {min(v):.0f} = {max(v) / min(v):.2f}×')
