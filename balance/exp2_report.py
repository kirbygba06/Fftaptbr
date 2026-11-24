# -*- coding: utf-8 -*-
import json, os, statistics as S, collections
import sim
J = {str(j['id']): j for j in sim.load()['jobs']}
race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
nm = lambda k: f"{J[k]['name']} ({race[J[k]['race']]})"
def load(n):
    p = f'exp2_{n}.json'
    return json.load(open(p)) if os.path.exists(p) else None
def stats(win): v = list(win.values()); return min(v), max(v), S.pstdev(v), sum(1 for x in v if x < .4 or x > .6)
def get(R, label, lv): return next((r for r in R if r['label'] == label and r['lv'] == lv), None)
def cls_win(r, name, rc=None): return [r['win'][k] for k, j in J.items() if j['name'] == name and (rc is None or j['race'] == rc)]
def mpavg(r): 
    v = [x for x in r['mp_unit'].values() if x > 0]; return S.mean(v) if v else 0
out = []
B = load('base')
if B:
    out.append('## A. Original x pacote de referência (bal10+bal11+bal01+bal02)\n| versão | nível | faixa | σ | fora de 40–60% | ações/batalha | MP gasto por unidade (média das que usam) |\n|---|---|---|---|---|---|---|')
    for lab in ('original', 'referencia'):
        for lv in (10, 25, 45, 50):
            r = get(B, lab, lv); a, b, s, o = stats(r['win']); out.append(f"| {lab} | {lv} | {a * 100:.0f}–{b * 100:.0f}% | {s:.3f} | {o} | {r['acts']:.0f} | {mpavg(r):.0f} |")
V = load('velocidade')
if V and B:
    out.append('\n## B. Compressão adicional de velocidade (sobre a referência)\n| versão | nível | σ | fora de 40–60% | ações | Assassin | Ninja | Thief (Hume) | Sage | Templar | corr(velocidade, vitória) |\n|---|---|---|---|---|---|---|---|---|---|---|')
    rows = [(l_, get(B, 'referencia', lv)) for l_ in ['referencia'] for lv in (10, 25, 45)] + [(r['label'], r) for r in V]
    for lab, r in sorted(rows, key=lambda x: (x[0] != 'referencia', x[0], x[1]['lv'])):
        a, b, s, o = stats(r['win']); sp = {k: j for k, j in J.items()}
        out.append(f"| {lab} | {r['lv']} | {s:.3f} | {o} | {r['acts']:.0f} | {S.mean(cls_win(r, 'Assassin')) * 100:.0f}% | {S.mean(cls_win(r, 'Ninja')) * 100:.0f}% | {S.mean(cls_win(r, 'Thief', 1)) * 100:.0f}% | {S.mean(cls_win(r, 'Sage')) * 100:.0f}% | {S.mean(cls_win(r, 'Templar')) * 100:.0f}% | – |")
H = load('haste')
if H and B:
    out.append('\n## C. Haste (original, isolado)\n| multiplicador | nível | σ | fora | ações | Time Mage (Nu Mou) | Time Mage (Moogle) | uso de Haste (% das ações do Time Mage) |\n|---|---|---|---|---|---|---|---|')
    rows = [('2.0 (original)', get(B, 'original', lv)) for lv in (10, 25, 45)] + [(r['label'].replace('haste ', ''), r) for r in H]
    for lab, r in sorted(rows, key=lambda x: (-float(x[0].split()[0]), x[1]['lv'])):
        a, b, s, o = stats(r['win']); u = r['use']; tm = sum(v for k, v in u.items() if k.startswith('Time Mage|Haste')); ta = max(1, r['n_act'].get('Time Mage', 1))
        out.append(f"| {lab} | {r['lv']} | {s:.3f} | {o} | {r['acts']:.0f} | {S.mean(cls_win(r, 'Time Mage', 3)) * 100:.0f}% | {S.mean(cls_win(r, 'Time Mage', 5)) * 100:.0f}% | {100 * tm / ta:.0f}% |")
C = load('capstones')
if C and B:
    out.append('\n## D. Habilidades finais (nível 50) e Quicken (original, isolado)\n| variante | nível | σ | fora | ações | Ninja | Red Mage | Time Mage (Nu Mou) |\n|---|---|---|---|---|---|---|---|')
    rows = [('original', get(B, 'original', 50))] + [(r['label'], r) for r in C if r['lv'] == 50] + [('original', get(B, 'original', lv)) for lv in (25, 45)] + [(r['label'], r) for r in C if r['lv'] in (25, 45)]
    for lab, r in rows:
        a, b, s, o = stats(r['win'])
        out.append(f"| {lab} | {r['lv']} | {s:.3f} | {o} | {r['acts']:.0f} | {S.mean(cls_win(r, 'Ninja')) * 100:.0f}% | {S.mean(cls_win(r, 'Red Mage')) * 100:.0f}% | {S.mean(cls_win(r, 'Time Mage', 3)) * 100:.0f}% |")
