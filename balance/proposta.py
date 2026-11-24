# -*- coding: utf-8 -*-
"""Gera a proposta de rebalanceamento (somente números) -> proposta_classes.csv, proposta_itens.csv, proposta_magias.csv
Regras explicadas em PROPOSTA.md. Não altera a ROM."""
import csv, math, os
from romdata import *
here = os.path.dirname(__file__)
J = [j for j in jobs() if j['race'] in (1, 2, 3, 4, 5) and j['name'] and j['name'] != '?' and j['hp'] and j['id'] < 0x39]
ROLE = {}
for n in ['Paladin', 'Templar', 'Defender', 'Warrior', 'Mog Knight', 'Soldier', 'Gadgeteer']: ROLE[n] = 'guardiao'
for n in ['Fighter', 'Dragoon', 'Gladiator', 'Sniper', 'Hunter', 'Archer', 'Gunner']: ROLE[n] = 'atacante'
for n in ['Thief', 'Ninja', 'Assassin', 'Fencer', 'White Monk', 'Juggler']: ROLE[n] = 'agil'
for n in ['Black Mage', 'Red Mage', 'Illusionist', 'Elementalist', 'Summoner', 'Alchemist', 'Sage']: ROLE[n] = 'mago'
for n in ['White Mage', 'Bishop', 'Animist', 'Time Mage', 'Beastmaster', 'Morpher', 'Blue Mage']: ROLE[n] = 'apoio'
# multiplicadores de crescimento por papel: hp, mp, atk, def, pow, res
M = {'guardiao': (1.12, 0.9, 0.98, 1.12, 0.92, 1.05), 'atacante': (0.98, 0.9, 1.10, 0.95, 0.90, 0.95),
     'agil': (0.92, 0.95, 1.02, 0.92, 0.98, 0.96), 'mago': (0.92, 1.0, 0.88, 0.92, 1.12, 1.10), 'apoio': (1.0, 1.0, 0.92, 1.0, 1.05, 1.12)}
MOVJ = {'guardiao': (3, 2), 'atacante': (4, 3), 'agil': (5, 4), 'mago': (3, 2), 'apoio': (4, 2)}
SRES = {'guardiao': 65, 'atacante': 50, 'agil': 35, 'mago': 45, 'apoio': 60}
def L50(b, g): return b * 1.05 + g * 49
rows = []
for j in J:
    r = ROLE.get(j['name'], 'atacante'); m = M[r]
    spd_b = round(100 + 0.7 * (j['spd'] - 100)); spd_g = round(1.2 + 0.5 * (j['g_spd'] - 1.2), 1)
    new = dict(id=j['id'], nome=j['name'], papel=r, spd_base=spd_b, g_spd=spd_g,
               g_hp=round(j['g_hp'] * m[0], 1), g_mp=round(j['g_mp'] * m[1], 1), g_atk=round(j['g_atk'] * m[2], 1),
               g_def=round(j['g_def'] * m[3], 1), g_pow=round(j['g_pow'] * m[4], 1), g_res=round(j['g_res'] * m[5], 1),
               mov=MOVJ[r][0], jmp=MOVJ[r][1], sres=SRES[r], mov_old=j['mov'], jmp_old=j['jmp'],
               spd50_old=round(L50(j['spd'], j['g_spd'])), spd50=round(L50(spd_b, spd_g)),
               atk50_old=round(L50(j['atk'], j['g_atk'])), atk50=round(L50(j['atk'], j['g_atk'] * m[2])),
               def50_old=round(L50(j['dfn'], j['g_def'])), def50=round(L50(j['dfn'], j['g_def'] * m[3])),
               hp50_old=round(L50(j['hp'], j['g_hp'])), hp50=round(L50(j['hp'], j['g_hp'] * m[0])),
               pow50_old=round(L50(j['pow'], j['g_pow'])), pow50=round(L50(j['pow'], j['g_pow'] * m[4])))
    rows.append(new)
with open(os.path.join(here, 'proposta_classes.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def spread(k): v = [r[k] for r in rows]; return round(max(v) / min(v), 2)
print('classes', len(rows))
for a in ('spd50', 'atk50', 'def50', 'hp50', 'pow50'): print(a, 'antes', spread(a + '_old') if a + '_old' in rows[0] else '', 'depois', spread(a))
# itens
I = items()
def newatk(a): return round(30 + (a - 15) * 0.55)
def newprice(atk): return int(round(300 * (atk / 36) ** 6.0 / 50.0) * 50)
out = []
for t in I:
    if not t['name']: continue
    d = dict(idx=t['idx'], nome=t['name'], tipo=t['type'], buy=t['buy'], sell=t['sell'], atk=t['atk'], dfn=t['dfn'], res=t['res'])
    if 1 <= t['type'] <= 19:
        d['atk_novo'] = newatk(t['atk']); d['buy_novo'] = newprice(d['atk_novo']) if t['buy'] else 0
    elif 20 <= t['type'] <= 29:
        d['dfn_novo'] = min(255, round(t['dfn'] * 1.7)); d['res_novo'] = min(255, round(t['res'] * 1.5)); d['buy_novo'] = t['buy']
    else: d['buy_novo'] = t['buy']
    d['sell_novo'] = d['buy_novo'] // 2 if d.get('buy_novo') else 0
    out.append(d)
cols = ['idx', 'nome', 'tipo', 'buy', 'sell', 'atk', 'dfn', 'res', 'atk_novo', 'dfn_novo', 'res_novo', 'buy_novo', 'sell_novo']
with open(os.path.join(here, 'proposta_itens.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
W = [d for d in out if 'atk_novo' in d]
print('armas: atk antes', min(d['atk'] for d in W), max(d['atk'] for d in W), 'depois', min(d['atk_novo'] for d in W), max(d['atk_novo'] for d in W))
print('exemplos', [(d['nome'], d['atk'], d['atk_novo'], d['buy'], d['buy_novo']) for d in W if d['nome'] in ('Short Sword', 'Estreledge', 'Masamune', 'Paraiba Blade', 'Sun Blade', 'Khukuri', 'Tiptaptwo', 'Excalibur2', 'Lohengrin')])
# dano exemplo novo: lutador L50 atk 547*1.10? vs soldado
def dano(att, eq, dfn, dfeq): return max(1, att + eq - (dfn + dfeq) // 2) * eq // 100
print('dano antigo arma 17/45/87:', dano(547, 17, 524, 40), dano(547, 45, 524, 40), dano(547, 87, 524, 40))
print('dano novo  arma', newatk(17), newatk(45), newatk(87), ':', dano(547, newatk(17), 524, 68), dano(547, newatk(45), 524, 68), dano(547, newatk(87), 524, 68))
# magias
A = abilities()
mag = {'Fire': (30, 6), 'Fira': (50, 14), 'Firaga': (80, 30), 'Thunder': (30, 6), 'Thundara': (50, 14), 'Thundaga': (80, 30), 'Blizzard': (30, 6), 'Blizzara': (50, 14), 'Blizzaga': (80, 30),
       'Cure': (40, 6), 'Cura': (65, 14), 'Curaga': (95, 28)}
with open(os.path.join(here, 'proposta_magias.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'nome', 'poder', 'mp', 'poder_novo', 'mp_novo'])
    for a in A:
        if a['name'] in mag and a['power']: w.writerow([a['idx'], a['name'], a['power'], a['mp'], mag[a['name']][0], mag[a['name']][1]])
