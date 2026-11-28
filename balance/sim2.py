# -*- coding: utf-8 -*-
"""Simulador v2: habilidades de classe (kits do Ability FAQ + efeitos do Mechanics Guide), status e suportes.
Dirigido por dados: abilities.json (efeitos), class_abilities.json (kit, AP), ROM (classes/itens).
SUPOSIÇÕES (não estão nos guias): duração dos status, valor de status pela IA, chance de alcançar o alvo, mistura de facing, dano de veneno.
NÃO MODELA: reações, JP/Combo/Totema/leis, elementos, altura, itens consumíveis, morph/learning/steal, 2º conjunto de habilidades."""
import json, re, random, math, statistics as S, os
import sim
here = os.path.dirname(__file__)
GUIDE = json.load(open(os.path.join(here, 'abilities.json')))
KIT = json.load(open(os.path.join(here, 'class_abilities.json')))
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
AI = dict(LAMBDA=0.15, SLEEP_V=2.0, HASTE_V=1.0)          # parâmetros da IA do simulador (NÃO são dados da ROM)
OBS_HIT = {'Rockseal': 0.60, 'Charmshot': 0.95, 'Cupid': 0.80, 'Checkmate': 0.60, 'Death Sickle': 0.60}   # precisão registrada (comunidade) vs humano nv25 sem equipamento
IMMSET = {'Frog', 'Stop', 'Disable', 'Immobilize', 'Berserk', 'Blind', 'Confusion', 'Confuse', 'Doom', 'Sleep', 'Petrify', 'KO', 'Slow', 'Silence', 'Poison', 'Addle', 'Charm'}
GAP = [0]   # distância entre as frentes das equipes (modelo de mapa); 0 = sem restrição de alcance
P = dict(PROG=0, APB=40, MAP=0, P_LARGE=0.25, SMALL=(4, 7), LARGE=(10, 13), HASTE=2.0, DS2=1.0, OBS=0, IMM={10: 0.0, 25: 0.10, 45: 0.25}, SV=1.0, DURM=1.0, POISON=0.10, REACH_MOV=0.07, FACE=(0.5, 0.3, 0.2), AOE_X=1.0, FF=0.25)     # parâmetros de sensibilidade
# CONFIRMADO (teste comunitário nível 25): Stop 3, Silence 3, Slow 3, Haste 3, Doom 3, Petrify até curar. Charm e Sleep terminam ao receber dano (duração natural: suposição).
# SUPOSIÇÃO: Confusion, Poison (turnos e %), Sleep/Charm natural, Blind, Berserk, Disable, Immobilize, buffs.
DUR = {'Stop': 3, 'Sleep': 4, 'Petrify': 99, 'Charm': 4, 'Confusion': 4, 'Confuse': 4, 'Berserk': 4, 'Blind': 4, 'Silence': 3, 'Disable': 4, 'Addle': 4, 'Immobilize': 4, 'Slow': 3,
       'Speed DOWN': 3, 'Poison': 5, 'Doom': 3, 'Frog': 4, 'Haste': 3, 'Expert Guard': 2, 'Quicken': 1, 'Protect': 4, 'Shell': 4, 'Defense': 3, 'Regen': 5, 'Reflect': 4, 'Boost': 3, 'Auto-Life': 99, 'Astra': 4,
       'WAtk DOWN': 4, 'MPow DOWN': 4, 'WDef DOWN': 4, 'MRes DOWN': 4, 'WAtk UP': 4, 'WDef UP': 4, 'MPow UP': 4, 'MRes UP': 4, 'Advice': 4, 'Conceal': 4}
HARM = {'Stop', 'Sleep', 'Petrify', 'Charm', 'Confusion', 'Confuse', 'Berserk', 'Blind', 'Silence', 'Disable', 'Addle', 'Immobilize', 'Slow', 'Speed DOWN', 'Poison', 'Doom', 'Frog',
        'WAtk DOWN', 'MPow DOWN', 'WDef DOWN', 'MRes DOWN', 'KO'}
RANGE_W = {'Archer': 5, 'Hunter': 4, 'Sniper': 5, 'Gunner': 4, 'Assassin': 4, 'Juggler': 3, 'Dragoon': 2, 'Fencer': 2, 'Gadgeteer': 3}
import collections
STATS = dict(use=collections.Counter(), acts=collections.Counter(), att=collections.Counter(), succ=collections.Counter(), impact=collections.defaultdict(float), moves=collections.Counter(), hgain=collections.defaultdict(float), hcast=collections.Counter(), evall=collections.defaultdict(float), evalln=collections.Counter(), best=collections.Counter(), ev=collections.defaultdict(float), evn=collections.Counter(), mp=collections.defaultdict(float), mpn=collections.Counter(), denied=collections.defaultdict(float), uses_ab=collections.Counter())
def reset_stats():
    for k in STATS: STATS[k].clear()
class Ab:
    __slots__ = ('harm', 'name', 'basis', 'power', 'mp', 'rng', 'area', 'eff', 'ap', 'type', 'cls', 'ranged_w')
