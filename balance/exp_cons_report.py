# -*- coding: utf-8 -*-
import json, collections, statistics as S
R = json.load(open('exp_cons_raw.json'))
ORDER = ['Rockseal', 'Charmshot', 'Cupid', 'Fire Veil', 'Death Sickle', 'Checkmate']
def agg(rows, key):
    return S.mean(r[key] for r in rows)
out = []
for obs, title in ((0, 'Modo A – acerto de status pela fórmula do guia (SRes 50)'), (1, 'Modo B – acerto de status = precisão registrada pela comunidade (Rockseal 60%, Charmshot 95%, Cupid 80%, Checkmate 60%, Death Sickle 60%)')):
    out.append(f'\n## {title}\n')
    for ab in ORDER:
        rows = [r for r in R if r['obs'] == obs and r['ab'] == ab]
        if not rows: continue
        variants = []
        for r in rows:
            if r['variant'] not in variants: variants.append(r['variant'])
        cls = sorted({r['cls'] for r in rows})
        out.append(f'### {ab} (classe: {", ".join(cls)})\n')
        out.append('| variante | nível | vitória da classe | % das ações da classe | sucesso do status | impacto por uso (PV) | turnos negados por uso (valor) |\n|---|---|---|---|---|---|---|')
        base = {lv: [r for r in rows if r['variant'] == 'original' and r['lv'] == lv] for lv in (10, 25, 45)}
        for v in variants:
            for lv in (10, 25, 45):
                rr = [r for r in rows if r['variant'] == v and r['lv'] == lv]
                if not rr: continue
                w = agg(rr, 'win'); b = agg(base[lv], 'win'); sh = agg(rr, 'share')
                att = sum(r['att'] for r in rr); suc = sum(r['succ'] for r in rr)
                out.append(f"| {v} | {lv} | {w * 100:.1f}% ({(w - b) * 100:+.1f}) | {sh * 100:.0f}% | {('%.0f%%' % (100 * suc / att)) if att else '–'} | {agg(rr, 'impact'):.0f} | {agg(rr, 'denied'):.0f} |")
        out.append('')
open('exp_cons_result.md', 'w').write('\n'.join(out)); print('\n'.join(out)[:200])
