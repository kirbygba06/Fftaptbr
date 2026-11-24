# -*- coding: utf-8 -*-
"""Lista de habilidades pouco usadas (pacote atual, progressão real) e a alavanca de dado disponível para cada uma."""
import json, collections
import sim2, exp3, exp4_teams_specs as SP
T = json.load(open('exp3_team_q2_final3.json'))
def effective(name):
    a = sim2.CAT[sim2.norm(name)]; mp, pw, area = a.mp, a.power, a.area
    for mods in (exp3.AB, exp3.FINAL_MODS, SP.SPECS['final3'].get('mods', {})):
        m = mods.get(a.name) if isinstance(mods, dict) else None
        if m is None: continue
        if isinstance(m, dict): mp = m.get('mp', mp); pw = m.get('power', pw); area = m.get('area', area)
        else: mp = m
    return mp, pw, area
def underused(lvs=('25', '45'), thr=0.03):
    rows = {}
    for lv in lvs:
        d = T[lv]
        for key, n in d['evalln'].items():
            if n < 200: continue
            c, ab = key.split('|', 1)
            if ab == 'Fight' or sim2.norm(ab) not in sim2.CAT: continue
            share = d['best'].get(key, 0) / n; ev = d['evall'].get(key, 0) / n
            rows.setdefault((c, ab), {})[lv] = (share, ev, n)
    out = []
    for (c, ab), v in rows.items():
        lv = '25' if '25' in v else '45'
        share, ev, n = v[lv]
        a = sim2.CAT[sim2.norm(ab)]
        modeled = any(e['kind'] != 'noop' and not (e['kind'] == 'dmg' and not a.basis) for e in a.eff)
        best_ev = max(x[1] for (cc, aa), vv in rows.items() if cc == c for x in [vv.get('25', vv.get('45'))])
        mp, pw, area = effective(ab)
        if share < thr:
            lever = 'dano+mp' if (pw is not None and a.basis and mp > 0) else 'dano' if (pw is not None and a.basis) else 'mp' if mp > 0 else 'nenhuma'
            out.append(dict(cls=c, ab=ab, share=round(share, 3), ev=round(ev), ev_rel=round(ev / best_ev, 2) if best_ev else 0, modeled=modeled, lever=lever, mp=mp, power=pw, lvl=lv))
    return out
if __name__ == '__main__':
    U = underused(); json.dump(U, open('exp8_underused.json', 'w'), ensure_ascii=False)
    mod = [u for u in U if u['modeled']]; unm = [u for u in U if not u['modeled']]
    print('combinações classe-habilidade pouco usadas (<3%):', len(U), '| modeladas:', len(mod), '| não modeladas (efeito sem valor no simulador):', len(unm))
    print('alavanca de dado entre as modeladas:', dict(collections.Counter(u['lever'] for u in mod)))
    names = {u['ab'] for u in mod if u['lever'] != 'nenhuma'}; print('habilidades distintas com alavanca:', len(names))
    print('sem alavanca simples (MP 0 e poder da arma):', sorted({(u['cls'], u['ab']) for u in mod if u['lever'] == 'nenhuma'})[:40])
    print('não modeladas:', sorted({u['ab'] for u in unm})[:60])