def parse_effect(s):
    parts = [p.strip() for p in s.split(',', 2)]
    if len(parts) < 3: return None
    hit, tgt, act = parts; dep = act.startswith('Eff')
    tgt0 = tgt.strip()
    mt = re.match(r'(Undead|Non-Undead|NonUndead|Monster|Animal|Dragon|NonDragon|NonMonster|NonAnimal|Gadget|Enemy|Self|Default|KOed Unit|EqpSword|LvlDivBy\d|SameLvDigit|SmeLvlDay|Eye2Eye)', tgt0)
    tgt0 = mt.group(1) if mt else tgt0
    act = re.sub(r'^Eff\dDep:\s*', '', act); act = re.sub(r'^(NonUndead|Undead|Non-Undead|Enemy|Self|Default|LvlDivBy\d|SameLvDigit)[:,]?\s*', '', act)
    e = dict(hit=hit, tgt=tgt0, dep=dep, kind='noop')
    m = re.match(r'(\d+)% Damage to MP', act)
    if m: e.update(kind='mpdmg', m=int(m.group(1)) / 100); return e
    m = re.match(r'(\d+)% Damage$', act)
    if m: e.update(kind='dmg', m=int(m.group(1)) / 100); return e
    m = re.match(r'(\d+)% Damage, ([\d.]+)x Hit Rate$', act)
    if m: e.update(kind='dmg', m=int(m.group(1)) / 100, hitm=float(m.group(2))); return e
    if re.match(r"100% Damage, capped to Target's Max HP", act): e.update(kind='dmg', m=1.0); return e
    if act == 'Heal Eff1 Damage': e.update(kind='drain'); return e
    if act == 'Knockback': e.update(kind='knock'); return e
    if act == '100% Heal': e.update(kind='heal', m=1.0); return e
    if act.startswith('Heal to full HP') or act.startswith('Cureall'): e.update(kind='healfull'); return e
    m = re.match(r'Revive to (\d+|full)', act)
    if m: e.update(kind='revive', m=1.0 if m.group(1) == 'full' else int(m.group(1)) / 100); return e
    if act in ('Esuna',) or act.startswith('Remove '): e.update(kind='esuna'); return e
    if act == 'Dispel': e.update(kind='dispel'); return e
    if act == 'Delay Unit': e.update(kind='delay'); return e
    m = re.match(r"\[\(Target's HP \+ 1\) / 2\] Damage", act)
    if m: e.update(kind='hpfrac', m=0.5); return e
    if re.match(r"\[Target's HP / 4\]", act): e.update(kind='hpfrac', m=0.25); return e
    if act.startswith('Max HP Damage') or act.startswith("(Target's Max HP)"): e.update(kind='hpfrac', m=1.0, mx=True); return e
    if act == '999 Damage': e.update(kind='flat', v=999); return e
    if act == '30 Damage': e.update(kind='flat', v=30); return e
    m = re.match(r'Inflict (.+)$', act)
    if m:
        names = [n.strip() for n in m.group(1).split('/')]; e.update(kind='status', names=names); return e
    return e
def build_catalog():
    cat = {}
    for g in GUIDE:
        a = Ab(); a.name = g['name']; pw = g['power']; m = re.match(r'(\d+)\s*\((\w+)\)', pw)
        a.basis = None; a.power = None
        if m: a.power = int(m.group(1)); a.basis = 'M' if m.group(2) == 'MPow' else 'W'
        elif pw.startswith('As Weapon'): a.basis = 'W'; a.power = None
        a.mp = int(g['mp']) if g['mp'].isdigit() else 0
        a.rng = g['range']; a.area = g['area']; a.eff = [x for x in (parse_effect(e) for e in g['effects']) if x and x['tgt'] not in ('Undead', 'Monster', 'Animal', 'Dragon', 'Gadget', 'EqpSword')]; cat.setdefault(norm(a.name), a)
    return cat
CAT = build_catalog()
DISABLE = set()
APMOD = {}   # nome da habilidade -> AP alterado (teste de progressão)
def kit_for(cls_name, cap):
    A, Sup = [], []
    for k in KIT:
        if norm(k['cls']) != norm(cls_name): continue
        if APMOD.get(k['name'], k['ap']) > cap: continue
        if k['type'] == 'A' and norm(k['name']) in CAT and k['name'] not in DISABLE: A.append(CAT[norm(k['name'])])
        elif k['type'] == 'S': Sup.append(k['name'])
    return A, Sup
