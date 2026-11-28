# -*- coding: utf-8 -*-
"""Gera PATCH_NOTES.md (tudo o que muda em relação ao jogo original) a partir dos CSV de final_v1/ e final_v2/
e dos nomes em português lidos da ROM já com o patch único. Uso: python3 gen_patch_notes.py ROM_LIMPA.gba"""
import os, sys, csv, struct
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import ips, build_patch as b
import v2_design as V
from textbanks import _glyph_tables
from romdata import JOB_BASE, ITEM_BASE, ABIL_BASE

clean = open(sys.argv[1], 'rb').read(); pt = bytearray(clean)
for o, d in ips.parse(os.path.join(HERE, 'final_v2', 'FFTA_ptBR_rebalance_v2.ips')): pt[o:o + len(d)] = d
pt = bytes(pt)
enc, dec80 = _glyph_tables(b.code01)
inv01 = {}
for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?:/'()+[]\"-%&*àáâãéêíóôõúçÀÁÂÊÉÍÓÚ":
    try: inv01.setdefault(b.code01(ch), ch)
    except Exception: pass
def dec(r, p):
    s = bytearray(); e = p
    while r[e] != 0 and e - p < 200: s.append(r[e]); e += 1
    if not s: return ''
    out, i = '', 0
    if s[0] == 1:
        return ''.join(inv01.get(g, ' ' if g == 0xFF else '') for g in s[1:])
    while i < len(s):
        if s[i] == 0x80 and i + 1 < len(s): out += dec80.get(s[i + 1], '-' if s[i + 1] == 0xFE else ''); i += 2
        elif s[i] == 0x81 and i + 1 < len(s): out += '&' if s[i + 1] == 0x08 else ''; i += 2
        elif s[i] == 0x40 and i + 1 < len(s): out += ' ' if s[i + 1] in (0x73, 0x3E) else ''; i += 2 + (1 if s[i + 1] == 0x3E else 0)
        else: i += 1
    return out.strip()
u16 = lambda r, a: struct.unpack_from('<H', r, a)[0]; u32 = lambda r, a: struct.unpack_from('<I', r, a)[0]
def tbl(r, base, i):
    p = u32(r, base + 4 * i); return dec(r, p - 0x08000000) if 0x08000000 <= p < 0x09000000 else ''
NAME = lambda i: tbl(pt, b.EN_NAMES, i)
MENU = lambda i: tbl(pt, b.EN_MENU, i)
job_pt = lambda jid: NAME(u16(pt, JOB_BASE + 0x34 * jid))
item_pt = lambda idx: NAME(u16(pt, ITEM_BASE + 0x20 * idx))
abil_pt = lambda aid: MENU(u16(pt, ABIL_BASE + 0x1C * aid) - 1)
RACE = {1: 'Humano', 2: 'Bangaa', 3: 'Nu Mou', 4: 'Viera', 5: 'Moogle'}

# quem aprende cada habilidade (listas por raça + faixa de cada classe)
learn = {}
for jid in range(1, 115):
    a = JOB_BASE + 0x34 * jid; race = clean[a + 4]
    if race not in RACE or not clean[a + 0x17]: continue
    s, e = clean[a + 0x2E], clean[a + 0x2F]
    base = u32(clean, 0x6DF4D4 + 4 * race) - 0x08000000
    for i in range(s, e + 1):
        n, d, ab, tt, ap = struct.unpack_from('<HHHBB', clean, base + 8 * i)
        if tt == 1: learn.setdefault(ab, []).append(job_pt(jid))
def who(aid):
    seen = []
    for c in learn.get(aid, []):
        if c not in seen: seen.append(c)
    return ', '.join(seen) or '—'
def rd(path): return list(csv.DictReader(open(os.path.join(HERE, path), encoding='utf-8')))
def arrow(a, b_, pct=False):
    a, b_ = float(a), float(b_)
    if a == b_: return None
    f = lambda x: ('%g' % x)
    s = '%s→%s' % (f(a), f(b_))
    if pct and a: s += ' (%+d%%)' % round(100 * (b_ - a) / a)
    return s

L = []
w = L.append
w('# FFTA PT-BR: notas do patch (Rebalance v2)\n')
w('Tudo o que muda em relação ao jogo original (ROM EU "AFXP", slot inglês). Patch: `final_v2/FFTA_ptBR_rebalance_v2.ips`, que inclui a tradução PT-BR. '
  'Aplique sobre a ROM limpa e comece um save novo. Gerado automaticamente a partir das tabelas de antes/depois (`final_v1/csv`, `final_v2/csv`).\n')
