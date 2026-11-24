# -*- coding: utf-8 -*-
import json, os, csv, statistics as S
import sim
J = {str(j['id']): j for j in sim.load()['jobs']}; race = {1: 'Hume', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}
nm = lambda k: f"{J[k]['name']} ({race[J[k]['race']]})"
def L(n):
    p = f'exp3_team_{n}.json'; return json.load(open(p)) if os.path.exists(p) else None
T = {n: L(n) for n in ('orig', 'r2', 'fix')}
out = []
if T['orig']:
    out.append('## 1. Efeito de cada classe na EQUIPE (5 contra 5, mapa variável)\nRegressão logística: a equipe que tem a classe vence quantos pontos percentuais a mais do que com uma classe média no lugar. Barra de erro ≈ ±1,0 ponto.\n')
    up = lambda d, lv, k: 25 * d[lv]['coef'][k]
    se = lambda d, lv, k: 25 * d[lv]['se'][k]
    for lab, d in T.items():
        if not d: continue
        sd = {lv: S.pstdev([up(d, lv, k) for k in J]) for lv in ('10', '25', '45')}
        big = {lv: sum(1 for k in J if abs(up(d, lv, k)) > 3) for lv in ('10', '25', '45')}
        out.append(f"- **{ {'orig': 'Original', 'r2': 'R2 (classes+itens+Gunner)', 'fix': 'Original + pacote de correções'}[lab] }**: desvio do efeito por classe {sd['10']:.1f} / {sd['25']:.1f} / {sd['45']:.1f} pp; classes com efeito > ±3 pp: {big['10']} / {big['25']} / {big['45']}; ações por batalha {d['10']['acts']:.0f} / {d['25']['acts']:.0f} / {d['45']['acts']:.0f}")
    order = sorted(J, key=lambda k: S.mean(up(T['orig'], lv, k) for lv in ('10', '25', '45')))
    out.append('\n| classe | Original 10/25/45 (pp) | R2 | Original + correções |\n|---|---|---|---|')
    def row(k):
        cells = []
        for lab in ('orig', 'r2', 'fix'):
            d = T[lab]
            cells.append(' / '.join(f'{up(d, lv, k):+.0f}' for lv in ('10', '25', '45')) if d else '–')
        return f'| {nm(k)} | ' + ' | '.join(cells) + ' |'
    out.append('**Piores 12 (efeito médio no original)**'); out.append('\n'.join(row(k) for k in order[:12]))
    out.append('\n**Melhores 8**'); out.append('| classe | Original | R2 | Original + correções |\n|---|---|---|---|'); out.append('\n'.join(row(k) for k in order[-8:]))
    # habilidades menos usadas
    d = T['orig']; rows = []
    for lv in ('10', '25', '45'):
        ev = {}; 
        for key, n_ in d[lv]['evalln'].items():
            c, ab = key.split('|', 1); ev.setdefault(c, {})[ab] = (d[lv]['evall'][key] / max(1, n_), d[lv]['best'].get(key, 0) / max(1, n_), n_)
        for c, abs_ in ev.items():
            mx = max(v[0] for v in abs_.values()) or 1
            for ab, (m, ch, n_) in abs_.items(): rows.append((c, lv, ab, round(m, 1), round(100 * m / mx), round(100 * ch, 1), n_))
    with open('abilidades_uso_5v5.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['classe', 'nivel', 'habilidade', 'valor_medio_quando_disponivel', 'valor_%_do_melhor_da_classe', 'escolhida_%_das_vezes_disponivel', 'vezes_disponivel']); w.writerows(sorted(rows))
    out.append('\n## 2. Habilidades menos usadas por classe (nível 45; escolhida = % das vezes em que estava disponível e foi a melhor opção; valor = valor esperado médio quando disponível, em % da melhor habilidade da classe)\n| classe | habilidades menos escolhidas (escolhida%, valor%) |\n|---|---|')
    byc = {}
    for c, lv, ab, m, rel, ch, n_ in rows:
        if lv == '45' and ab != 'Fight' and n_ >= 200: byc.setdefault(c, []).append((ch, rel, ab))
    for c in sorted(byc):
        l = sorted(byc[c])[:3]; out.append(f"| {c} | " + '; '.join(f'{ab} ({ch:.0f}%, {rel}%)' for ch, rel, ab in l) + ' |')
FX = json.load(open('exp3_fix_raw.json')) if os.path.exists('exp3_fix_raw.json') else None
if FX:
    out.append('\n## 3. Testes de melhoria (5 contra 5, mapa variável; a classe sempre no time A; 2.000 batalhas por ponto)\nΔ = diferença para o original da mesma classe e nível. Diferenças < 5 pontos não são conclusivas.\n')
    labs = []; [labs.append(r['label']) for r in FX if r['label'] not in labs]
    keys = []; [keys.append((r['cls'])) for r in FX if r['cls'] not in keys]
    out.append('| variante | classe | nível 10 | nível 25 | nível 45 | ações/batalha (25) | MP gasto (25) | habilidades mais usadas (nível 45) |\n|---|---|---|---|---|---|---|---|')
    base = {(r['cls'], r['lv']): r for r in FX if r['label'] == 'original'}
    for lab in labs:
        for c in keys:
            rr = {r['lv']: r for r in FX if r['label'] == lab and r['cls'] == c}
            if len(rr) < 3: continue
            cells = []
            for lv in (10, 25, 45):
                w = rr[lv]['win'] * 100; b = base[(c, lv)]['win'] * 100
                cells.append(f'{w:.0f}%' if lab == 'original' else f'{w:.0f}% ({w - b:+.0f})')
            out.append(f"| {lab} | {c} | {' | '.join(cells)} | {rr[25]['acts']:.0f} | {rr[25]['mp']:.0f} | {rr[45]['top']} |")
open('exp3_result.md', 'w').write('\n'.join(out)); print('\n'.join(out)[:6000])