FIGHT = Ab(); FIGHT.name = 'Fight'; FIGHT.basis = 'W'; FIGHT.power = None; FIGHT.mp = 0; FIGHT.rng = 'As Weapon'; FIGHT.area = 'One Unit'; FIGHT.eff = [dict(hit='AType', tgt='Enemy', dep=False, kind='dmg', m=1.0)]
def cap_for(level): return 100 if level <= 12 else 200 if level <= 25 else 300 if level <= 45 else 999
# ---------- unidade ----------
SUPPORT_PRIO = ['Double Sword', 'Doublecast', 'Weapon Atk+', 'Magic Pow+', 'Doublehand', 'Turbo MP', 'Concentrate', 'Weapon Def+', 'Half MP', 'Immunity']
def mk(j, level, g, abil, cfg=None, scenario_mp=None):
    t = sim.tier(level); prof = sim.PROFILE.get(j['name'], sim.PHYS); rob = prof in sim.ROBE
    L = lambda b, gg: b * 1.05 + gg * (level - 1)
    u = dict(name=j['name'], id=j['id'], lvl=level, prof=prof, hp=L(j['hp'], j['g_hp']), mp=L(j['mp'], j['g_mp']), spd=L(j['spd'], j['g_spd']), atk=L(j['atk'], j['g_atk']),
             dfn=L(j['dfn'], j['g_def']), pw=L(j['pow'], j['g_pow']), rs=L(j['res'], j['g_res']), eva=j['eva'] + (0 if rob else g['phys_eva'][t]), mov=j['mov'], sres=j['sres'] or 50)
    u['wep'] = g['wep'][t] * (0.8 if rob else 1.0); u['dfn'] += g['mage_def'][t] if rob else g['phys_def'][t]; u['rs'] += g['mage_res'][t] if rob else g['phys_res'][t]; u['pw'] += g['rod_pow'][t] if rob else 0
    u['imm'] = random.random() < P['IMM'].get(level, 0.25 if level > 25 else 0.10 if level > 12 else 0.0)
    u['maxhp'] = u['hp']; u['mp0'] = u['mp']; u['cnt'] = 0; u['st'] = {}; u['wr'] = RANGE_W.get(j['name'], 1)
    if P.get('PROG') == 2:
        import progression
        _pl = progression.plan(j['race'], j['name'], level, P['APB'], APMOD, P.get('BATT'))
        _sr = {1: 'auto', 0: 'none', 2: 'prereq'}[P.get('SEC', 1)]
        _pl = progression.plan(j['race'], j['name'], level, P['APB'], APMOD, P.get('BATT'), 'prereq' if _sr == 'prereq' else 'auto') if _sr != 'none' else _pl
        _n = _pl['kit_A'] if _sr != 'none' else _pl.get('kit_A_own', _pl['kit_A'])
        Sup = _pl['kit_S']; A = [CAT[norm(x)] for x in _n if norm(x) in CAT and x not in DISABLE]
    elif P.get('PROG'):
        import progression
        _n, Sup = progression.kit_prog(j['name'], level, P['APB'], APMOD)
        A = [CAT[norm(x)] for x in _n if norm(x) in CAT and x not in DISABLE]
    else: A, Sup = kit_for(j['name'], cap_for(level))
    u['abs'] = [FIGHT] + A; u['sup'] = [s for s in SUPPORT_PRIO if s in Sup]; u['s'] = u['sup'][0] if u['sup'] else None
    if P.get('NO_DS'): u['sup'] = [x for x in u['sup'] if x != 'Double Sword']; u['s'] = u['sup'][0] if u['sup'] else None
    if P.get('NO_DC'): u['sup'] = [x for x in u['sup'] if x != 'Doublecast']; u['s'] = u['sup'][0] if u['sup'] else None
    if 'Double Sword' in u['sup'] and level > 45: u['s'] = 'Double Sword'
    return u
# ---------- fórmulas ----------
def has(u, s): return s in u['st']
def attv(u, phys):
    v = (u['atk'] + u['wep']) if phys else u['pw']
    if phys and u['s'] in ('Weapon Atk+',): v *= 307 / 256
    if (not phys) and u['s'] == 'Magic Pow+': v *= 307 / 256
    if phys and has(u, 'Berserk'): v *= 307 / 256
    if phys and has(u, 'Boost'): v *= 1.5
    if has(u, 'Frog'): v *= 0.1
    if phys and has(u, 'WAtk UP'): v *= 1.1
    if phys and has(u, 'WAtk DOWN'): v *= 0.9
    if (not phys) and has(u, 'MPow UP'): v *= 1.1
    if (not phys) and has(u, 'MPow DOWN'): v *= 0.9
    return v
def defv(u, phys):
    v = u['dfn'] if phys else u['rs']
    if phys and u['s'] == 'Weapon Def+': v *= 358 / 256
    if phys and (has(u, 'Protect') or has(u, 'Defense')): v *= 358 / 256
    if (not phys) and has(u, 'Shell'): v *= 358 / 256
    if has(u, 'Petrify'): v *= 460 / 256
    if has(u, 'Frog'): v *= 0.1
    if phys and has(u, 'WDef UP'): v *= 1.4
    if phys and has(u, 'WDef DOWN'): v *= 0.7
    if (not phys) and has(u, 'MRes UP'): v *= 1.4
    if (not phys) and has(u, 'MRes DOWN'): v *= 0.7
    return v
def power_of(u, a, phys):
    if a.power is None: return u['wep'] if phys else u['pw'] * 0 + u['wep']
    p = a.power
    if a is FIGHT: p = u['wep']
    return p
def base_dmg(u, t, a, e):
    phys = a.basis == 'W'
    p = power_of(u, a, phys)
    att = attv(u, phys)
    if a.mp > 0 and u['s'] == 'Turbo MP': att *= 332 / 256
    return max(1.0, att - defv(t, phys) / 2) * p / 100 * e.get('m', 1.0) * u.get('dmgmult', 1.0)
def hit_a(u, t, rng):
    if has(t, 'Stop') or has(t, 'Sleep') or has(t, 'Petrify'): return 1.0
    ev = max(0, min(100, t['eva'])); f = rng.random(); fp = P['FACE']
    ev = ev if f < fp[0] else ev // 2 if f < fp[0] + fp[1] else ev // 4
    if has(t, 'Blind'): ev -= 20
    if has(t, 'Confusion'): ev -= 10
    if has(u, 'Blind'): ev += 50
    if u['s'] == 'Concentrate': ev -= 50
    if u['s'] == 'Turbo MP': ev -= 15
    return (100 - max(5, min(95, ev))) / 100