w('## Resumo\n')
w('- **Classes:** atributos base e crescimento rebalanceados; Velocidade e Evade comprimidos (menos extremos).')
w('- **Equipamento:** armas raras menos absurdas, armaduras de topo mais fortes, escudos com o dobro de Evade e preços coerentes.')
w('- **Habilidades:** 15 habilidades novas no lugar de habilidades inúteis; dezenas de ajustes de MP, poder, área e AP.')
w('- **Magias:** Fogo, Gelo e Raio passam a ter funções diferentes.')
w('- **Contra-jogo:** itens de loja baratos dão imunidade a Encanto e Confusão.')
w('- **Sem mudanças de rotina do jogo (ASM):** só valores das tabelas.\n')

# ---------- habilidades novas
w('## Habilidades novas\n')
w('Elas ocupam o lugar de habilidades que quase não tinham uso. Quem aprendia a antiga aprende a nova, com a mesma arma e o mesmo custo de AP.\n')
w('| Nova | Substitui | Classes | Efeito | MP |')
w('|---|---|---|---|---|')
EFX = {'DMG': 'dano', 'DMGCAP': 'dano', 'HALF': 'metade do dano', 'DELAY': 'atrasa o turno', 'KNOCK': 'empurra', 'DRAIN': 'recupera HP = dano', 'IMMO': 'imobiliza',
       'SLOWD': 'Lento', 'PROT': 'Proteção', 'SHELL': 'Barreira', 'REGEN': 'Regen', 'BOOST': 'reforça o próximo ataque', 'DISABLE': 'paralisa', 'POISON': 'veneno', 'BLIND': 'cegueira'}
for s in V.SKILLS:
    area = ' (aliados ao redor)' if s['t'] == V.T_SELFAREA else (' (em si mesmo)' if s['t'] == V.T_SELF else '')
    arma = 'golpe com a arma: ' if s['sim'].get('rng') == 'As Weapon' else ''
    mp = u32(b'\0' * 0, 0) if False else pt[ABIL_BASE + 0x1C * s['slot'] + 4]
    w('| **%s** | %s | %s | %s%s%s | %s |' % (abil_pt(s['slot']), s['old'], who(s['slot']), arma, ' + '.join(EFX[k] for k in s['eff']), area, mp or '—'))
w('')

w('Cada habilidade nova usa a animação de uma habilidade original com a mesma estrutura (dano + status, dano + dreno etc.). '
  'Assim o jogo mostra o ícone de status, o brilho do efeito ou o número de cura, como nas habilidades originais.\n')

# ---------- magias
w('## Magias: Fogo, Gelo e Raio\n')
w('No original, as três eram idênticas (poder 30/40/50, MP 6/12/24). Agora cada elemento tem um papel:\n')
w('| Magia | Poder | MP | Efeito novo |')
w('|---|---|---|---|')
for r in sorted(rd('final_v1/csv/bal23_magias.csv'), key=lambda r: int(r['id'])):
    ef = {'103': 'causa Lento se acertar', '27': 'atrasa o turno se acertar'}.get(r['efeito2_novo'], '—')
    w('| %s | %s | %s | %s |' % (abil_pt(int(r['id'])), arrow(r['poder_orig'], r['poder_novo']) or r['poder_novo'], arrow(r['mp_orig'], r['mp_novo']) or r['mp_novo'], ef))
w('\nAnimações: Gelo usa a do Sliprain e Trovão a do Shining Air, para que o Lento e o atraso apareçam na tela (com a animação original do '
  'Blizzard e do Thunder, o efeito extra não era mostrado). Fogo mantém a sua.\n')
w('\n**Fogo** causa mais dano. **Gelo** causa menos dano, mas deixa o alvo Lento. **Raio** fica no meio e atrasa o turno do alvo.\n')

# ---------- habilidades alteradas
w('## Habilidades alteradas\n')
w('| Habilidade | Classes | Mudança |')
w('|---|---|---|')
AREA = {'1/0': 'alvo único', '5/2': 'área (raio 1)', '5/1': 'área (raio 1)'}
rows = []
for r in rd('final_v1/csv/bal22_habilidades.csv'):
    ch = []
    if r['mp_orig'] != r['mp_novo']: ch.append('MP ' + arrow(r['mp_orig'], r['mp_novo']))
    if r['poder_orig'] != r['poder_novo']: ch.append('poder ' + arrow(r['poder_orig'], r['poder_novo'], pct=True))
    if r['ap_orig'] != r['ap_novo']: ch.append('AP ' + arrow(r['ap_orig'], r['ap_novo']))
    if r['area_orig'] != r['area_novo']: ch.append('%s → %s' % (AREA.get(r['area_orig'], r['area_orig']), AREA.get(r['area_novo'], r['area_novo'])))
    rows.append((abil_pt(int(r['id'])), who(int(r['id'])), '; '.join(ch)))
