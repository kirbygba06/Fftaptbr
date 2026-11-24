# -*- coding: utf-8 -*-
"""Tabela de nível/crescimento do Mechanics Guide -> growth.json"""
import re, json, os
here = os.path.dirname(__file__)
L = open(os.path.join(here, 'fontes', 'mechanics_guide_terence.txt'), encoding='utf-8').read().split('\n')
s = next(i for i, l in enumerate(L) if l.startswith('Level Growth'))
out = []; grp = ''
for l in L[s:s + 140]:
    m = re.match(r'^---([A-Z ]+)-+$', l)
    if m: grp = m.group(1).title(); continue
    if l.startswith('Monster'): grp = 'Monstro'
    if l.startswith('Misc'): grp = 'Outros'
    m = re.match(r'^([A-Za-z\.\- ]+?)\s+((?:\d+/\s*[\d\.]+\s*){7})$', l)
    if m:
        v = re.findall(r'(\d+)/\s*([\d\.]+)', m.group(2))
        names = ['HP', 'MP', 'WAtk', 'WDef', 'MPow', 'MRes', 'Spd']
        out.append(dict(name=m.group(1).strip(), grp=grp, **{n: (int(a), float(b)) for n, (a, b) in zip(names, v)}))
json.dump(out, open(os.path.join(here, 'growth.json'), 'w'), ensure_ascii=False, indent=1)
print(len(out))