def hit_s(u, t, rng, names, abname=None):
    if t.get('imm') and any(n in IMMSET for n in names): return 0.0
    if P['OBS'] and abname in OBS_HIT and not has(t, 'Astra'):
        f = rng.random(); fp = P['FACE']; sh = 0 if f < fp[0] else 0.10 if f < fp[0] + fp[1] else 0.20
        return max(0.0, min(1.0, OBS_HIT[abname] - sh))
    if has(t, 'Stop') or has(t, 'Sleep') or has(t, 'Petrify'): return 1.0
    if t['s'] == 'Immunity' and any(n in ('Frog', 'Blind', 'Confusion', 'Confuse', 'Sleep', 'Petrify', 'Silence', 'Poison') for n in names): return 0.0
    if has(t, 'Astra'): return 0.0
    sr = t['sres']; f = rng.random(); fp = P['FACE']
    sr -= 0 if f < fp[0] else 10 if f < fp[0] + fp[1] else 20
    if u['s'] == 'Concentrate': sr -= 20
    if u['s'] == 'Turbo MP': sr -= 10
    return (100 - max(0, min(100, sr))) / 100
def is_harm(a):
    h = getattr(a, 'harm', None)
    if h is None:
        h = any(e['kind'] in ('dmg', 'hpfrac', 'flat', 'mpdmg', 'delay', 'dispel') or (e['kind'] == 'status' and any(n in HARM for n in e['names'])) for e in a.eff)
        a.harm = h
    return h
def eff_range(u, a):
    r = a.rng
    if r == 'Infinite': return 99
    if r == 'Self' and 'Not Self' not in a.area: return 99
    if r == 'Self': return 1
    return u['wr'] if r == 'As Weapon' else (3 if r in ('Cone', 'Line', 'Dbl-Line') else int(r) if r.isdigit() else 1)
def reach(u, a, gate=None):
    if P['MAP'] and GAP[0] > 0 and (is_harm(a) if gate is None else gate):
        mv = 0 if has(u, 'Immobilize') else u['mov']
        if GAP[0] > mv + eff_range(u, a): return 0.0
    r = a.rng; mov = u['mov']
    if r == 'Infinite': return 1.0
    if r == 'Self' and 'Not Self' not in a.area: return 1.0
    if r == 'Self': r = '1'
    R = u['wr'] if r == 'As Weapon' else (3 if r in ('Cone', 'Line', 'Dbl-Line') else int(r) if r.isdigit() else 1)
    mv = 0 if has(u, 'Immobilize') else mov
    return max(0.2, min(0.98, 0.45 + P['REACH_MOV'] * mv * 1.0 + 0.10 * (R - 1) - (0.0 if mv else 0.25)))
def extra_targets(a):
    ar = a.area
    if ar.startswith('Infinite'): return 9
    m = re.match(r'r(\d)', ar)
    if m: return {1: 0.8, 2: 1.6, 3: 2.4}.get(int(m.group(1)), 0.8) * P['AOE_X']
    if 'Not Self' in ar: return 1.0
    return 0.0
# ---------- status ----------
SRC = [None]
def add_status(u, name, rng, sleep_ok=True):
    if has(u, 'Petrify') or u['hp'] <= 0: return
    d = int(round(DUR.get(name, 4) * P['DURM']))
    if name == 'KO': u['hp'] = 0; return
    if name == 'Quicken': u['cnt'] = 1000; return
    if name == 'Speed DOWN': name = 'Slow'
    if name == 'Confuse': name = 'Confusion'
    if name == 'Haste' and has(u, 'Slow'): del u['st']['Slow']; return
    if name == 'Slow' and has(u, 'Haste'): del u['st']['Haste']; return
    u['st'][name] = max(1, d); u.setdefault('src', {})[name] = SRC[0]
def clear_debuffs(u):
    for k in list(u['st']):
        if k in HARM and k != 'Doom' or k == 'Doom': u['st'].pop(k, None)
def status_value(u, t, name, ally_dps, foe_dps_total, nallies):
    D = DUR.get(name, 4) * P['DURM']; td = max(1.0, t.get('dps', 100.0)); mage = t['prof'] in (sim.MAGE, sim.HEAL, sim.UTIL)
    if name in ('Stop',): return td * min(D, 3) * 0.9
    if name == 'Sleep': return td * AI['SLEEP_V']
    if name == 'Petrify': return td * 8 + t['hp'] * 0.2
    if name in ('Charm',): return td * D * 0.9
    if name in ('Confusion', 'Confuse'): return td * D * 0.7
    if name == 'Berserk': return td * D * (0.3 if mage else 0.05)
    if name == 'Blind': return td * D * (0.1 if mage else 0.3)
    if name == 'Silence': return td * D * (0.8 if mage else 0.05)
    if name in ('Disable', 'Addle'): return td * D * 0.5
    if name == 'Immobilize': return td * D * 0.3
    if name in ('Slow', 'Speed DOWN'): return td * D * 0.4
    if name == 'Poison': return t['maxhp'] * P['POISON'] * D
    if name == 'Doom': return t['hp'] * 0.6 + td * 1.5
    if name == 'KO': return t['hp'] + td * 3
    if name == 'Frog': return td * D * 0.9
    if name in ('WAtk DOWN', 'MPow DOWN', 'WDef DOWN', 'MRes DOWN'): return td * D * 0.1
    # benéficos (t = aliado)
    if name == 'Haste': return td * D * 1.0 * AI['HASTE_V']
    if name == 'Quicken': return td * 1.0
    if name == 'Expert Guard': return 0.9 * foe_dps_total * 1.2 / max(1, nallies) * D
    if name in ('Protect', 'Shell', 'Defense'): return 0.2 * foe_dps_total / max(1, nallies) * D
    if name == 'Regen': return t['maxhp'] * 0.1 * D * 0.8
    if name in ('Boost',): return td * 0.5 * D
    if name == 'Auto-Life': return td * 1.5
    if name in ('WAtk UP', 'MPow UP', 'WDef UP', 'MRes UP', 'Advice', 'Reflect', 'Astra', 'Conceal'): return td * D * 0.1
    return 0.0
