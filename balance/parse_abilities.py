# -*- coding: utf-8 -*-
"""Lê o Apêndice I do Mechanics Guide (Terence) e gera abilities.json."""
import re, json, os
here = os.path.dirname(__file__)
L = open(os.path.join(here, 'fontes', 'mechanics_guide_terence.txt'), encoding='utf-8').read().split('\n')
start = next(i for i, l in enumerate(L) if 'APPENDIX I: ABILITY DATA' in l)
out = []; i = start
while i < len(L):
    if L[i].startswith('+====') and i + 2 < len(L) and L[i + 1].startswith('|') and L[i + 2].startswith('+===='):
        m = re.match(r'\|\s*(.+?)\s{2,}(.*?)\s*\|$', L[i + 1])
        if m and 'Power:' in L[i + 3]:
            name, sets = m.group(1), m.group(2)
            blk = L[i + 3:i + 24]
            p = re.search(r'Power:\s*(.*?)\s{2,}MP:\s*(\S+)\s*\|\s*Range:\s*(.*?)\s*\|', blk[0])
            e = re.search(r'Elem:\s*(.*?)\s*\|\s*Area:\s*(.*?)\s*\|', blk[1])
            effs = []
            for l in blk[2:12]:
                mm = re.match(r'\|\s*Eff\d:\s*(.*?)\s*\|$', l)
                if mm and mm.group(1) != '---': effs.append(mm.group(1))
            flags = ' '.join(blk[2:22]).count('Offensive') > 0
            txt = ' '.join(blk[:22])
            uniq = ''
            j = i + 3
            while j < len(L) and not (L[j].startswith('+====') and j > i + 8 and L[j + 1].strip() == '' ): j += 1
            if p:
                out.append(dict(name=name, sets=sets, power=p.group(1).strip(), mp=p.group(2), range=p.group(3).strip(),
                                elem=e.group(1).strip() if e else '', area=e.group(2).strip() if e else '', effects=effs))
    i += 1
json.dump(out, open(os.path.join(here, 'abilities.json'), 'w'), ensure_ascii=False, indent=1)
print(len(out))
