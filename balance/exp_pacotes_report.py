# -*- coding: utf-8 -*-
import json, statistics as S, collections
import sim
import os
R = json.load(open('exp_pacotes_raw.json')) + (json.load(open('exp_pacotes_raw2.json')) if os.path.exists('exp_pacotes_raw2.json') else []); J = {j['id']: j for j in sim.load()['jobs']}
names = []; [names.append(r['name']) for r in R if r['name'] not in names]
FOCUS = {'Gunner/5': 'Gunner', 'Archer/1': 'Archer (Hume)', 'Archer/4': 'Archer (Viera)', 'Ninja/1': 'Ninja', 'Assassin/4': 'Assassin', 'Sniper/4': 'Sniper', 'Fencer/4': 'Fencer'}
fid = {f"{j['name']}/{j['race']}": i for i, j in J.items()}
out = []
for obs, title in ((0, 'Modo A (acerto de status pela fórmula)'), (1, 'Modo B (precisão registrada pela comunidade)')):
    out.append(f'\n## {title}\n')
    out.append('### Equilíbrio global (42 classes)\n| pacote | nível | faixa de vitória | desvio | ações/batalha |\n|---|---|---|---|---|')
    for nm in names:
        for lv in (10, 25, 45):
            r = next(x for x in R if x['name'] == nm and x['lv'] == lv and x['obs'] == obs); v = list(r['win'].values())
            out.append(f"| {nm} | {lv} | {min(v) * 100:.0f}%–{max(v) * 100:.0f}% | {S.pstdev(v):.3f} | {r['acts']:.0f} |")
    out.append('\n### Classes afetadas e as que mais vencem (taxa de vitória)\n| classe | nível | ' + ' | '.join(names) + ' |\n|---|---|' + '---|' * len(names))
    for k, lab in FOCUS.items():
        for lv in (25, 45):
            row = []
            base = next(x for x in R if x['name'] == 'original' and x['lv'] == lv and x['obs'] == obs)['win'][str(fid[k])]
            for nm in names:
                w = next(x for x in R if x['name'] == nm and x['lv'] == lv and x['obs'] == obs)['win'][str(fid[k])]
                row.append(f'{w * 100:.0f}% ({(w - base) * 100:+.0f})' if nm != 'original' else f'{w * 100:.0f}%')
            out.append(f'| {lab} | {lv} | ' + ' | '.join(row) + ' |')
    out.append('\n### Identidade: composição das ações (nível 45) – dano / controle / dano+controle / apoio\n| classe | ' + ' | '.join(names) + ' |\n|---|' + '---|' * len(names))
    for k, lab in FOCUS.items():
        cn = k.split('/')[0]; row = []
        for nm in names:
            r = next(x for x in R if x['name'] == nm and x['lv'] == 45 and x['obs'] == obs); d = r['roles'].get(cn, {}); t = max(1, sum(d.values()))
            row.append(' / '.join(f"{100 * d.get(c, 0) / t:.0f}" for c in ('dano', 'controle', 'dano+controle', 'apoio')))
        out.append(f'| {lab} | ' + ' | '.join(row) + ' |')
    out.append('\n### Sucesso dos status e valor por uso (nível 45)\n| habilidade | pacote | usos | status aplicado por uso | impacto por uso (PV) | turnos negados por uso (valor) |\n|---|---|---|---|---|---|')
    for ab in ('Rockseal', 'Charmshot', 'Cupid', 'Fire Veil', 'Death Sickle', 'Checkmate', 'Stopshot', 'Confushot'):
        for nm in names:
            r = next(x for x in R if x['name'] == nm and x['lv'] == 45 and x['obs'] == obs)
            uses = sum(v for k, v in r['use'].items() if k.endswith('|' + ab))
            if not uses: continue
            att = r['att'].get(ab, 0); suc = r['succ'].get(ab, 0)
            out.append(f"| {ab} | {nm} | {uses} | {('%.0f%%' % (100 * suc / uses)) if suc else '–'} (condicional: {('%.0f%%' % (100 * suc / att)) if att else '–'}) | {r['impact'].get(ab, 0) / uses:.0f} | {r['denied'].get(ab, 0) / uses:.0f} |")
open('exp_pacotes_result.md', 'w').write('\n'.join(out)); print('ok')