BEN = {'Expert Guard', 'Haste', 'Quicken', 'Protect', 'Shell', 'Defense', 'Regen', 'Boost', 'Auto-Life', 'WAtk UP', 'MPow UP', 'WDef UP', 'MRes UP', 'Advice', 'Reflect', 'Astra', 'Conceal'}
def est_dps(u, foes):
    ad = S.mean(f['dfn'] for f in foes); ar = S.mean(f['rs'] for f in foes); best = 0
    for a in u['abs']:
        for e in a.eff:
            if e['kind'] == 'dmg' and a.basis:
                ph = a.basis == 'W'; p = u['wep'] if (a.power is None or a is FIGHT) else a.power
                d = max(1, attv(u, ph) - (ad if ph else ar) / 2) * p / 100 * e['m'] * (0.7 if a.mp and u['mp'] < a.mp else 1.0)
                if a.mp > 0 and u['mp0'] < a.mp * 3: d *= 0.6
                best = max(best, d * 0.75)
    return best
def allowed(u, a):
    if has(u, 'Frog'): return a is FIGHT
    if has(u, 'Disable') or has(u, 'Addle'): return a is FIGHT
    if has(u, 'Silence') and (a.mp > 0 or a.basis == 'M'): return False
    mp = a.mp * (2 if u['s'] == 'Turbo MP' else 0.5 if u['s'] == 'Half MP' else 1)
    return u['mp'] >= mp
def score_ability(u, a, own, foes, rng):
    """melhor (valor, alvo) para a habilidade a; valor em PV equivalentes."""
    r = reach(u, a, gate=is_harm(a))
    live_f = [f for f in foes if f['hp'] > 0 and not has(f, 'Petrify')]; live_a = [x for x in own if x['hp'] > 0]; dead_a = [x for x in own if x['hp'] <= 0 and not has(x, 'Petrify')]
    if not live_f: return 0, None
    ftot = sum(f.get('dps', 100) for f in live_f)
    ex = extra_targets(a); best = (0.0, None)
    harmful = any(e['kind'] in ('dmg', 'hpfrac', 'flat', 'mpdmg') or (e['kind'] == 'status' and any(n in HARM for n in e['names'])) or e['kind'] in ('delay', 'dispel') for e in a.eff)
    cands = live_f if harmful else (dead_a if any(e['kind'] == 'revive' for e in a.eff) else live_a)
    if (a.area == 'Self' or a.rng == 'Self') and not harmful: cands = [u]
    if not cands: return 0, None
    vals = []
    for t in cands:
        tot = 0.0; e1 = 1.0
        for k, e in enumerate(a.eff):
            kind = e['kind']
            h = e['hit']
            if kind == 'dmg' and a.basis:
                hit = hit_a(u, t, rng) if h == 'AType' else (hit_s(u, t, rng, []) if h == 'SType' else 1.0)
                if e.get('hitm'): hit = min(1.0, hit * e['hitm'])
                if e['dep']: hit = e1
                dm = base_dmg(u, t, a, e); tot += hit * min(dm, t['hp']) * (1 if t in foes else -1)
                lastdm = min(dm, t['hp'])
                if t in foes and dm >= t['hp']: tot += hit * t.get('dps', 100) * 2
                if k == 0: e1 = hit
            elif kind == 'hpfrac' and harmful:
                tot += hit_a(u, t, rng) * min(t['hp'] * e['m'] if not e.get('mx') else t['maxhp'], t['hp'])
            elif kind == 'flat' and harmful: tot += min(e['v'], t['hp']) * hit_a(u, t, rng)
            elif kind == 'heal':
                dm = base_dmg(u, t, a, e); tot += min(dm, t['maxhp'] - t['hp'])
            elif kind == 'healfull': tot += t['maxhp'] - t['hp']
            elif kind == 'revive' and t['hp'] <= 0: tot += t.get('dps', 100) * 4 + t['maxhp'] * e['m'] * 0.5
            elif kind == 'status':
                for nm in e['names']:
                    harm = nm in HARM
                    if harm and t in own and t is not u: continue
                    if not harm and t in foes: continue
                    hit = hit_s(u, t, rng, e['names'], a.name) if (e['hit'] == 'SType' and (not e['dep'] or (P['OBS'] and a.name in OBS_HIT))) else (e1 if e['dep'] else (hit_a(u, t, rng) if e['hit'] == 'AType' else 1.0))
                    if e['hit'] not in ('AType', 'SType') and not e['dep']:
                        m = re.match(r'(\d+)%', e['hit']); hit = int(m.group(1)) / 100 if m else 1.0
                    if nm in t['st']: continue
                    tot += hit * status_value(u, t, nm, 0, ftot, len(live_a)) * P['SV']
            elif kind == 'esuna':
                tot += sum(status_value(u, t, k_, 0, ftot, len(live_a)) for k_ in t['st'] if k_ in HARM) * 0.7 * P['SV']
            elif kind == 'delay': tot += t.get('dps', 100) * 0.4 * (e1 if e['dep'] else hit_a(u, t, rng))
            elif kind == 'drain' and t in foes: tot += e1 * min(locals().get('lastdm', 0), u['maxhp'] - u['hp'])
            elif kind == 'knock' and t in foes: tot += t.get('dps', 100) * 0.15 * e1
        vals.append((tot * r, t))
    vals.sort(key=lambda x: -x[0]); v0, t0 = vals[0]
    if len(vals) > 1 and ex > 0:
        m = min(ex, len(vals) - 1); rest = [v for v, _ in vals[1:1 + int(math.ceil(m))]]
        frac = m / max(1, len(rest)); v0 += sum(rest) * frac * (1 - P['FF']) - sum(rest) * frac * P['FF'] * 0.5
    return v0, t0
