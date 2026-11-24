# -*- coding: utf-8 -*-
"""Ability FAQ (NeoBlitz) -> classes.json: habilidades por classe, item que ensina, AP, tipo."""
import re, json, os
here = os.path.dirname(__file__)
L = open(os.path.join(here, 'fontes', 'ability_faq_neoblitz.txt'), encoding='utf-8').read().split('\n')
cls = None; out = []; grp = ''
for l in L:
    m = re.match(r'^4\.\d+\s+([A-Za-z][A-Za-z \-]+?)\s*\*?\s*$', l)
    if m: cls = m.group(1).title(); continue
    m = re.match(r'^([A-Za-z][A-Za-z \'\.\-]+?)\s*\n?$', l)
    m = re.match(r'^\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*AP\s*\|\s*([ARSC])\s*\|\s*(.*)$', l)
    if m and cls:
        out.append(dict(cls=cls, name=m.group(1), item=m.group(2), ap=int(m.group(3)), type=m.group(4), desc=m.group(5)))
json.dump(out, open(os.path.join(here, 'class_abilities.json'), 'w'), ensure_ascii=False, indent=1)
print(len(out))
from collections import Counter
print(Counter(o['type'] for o in out)); print(sorted(Counter(o['cls'] for o in out).items()))
