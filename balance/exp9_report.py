# -*- coding: utf-8 -*-
import json, statistics as S, collections
import sim
from exp9_area import SUP, OFF
J = {str(j['id']): j for j in sim.load()['jobs']}; race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
files = dict(base='exp3_team_v2_base.json', sup='exp3_team_v2_area_sup.json', off='exp3_team_v2_area_off.json')
D = {k: json.load(open(v)) for k, v in files.items()}
def stats(T):
    out = {}
    for lv in ('25', '45'):
        d = T[lv]; best = {}
        for key, n in d['evalln'].items():
            if n < 200: continue
            c, ab = key.split('|', 1); best[c] = max(best.get(c, 0), d['evall'].get(key, 0) / n)
        for key, n in d['evalln'].items():
            if n < 200: continue
            c, ab = key.split('|', 1)
            if (c, ab) not in out: out[(c, ab)] = (d['best'].get(key, 0) / n, (d['evall'].get(key, 0) / n) / best[c] if best[c] else 0, lv)
    return out
St = {k: stats(v) for k, v in D.items()}
eff = lambda n, lv, k: 25 * D[n][lv]['coef'][k] if k in D[n][lv]['avail'] else None
out = ['## Habilidades fracas em área (raio 1) – equipes de 5, mapa variável, progressão real\n', 'Cada alvo extra de um efeito benéfico tem 25% de chance de ser um inimigo (e as ofensivas podem acertar aliados), para não superestimar as áreas.\n',
       '| versão | desvio entre classes 25 / 45 | ações por batalha 25 / 45 | classes fora de ±5 pp (25) |', '|---|---|---|---|']
for n, lab in (('base', 'base (pacote + 25 habilidades seletivas)'), ('sup', '+ área nas 10 de suporte'), ('off', '+ área nas 15 ofensivas/status')):
    cl = lambda lv: [eff(n, lv, k) for k in J if eff(n, lv, k) is not None]
    out.append(f"| {lab} | {S.pstdev(cl('25')):.1f} / {S.pstdev(cl('45')):.1f} | {D[n]['25']['acts']:.0f} / {D[n]['45']['acts']:.0f} | {sum(1 for x in cl('25') if abs(x) > 5)} |")
for n, lst, titulo in (('sup', SUP, 'Suporte'), ('off', OFF, 'Ofensivas e de status')):
    out.append(f'\n### {titulo}: escolha e valor antes e depois da área\n\n| habilidade | classe | escolha antes → depois | valor relativo à melhor da classe antes → depois | maior participação em uma classe |\n|---|---|---|---|---|')
    ok = 0
    for ab in lst:
        cs = [c for (c, a) in St['base'] if a == ab and (c, a) in St[n]]
        if not cs: out.append(f'| {ab} | – | sem dados (habilidade não disponível com n suficiente) | | |'); continue
        c = max(cs, key=lambda x: St[n][(x, ab)][0]); b = St['base'][(c, ab)]; a = St[n][(c, ab)]
        ok += a[0] >= 0.03
        out.append(f'| {ab} | {c} | {100*b[0]:.1f}% → **{100*a[0]:.1f}%** | {b[1]:.2f} → {a[1]:.2f} | {"> 20%: vira habilidade dominante" if a[0] > 0.2 else ""} |')
    out.append(f'\n**{ok} de {len(lst)} chegam a ≥ 3% de escolha.**')
    sh = sorted(((eff(n, '25', k) - eff('base', '25', k), k) for k in J if eff(n, '25', k) is not None and eff('base', '25', k) is not None))
    out.append('Classes que mais mudam (nível 25): ' + '; '.join(f"{J[k]['name']} ({race[J[k]['race']]}) {d:+.1f}" for d, k in sh[:4] + sh[-5:]))
open('exp9_result.md', 'w').write('\n'.join(out)); print('\n'.join(out))