def do_effects(u, t, a, own, foes, rng, e1ok):
    first = True; ok = True; res = []
    for e in a.eff:
        kind = e['kind']; h = e['hit']
        if kind == 'noop': continue
        hit = hit_a(u, t, rng) if h == 'AType' else (hit_s(u, t, rng, e.get('names', []), a.name) if h == 'SType' else 1.0)
        if h not in ('AType', 'SType'):
            m = re.match(r'(\d+)%', h); hit = int(m.group(1)) / 100 if m else 1.0
        if e.get('hitm'): hit = min(1.0, hit * e['hitm'])
        if e['dep'] and not (P['OBS'] and a.name in OBS_HIT and kind == 'status'): success = ok
        else: success = rng.random() < hit
        if kind == 'status' and (not e['dep'] or (P['OBS'] and a.name in OBS_HIT)):
            STATS['att'][a.name] += 1; STATS['succ'][a.name] += 1 if success else 0
        elif kind == 'status' and ok:
            STATS['att'][a.name] += 1; STATS['succ'][a.name] += 1
        if first: ok = success; first = False
        if not success: continue
        if kind == 'dmg' and a.basis:
            dm = base_dmg(u, t, a, e) * rng.uniform(.9, 1.1)
            if a.basis == 'W' and has(t, 'Sleep'): t['st'].pop('Sleep', None)
            if has(t, 'Expert Guard'): dm = 0
            t['hp'] -= dm; STATS['impact'][a.name] += min(dm, max(0, t['hp'] + dm)) * (1 if t in foes else -1); lastdm = min(dm, max(0, t['hp'] + dm))
            for _s in ('Sleep', 'Charm'): t['st'].pop(_s, None)
        elif kind == 'hpfrac':
            _d = 0 if has(t, 'Expert Guard') else (t['maxhp'] if e.get('mx') else t['hp']) * e['m']; t['hp'] -= _d; STATS['impact'][a.name] += _d
        elif kind == 'flat': t['hp'] -= e['v']
        elif kind == 'mpdmg': t['mp'] = max(0, t['mp'] - base_dmg(u, t, a, e))
        elif kind == 'heal':
            _h = min(t['maxhp'] - t['hp'], base_dmg(u, t, a, e) * rng.uniform(.9, 1.1)); t['hp'] += _h; STATS['impact'][a.name] += _h
        elif kind == 'healfull': t['hp'] = t['maxhp']
        elif kind == 'revive':
            if t['hp'] <= 0 and not has(t, 'Petrify'): t['hp'] = t['maxhp'] * e['m']; t['st'].clear()
        elif kind == 'status':
            for nm in e['names']:
                harm = nm in HARM
                if (harm and t in own and t is not u) or ((not harm) and t in foes): continue
                SRC[0] = a.name; add_status(t, nm, rng)
                if nm == 'Haste': STATS['hcast'][a.name] += 1
                if nm == 'Petrify': STATS['denied'][a.name] += t.get('dps', 100) * 6
        elif kind == 'esuna': clear_debuffs(t)
        elif kind == 'dispel':
            for k_ in list(t['st']):
                if k_ in BEN: t['st'].pop(k_, None)
        elif kind == 'delay': t['cnt'] = 0
        elif kind == 'drain': u['hp'] = min(u['maxhp'], u['hp'] + locals().get('lastdm', 0))
        elif kind == 'knock': t['cnt'] = t['cnt'] * 0.6
    if t['hp'] <= 0 and t['st'].get('Auto-Life'):
        t['hp'] = t['maxhp'] * 0.25; t['st'].clear()