M = load('magias')
if M and B:
    out.append('\n## E. Magias de tier 2 e 3 (original, isolado)\n| variante | nível | σ | fora | ações | MP por unidade | Black Mage (Hume) | Black Mage (Nu Mou) | Red Mage | Elementalist |\n|---|---|---|---|---|---|---|---|---|---|')
    rows = [('original', get(B, 'original', lv)) for lv in (25, 45)] + [(r['label'], r) for r in M]
    for lab, r in sorted(rows, key=lambda x: (x[1]['lv'], x[0] != 'original', x[0])):
        a, b, s, o = stats(r['win'])
        out.append(f"| {lab} | {r['lv']} | {s:.3f} | {o} | {r['acts']:.0f} | {mpavg(r):.0f} | {S.mean(cls_win(r, 'Black Mage', 1)) * 100:.0f}% | {S.mean(cls_win(r, 'Black Mage', 3)) * 100:.0f}% | {S.mean(cls_win(r, 'Red Mage')) * 100:.0f}% | {S.mean(cls_win(r, 'Elementalist')) * 100:.0f}% |")
U = load('buffs')
if U:
    out.append('\n## F. Habilidades candidatas a buff: ablação, uso forçado e valor por ação\n| classe | habilidade | nível | vitória (normal) | ablação (Δ) | forçado (Δ) | % ações (normal) | valor esperado por uso | valor esperado do Fight | dano/impacto por uso (forçado) | turnos negados por uso (forçado) | status aplicado por uso |\n|---|---|---|---|---|---|---|---|---|---|---|---|')
    keys = []; [keys.append((r['label'], r['lv'])) for r in U if (r['label'], r['lv']) not in keys]
    for lab, lv in keys:
        g = lambda m: next(r for r in U if r['label'] == lab and r['lv'] == lv and r['mode'] == m)
        n_, a_, f_ = g('normal'), g('ablacao'), g('forcado'); cl, ab = lab.split(' ', 1) if not lab.startswith(('White Monk', 'Mog')) else ('White Monk', lab[len('White Monk '):])
        out.append(f"| {n_['cls']} | {n_['ab']} | {lv} | {n_['win'] * 100:.0f}% | {(a_['win'] - n_['win']) * 100:+.0f} | {(f_['win'] - n_['win']) * 100:+.0f} | {n_['share'] * 100:.0f}% | {f_['ev']:.0f} | {f_['ev_fight']:.0f} | {f_['impact']:.0f} | {f_['denied']:.0f} | {(100 * f_['succ'] / f_['uses']) if f_['uses'] else 0:.0f}% |")
CB = load('combo')
if CB and B:
    out.append('\n## G. JP e Combo (modelo paramétrico; original, nível 25 e 45)\n| regime de JP | fórmula | nível | σ | fora de 40–60% | ações/batalha | Combo (% das ações) | multiplicador médio do golpe final |\n|---|---|---|---|---|---|---|---|')
    out.append(f"| sem JP (jogo sem Combo) | – | 25 | {stats(get(B, 'original', 25)['win'])[2]:.3f} | {stats(get(B, 'original', 25)['win'])[3]} | {get(B, 'original', 25)['acts']:.0f} | 0% | – |")
    out.append(f"| sem JP (jogo sem Combo) | – | 45 | {stats(get(B, 'original', 45)['win'])[2]:.3f} | {stats(get(B, 'original', 45)['win'])[3]} | {get(B, 'original', 45)['acts']:.0f} | 0% | – |")
    for r in CB:
        a, b, s, o = stats(r['win']); reg, fl = r['label'].split(' | ')
        out.append(f"| {reg} | {fl} | {r['lv']} | {s:.3f} | {o} | {r['acts']:.0f} | {r['combo_share'] * 100:.0f}% | {r['mult']:.2f}× |")
HU = load('hunting')
if HU:
    out.append('\n## H. Hunting (Hunter, nível 45; JP só por abates)\n| versão | vitória do Hunter | JP ao fim da batalha | % de ações Hunting | % de ações Combo |\n|---|---|---|---|---|')
    for r in HU: out.append(f"| {r['label']} | {r['win'] * 100:.0f}% | {r['jp_end']:.1f} | {r['hunting_share'] * 100:.0f}% | {r['combo_share'] * 100:.0f}% |")
open('exp2_result.md', 'w').write('\n'.join(out)); print('\n'.join(out))