for r in rd('final_v2/csv/bal24_habilidades_novas.csv'):
    if r['efeitos'] == 'buff':
        rows.append((abil_pt(int(r['id'])), who(int(r['id'])), 'poder 15→%s; MP 4→%s' % (r['poder'], r['mp'])))
for n, c, ch in sorted(rows): w('| %s | %s | %s |' % (n, c, ch))
w('')

# ---------- contra-jogo
w('## Itens de contra-jogo\n')
EF = {'2c': 'imune a Encanto', '31': 'imune a Confusão'}
for r in rd('final_v2/csv/bal25_contrajogo.csv'):
    w('- **%s** (à venda na loja): agora %s.' % (item_pt(int(r['idx'])), EF.get(r['efeitos_depois'][:2], r['efeitos_depois'])))
w('')

# ---------- classes
w('## Classes\n')
w('Regras gerais:\n')
w('- Velocidade comprimida em torno de 100 (70% da distância original): as classes muito rápidas perdem um pouco e as lentas ganham.')
w('- Evade comprimido em torno de 50 (60% da distância).')
w('- ATK e PM base ×1,12 para acompanhar a compressão das armas raras.')
w('- Orçamento de atributos ajustado por classe a partir de 12 rodadas de simulação 5v5 (milhares de batalhas por nível).')
w('- Blue Mage, Ladrão, Morpher, Domador e Engenhoqueiro recebem só o ajuste global, porque o simulador não modela os kits deles.\n')
w('Valores: base → novo. "Cresc." é o crescimento por nível. Só aparece o que mudou.\n')
w('| Classe | Raça | HP | MP | Vel. | ATK | DEF | PM | RM | Evade | Cresc. ATK | Cresc. DEF | Cresc. PM | Cresc. RM | Cresc. HP |')
w('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for r in sorted(rd('final_v1/csv/bal20_classes.csv'), key=lambda r: (int(r['raca']), job_pt(int(r['id'])))):
    c = lambda k, p=False: arrow(r[k + '_orig'], r[k + '_novo'], pct=p) or '='
    w('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        job_pt(int(r['id'])), RACE[int(r['raca'])], c('hp'), c('mp'), c('spd'), c('atk', True), c('dfn', True), c('pow', True), c('res', True), c('eva'),
        c('g_atk'), c('g_def'), c('g_pow'), c('g_res'), c('g_hp')))
w('')

# ---------- itens
w('## Equipamento\n')
w('- **Armas:** as que passam de 45 de ATK são comprimidas (45 + 55% do excesso). As armas de loja não mudam.')
w('- **Armaduras, elmos e chapéus:** a DEF e a RM crescem em curva. As peças fracas quase não mudam e as de topo chegam a ×3.')
w('- **Escudos:** Evade ×2.')
w('- **Preços:** dentro de cada tipo de arma, arma mais forte nunca é mais barata. O preço de venda é metade do de compra.\n')
it = rd('final_v1/csv/bal21_itens.csv')
groups = [('Armas (ATK)', lambda r: r['atk_orig'] != r['atk_novo'], [('atk', 'ATK')]),
          ('Armaduras e acessórios (DEF / RM)', lambda r: r['dfn_orig'] != r['dfn_novo'] or r['res_orig'] != r['res_novo'], [('dfn', 'DEF'), ('res', 'RM')]),
          ('Escudos (Evade)', lambda r: r['eva_orig'] != r['eva_novo'], [('eva', 'Evade')]),
          ('Preços', lambda r: r['buy_orig'] != r['buy_novo'], [('buy', 'Compra'), ('sell', 'Venda')])]
for title, cond, cols in groups:
    sel = [r for r in it if cond(r)]
    w('### %s (%d itens)\n' % (title, len(sel)))
    w('| Item | ' + ' | '.join(c[1] for c in cols) + ' |'); w('|---|' + '---|' * len(cols))
    for r in sorted(sel, key=lambda r: item_pt(int(r['idx']))):
        w('| %s | ' % item_pt(int(r['idx'])) + ' | '.join(arrow(r[k + '_orig'], r[k + '_novo'], pct=(k == 'atk')) or '=' for k, _ in cols) + ' |')
    w('')
w('## Não muda\n')
w('- Rotinas do jogo: fórmulas de dano, duração de status, Combo, Doublecast, Dragonheart.')
w('- Mapas, missões, inimigos fixos, leis e textos da história (além da tradução).')
w('- As descrições das magias Gelo e Raio no jogo ainda não citam o Lento e o atraso de turno.')
w('- O atraso de turno (Raio, Golpe Seco, Tiro Choque) não tem ícone próprio no jogo: aparece como um brilho no alvo.')
open(os.path.join(HERE, 'PATCH_NOTES.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('PATCH_NOTES.md:', len(L), 'linhas')