FORCE = {}   # id da classe -> nome da habilidade usada sempre que possível (medida de valor por ação)
def pick_action(u, own, foes, rng):
    best = (0.0, None, None)
    cands = [a for a in u['abs'] if allowed(u, a)]
    fa = FORCE.get(u['id'])
    if fa:
        for a in cands:
            if a.name == fa:
                v, t = score_ability(u, a, own, foes, rng)
                if t is not None: return (v, a, t)
    for a in cands:
        v, t = score_ability(u, a, own, foes, rng)
        v -= AI['LAMBDA'] * a.mp
        STATS['evall'][(u['name'], a.name)] += v; STATS['evalln'][(u['name'], a.name)] += 1
        if v > best[0]: best = (v, a, t)
    if best[1] is not None: STATS['best'][(u['name'], best[1].name)] += 1
    return best
def take_turn(u, own, foes, rng):
    st = u['st']
    # início do turno
    if has(u, 'Poison'): u['hp'] -= u['maxhp'] * P['POISON']
    if has(u, 'Regen'): u['hp'] = min(u['maxhp'], u['hp'] + u['maxhp'] * 0.1)
    if has(u, 'Doom'):
        st['Doom'] -= 1
        if st['Doom'] <= 0: u['hp'] = 0
    if u['hp'] <= 0:
        if u['st'].get('Auto-Life'): u['hp'] = u['maxhp'] * 0.25; u['st'].clear()
        else: return
    if has(u, 'Haste'): STATS['hgain'][u.get('src', {}).get('Haste') or '?'] += 0.5 * u.get('dps', 100)
    skip = has(u, 'Stop') or has(u, 'Sleep') or has(u, 'Petrify')
    for _n in ('Stop', 'Sleep', 'Charm', 'Confusion'):
        if has(u, _n): STATS['denied'][u.get('src', {}).get(_n) or '?'] += u.get('dps', 100) * (1.0 if _n != 'Confusion' else 0.7)
    live_f = [f for f in foes if f['hp'] > 0 and not has(f, 'Petrify')]
    if not live_f: return
    if not skip:
        if has(u, 'Charm'):
            pool = [x for x in own if x['hp'] > 0 and x is not u] or [u]; tg = rng.choice(pool); a = FIGHT
            if rng.random() < reach(u, a): do_effects(u, tg, a, own, foes, rng, True)
        elif has(u, 'Confusion'):
            tg = rng.choice([x for x in own + foes if x['hp'] > 0]); a = FIGHT
            do_effects(u, tg, a, own, foes, rng, True)
        elif has(u, 'Berserk'):
            tg = rng.choice(live_f)
            if rng.random() < reach(u, FIGHT): do_effects(u, tg, FIGHT, own, foes, rng, True)
        else:
            v, a, t = pick_action(u, own, foes, rng)
            if a is None: a, t = FIGHT, min(live_f, key=lambda f: f['hp'])
            STATS['use'][(u['name'], u['lvl'], a.name)] += 1; STATS['acts'][(u['name'], u['lvl'])] += 1; STATS['ev'][a.name] += v; STATS['evn'][a.name] += 1
            n = 2 if (u['s'] == 'Double Sword' and a is FIGHT) else 1
            casts = 2 if (u['s'] == 'Doublecast' and a.mp > 0) else 1
            if P['MAP'] and GAP[0] > 0 and is_harm(a) and reach(u, a) == 0.0:
                GAP[0] = max(0, GAP[0] - u['mov']); STATS['moves'][u['name']] += 1
                for _k in list(st):
                    if _k not in ('Petrify', 'Auto-Life', 'Doom'):
                        st[_k] -= 1
                        if st[_k] <= 0: del st[_k]
                return
            for _ in range(max(n, casts)):
                u['dmgmult'] = P['DS2'] if (n == 2 and _ == 1) else 1.0
                if t is None or (t['hp'] <= 0 and not any(e['kind'] == 'revive' for e in a.eff)): break
                if rng.random() < reach(u, a):
                    targets = [t]
                    ex = extra_targets(a)
                    if ex > 0:
                        pool = [x for x in (foes if t in foes else own) if x is not t and (x['hp'] > 0 or any(e['kind'] == 'revive' for e in a.eff))]
                        rng.shuffle(pool); targets += pool[:int(ex) + (1 if rng.random() < ex - int(ex) else 0)]
                        if t in own and not is_harm(a):
                            lf = [f for f in foes if f['hp'] > 0]
                            for _i in range(1, len(targets)):
                                if lf and rng.random() < P['FF']: targets[_i] = rng.choice(lf)
                    if a.mp:
                        _c = a.mp * (2 if u['s'] == 'Turbo MP' else 0.5 if u['s'] == 'Half MP' else 1); u['mp'] -= _c; u['mpsp'] = u.get('mpsp', 0) + _c
                    for tt in targets: do_effects(u, tt, a, own, foes, rng, True)
                    if P['MAP'] and GAP[0] > 0 and is_harm(a): GAP[0] = min(GAP[0], max(1, eff_range(u, a) if eff_range(u, a) < 99 else 1))
                    u['casts'] = u.get('casts', 0) + (1 if a.mp else 0)
                if casts == 2 and _ == 0:
                    v, a2, t2 = pick_action(u, own, foes, rng)
                    if a2 is None or not a2.mp: break
                    a, t = a2, t2
    u['dmgmult'] = 1.0
    for k in list(st):
        if k in ('Petrify', 'Auto-Life', 'Doom'): continue
        st[k] -= 1
        if st[k] <= 0: del st[k]
