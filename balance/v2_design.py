# -*- coding: utf-8 -*-
"""Rebalance v2: habilidades novas (slots de habilidades inúteis reaproveitados), buffs de Véus e equipamentos de contra-jogo.
Fonte única: o simulador lê SIM_MODS; o gerador do patch lê SKILLS/ITEMS; a tradução lê NAMES/DESCS (via tools/v2_text.py).
Cada habilidade nova herda do slot antigo: ID, nome/descrição (índices), custo de AP, quem aprende e qual arma ensina.
Do 'template' copia animação, flags e IA; depois troca efeitos, poder, MP, alcance e área."""
# efeitos (texto do simulador -> ID de efeito da ROM, já usados por outras habilidades)
E_ = {
 'DMG':   ('AType, Default, 100% Damage', 63),
 'HALF':  ('AType, Default, 50% Damage', 198),
 'BEAT':  ('AType, Default, 200% Damage, 0.5x Hit Rate', 66),
 'BLITZ': ('AType, Default, 50% Damage, 2.0x Hit Rate', 65),
 'DELAY': ('100%H, Default, Eff1Dep: Delay Unit', 27),
 'KNOCK': ('100%H, Default, Eff1Dep: Knockback', 75),
 'DRAIN': ('100%H, Self, Eff1Dep: Heal Eff1 Damage', 24),
 'IMMO':  ('SType, Default, Eff1Dep: Inflict Immobilize', 72),
 'SLOWD': ('SType, Default, Eff1Dep: Inflict Slow', 103),
 'PROT':  ('100%H, Default, Inflict Protect', 78),
 'SHELL': ('100%H, Default, Inflict Shell', 45),
 'REGEN': ('100%H, NonUndead, Inflict Regen', 195),
 'BOOST': ('100%H, Default, Inflict Boost', 131),
 'BLIND': ('SType, Default, Inflict Blind', 87),
 'POISON': ('SType, Default, Eff1Dep: Inflict Poison', 124),
 'DISABLE': ('SType, Default, Eff1Dep: Inflict Disable', 68),
}
T_THROW = 108   # Air Render: dano físico à distância com poder próprio
# templates (ID da habilidade cujo registro é copiado): arma corpo a corpo, arco, buff em aliado, área centrada em si, buff próprio, status em área
T_MELEE, T_BOW, T_ALLY, T_SELFAREA, T_SELF, T_AREA = 112, 178, 9, 87, 94, 32
WEAP = dict(basis='W', power=None, rng='As Weapon')
SKILLS = [
 # slot, nome sim (slot antigo), template, efeitos, extras sim, campos ROM (power, mp, rng, vrng, area, varea), nome PT, descrição PT, classes
 dict(slot=79,  old='Magicbreak',  t=T_MELEE,  eff=['DMG', 'DELAY'], sim=WEAP, rom={}, pt='Golpe Seco',
      desc='Golpe com a arma que\natrasa o turno do alvo.', cls='Soldado, Guerreiro'),
 dict(slot=83,  old='Sensor',      t=T_SELFAREA, eff=['PROT'], sim=dict(rng='Self', area='r1/v2', mp=10), rom=dict(power=0, mp=10), pt='Formação',
      desc='Dá Proteção aos\naliados ao redor.', cls='Soldado'),
 dict(slot=91,  old='Parley',      t=T_ALLY,   eff=['PROT', 'SHELL'], sim=dict(rng='3', area='One Unit', mp=12), rom=dict(mp=12, rng=3, area=1, varea=0), pt='Égide',
      desc='Dá Proteção e Barreira\na um aliado.', cls='Paladino'),
 dict(slot=95,  old='Drop Weapon', t=T_MELEE,  eff=['DMG', 'KNOCK'], sim=WEAP, rom={}, pt='Empurrão',
      desc='Golpe com a arma que\nempurra o alvo.', cls='Paladino, Defensor'),
 dict(slot=97,  old='Hibernate',   t=T_SELFAREA, eff=['SHELL'], sim=dict(rng='Self', area='r1/v2', mp=10), rom=dict(power=0, mp=10), pt='Baluarte',
      desc='Dá Barreira aos\naliados ao redor.', cls='Defensor'),
 dict(slot=126, old='Wyrmtamer',   t=T_SELF,   eff=['REGEN', 'BOOST'], sim=dict(rng='Self', area='Self', mp=0), rom={}, pt='Sangue Wyrm',
      desc='Ganha Regen e reforça\no próximo ataque.', cls='Dragoon'),
 dict(slot=181, old='Oust',        t=T_BOW,    eff=['HALF', 'SLOWD'], sim=WEAP, rom={}, pt='Rastreio',
      desc='Tiro leve que deixa\no alvo lento.', cls='Caçador'),
 dict(slot=176, old='Burial',      t=T_BOW,    eff=['DMG', 'IMMO'], sim=WEAP, rom={}, pt='Pregar',
      desc='Flecha que fere e\nimobiliza o alvo.', cls='Arqueiro'),
 dict(slot=154, old='Unspell',     t=T_THROW,  eff=['DMG', 'DISABLE'], sim=dict(basis='W', power=35, rng='4', area='One Unit', mp=6), rom=dict(power=35, mp=6, rng=4, vrng=0), pt='Shuriken',
      desc='Arremessa um shuriken\nque fere e paralisa.', cls='Ninja'),
 dict(slot=137, old='Mog Peek',    t=T_MELEE,  eff=['DMG', 'KNOCK'], sim=WEAP, rom={}, pt='Mog Empurra',
      desc='Golpe com a arma que\nempurra o alvo, kupo!', cls='Cavaleiro Mog'),
 dict(slot=107, old='Holy Sign',   t=T_SELFAREA, eff=['REGEN'], sim=dict(rng='Self', area='r1/v2', mp=0), rom=dict(power=0, mp=0), pt='Mantra',
      desc='Dá Regen aos aliados\nao redor.', cls='Monge Branco'),
 dict(slot=143, old='Featherblow', t=T_MELEE,  eff=['DMG', 'DRAIN'], sim=WEAP, rom={}, pt='Lâmina Vampira',
      desc='Golpe que recupera HP\nigual ao dano causado.', cls='Esgrimista'),
 dict(slot=217, old='Gil Toss',    t=T_MELEE,  eff=['DMG', 'POISON'], sim=WEAP, rom={}, pt='Faca Venenosa',
      desc='Golpe com a arma que\nenvenena o alvo.', cls='Malabarista'),
 dict(slot=233, old='Friend',      t=T_SELFAREA, eff=['BOOST'], sim=dict(rng='Self', area='r1/v2', mp=12), rom=dict(power=0, mp=12), pt='Coragem',
      desc='Reforça o próximo\nataque dos aliados.', cls='Animista'),
 dict(slot=226, old='Aim: Wallet', t=T_BOW,    eff=['DMG', 'DELAY'], sim=WEAP, rom={}, pt='Tiro Choque',
      desc='Tiro que atrasa o\nturno do alvo.', cls='Atirador'),
]
# Véus do Ninja: poder 15 -> 28, MP 4 -> 8 (dano mais útil, ainda abaixo das magias de nível 2)
VEILS = {n: dict(power=28, mp=8) for n in ('Fire Veil', 'Water Veil', 'Earth Veil', 'Metal Veil', 'Wood Veil')}
# Equipamento de contra-jogo (efeitos de item já existentes): idx do item -> lista de efeitos (3 slots)
ITEMS = {349: [0x2C, 0, 0],    # Gauntlets (loja, 2000): imune a Encanto
         339: [0x31, 0, 0]}    # Battle Boots (loja, 1000): imune a Confusão

def sim_mods():
    out = {}
    for s in SKILLS:
        m = dict(s['sim']); m['eff'] = [E_[k][0] for k in s['eff']]
        if 'rom' in s and 'power' in s['rom'] and m.get('basis') != 'W': m.setdefault('power', s['rom']['power'] or None)
        out[s['old']] = m
    out.update(VEILS)
    return out
NAMES = {}   # preenchido pelo gerador (índice no menu -> nome PT)
DESCS = {}   # índice no banco 0x529514 -> descrição PT
