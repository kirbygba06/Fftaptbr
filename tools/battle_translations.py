# -*- coding: utf-8 -*-
"""Falas de missão (início/fim de batalha). Arquivos em tools/battle_tr/*.txt, uma entrada por linha:
'banco[índice] texto', com '/' = quebra de linha e ' ¶ ' = nova página. {40 25 03} = nome do clã; {40 21 0x} = retrato."""
import os, re, glob
BATTLE = {}
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'battle_tr', '*.txt'))):
    for ln in open(f, encoding='utf-8'):
        ln = ln.rstrip('\n')
        m = re.match(r'(\d+)\[(\d+)\] (.*)$', ln)
        if not m: continue
        t = m.group(3).strip().replace(' ¶ ', '\f').replace('¶', '\f').replace('/', '\n')
        BATTLE.setdefault(int(m.group(1)), {})[int(m.group(2))] = t