def battle(A, B, rng, maxturn=400):
    r = _battle(A, B, rng, maxturn)
    for u in A + B: STATS['mp'][(u['name'], u['lvl'])] += u.get('mpsp', 0); STATS['mpn'][(u['name'], u['lvl'])] += 1
    return r
def _battle(A, B, rng, maxturn=400):
    units = A + B; order = {id(u): i for i, u in enumerate(units)}
    if P['MAP']:
        lo, hi = P['LARGE'] if random.random() < P['P_LARGE'] else P['SMALL']; GAP[0] = random.randint(lo, hi)
    else: GAP[0] = 0
    for u in units: u['cnt'] = 0; u['st'] = {}
    for team, foes in ((A, B), (B, A)):
        for u in team: u['dps'] = max(40.0, est_dps(u, foes))
    acts = 0
    for _ in range(maxturn * 40):
        for u in units:
            if u['hp'] > 0 and not has(u, 'Petrify'):
                sp = u['spd'] * (P['HASTE'] if has(u, 'Haste') else 0.5 if has(u, 'Slow') else 1.0); u['cnt'] += sp
        ready = sorted([u for u in units if u['hp'] > 0 and u['cnt'] >= 1000], key=lambda u: (-u['cnt'], order[id(u)]))
        for u in ready:
            if u['hp'] <= 0: continue
            own, foe = (A, B) if u in A else (B, A)
            take_turn(u, own, foe, rng); u['cnt'] -= 1000; acts += 1
            if all(f['hp'] <= 0 or has(f, 'Petrify') for f in foe): return (1 if u in A else 0), acts
            if all(x['hp'] <= 0 or has(x, 'Petrify') for x in own): return (0 if u in A else 1), acts
        if all(u['hp'] <= 0 or has(u, 'Petrify') for u in B): return 1, acts
        if all(u['hp'] <= 0 or has(u, 'Petrify') for u in A): return 0, acts
        if acts > 400: break
    return 0.5, acts
HARD = {'Petrify': 20, 'Doom': 20, 'KO': 20, 'Stop': 16, 'Charm': 14, 'Confusion': 14, 'Confuse': 14, 'Sleep': 14, 'Frog': 14}
SOFT = {'Slow': 6, 'Speed DOWN': 6, 'Blind': 6, 'Silence': 8, 'Poison': 6, 'Berserk': 6, 'Disable': 8, 'Addle': 8, 'Immobilize': 8}
def price_mods():
    """Regra F1 de preço de status: habilidade que aplica status duro/leve com SType custa pelo menos X de MP (tabela HARD/SOFT)."""
    mods = {}
    for a in CAT.values():
        need = 0
        for e in a.eff:
            if e['kind'] == 'status' and e['hit'] == 'SType':
                for nm in e['names']:
                    need = max(need, HARD.get(nm, 0), SOFT.get(nm, 0))
        if need and a.mp < need: mods[a.name] = need
    return mods
def run(scn, levels=(10, 25, 45), n=1500, seed=1, size=3, jobs=None):
    mods = scn.get('mods') or {}; saved = {}; DISABLE.clear(); DISABLE.update(scn.get('disable', ()))
    random.seed(seed + 7)
    for a in CAT.values():
        if a.name in mods:
            m = mods[a.name]; saved[a.name] = (a.mp, a.power)
            if isinstance(m, dict): a.mp = m.get('mp', a.mp); a.power = m.get('power', a.power)
            else: a.mp = m
    try: return _run(scn, levels, n, seed, size, jobs)
    finally:
        DISABLE.clear()
        for a in CAT.values():
            if a.name in saved: a.mp, a.power = saved[a.name]
def _run(scn, levels, n, seed, size, jobs):
    rng = random.Random(seed); g = sim.gear(scn['items']); J = jobs or scn['jobs']; res = {}; pace = {}
    for lv in levels:
        W = {j['id']: [0, 0] for j in J}; ac = []
        for _ in range(n):
            ta = rng.sample(J, size); tb = rng.sample(J, size)
            A = [mk(j, lv, g, scn['abil']) for j in ta]; B = [mk(j, lv, g, scn['abil']) for j in tb]
            r, a = battle(A, B, rng); ac.append(a)
            for j in ta: W[j['id']][0] += r; W[j['id']][1] += 1
            for j in tb: W[j['id']][0] += 1 - r; W[j['id']][1] += 1
        res[lv] = {i: w / c for i, (w, c) in W.items() if c}; pace[lv] = S.mean(ac)
    return res, pace
def summarize(res, J, label=''):
    nm = {j['id']: j['name'] + '/' + str(j['race']) for j in J}
    for lv, d in res.items():
        v = sorted(d.items(), key=lambda kv: -kv[1]); vals = [x for _, x in v]
        print(f'{label} L{lv}: min {min(vals):.2f} max {max(vals):.2f} σ {S.pstdev(vals):.3f} | topo {[(nm[i][:10], round(w, 2)) for i, w in v[:5]]} | base {[(nm[i][:10], round(w, 2)) for i, w in v[-5:]]}')
if __name__ == '__main__':
    import time; t0 = time.time(); scn = sim.load()
    r, p = run(scn, n=600); summarize(r, scn['jobs'], 'v2 ATUAL'); print('ações/batalha', {k: round(v) for k, v in p.items()}, round(time.time() - t0), 's')
