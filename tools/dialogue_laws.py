# -*- coding: utf-8 -*-
"""Descrições de leis (banco 0x54382C) restantes: tradução por modelos."""
import re

TERM = {'Skills': 'Habilidades', 'Techniques': 'Técnicas', 'Color Magic': 'Magia Cor', 'Missile': 'Projéteis', 'Chivalry': 'Cavalaria', 'Charge': 'Investida',
 'Prayer': 'Oração', 'Corner': 'Encurralar', 'Defend': 'Defesa', 'Hunt': 'Caça', 'Spirit Magic': 'Magia Espirit.', 'Time Magic': 'Magia Temp.',
 'Gunmanship': 'Artilharia', 'Summon': 'Invocação', 'Summon Magic': 'Magia de Invocação', 'Control': 'Controle', 'Morph': 'Metamorfose', 'Lightning': 'Trovão', 'Wind': 'Vento',
 'Ganging Up': 'Em Grupo', 'Copycat': 'Imitador', 'Fight': 'Luta', 'Target Area': 'Alvo: Área', 'Target All': 'Alvo: Todos', 'Swords': 'Espadas', 'Blades': 'Lâminas',
 'Staves': 'Cajados', 'Rods': 'Bastões', 'Knightswords': 'Esp. Cavaleiro', 'Kngtswords': 'Esp. Cav.', 'Instruments': 'Instrumentos', 'Greatswords': 'Espadões',
 'Rapiers': 'Floretes', 'Broadswords': 'Montantes', 'Spears': 'Lanças', 'Knuckles': 'Soqueiras', 'Soul': 'Alma', 'Healing': 'Cura', 'Status': 'Status', 'Petrify': 'Pedra',
 'Frog': 'Sapo', 'Confuse': 'Confusão', 'Berserk': 'Fúria', 'Silence': 'Silêncio', 'Charm': 'Encanto', 'Addle': 'Atordoar', 'Stop': 'Parar', 'Shell': 'Barreira',
 'Protect': 'Proteger', 'Poison': 'Veneno', 'Dmg2 Human': 'Dano2 Hum.', 'Dmg2 Bangaa': 'Dano2 Bangaa', 'Dmg2 Nu Mou': 'Dano2 Nu Mou', 'Dmg2 Viera': 'Dano2 Viera',
 'Dmg2 Moogle': 'Dano2 Moogle', 'Fire': 'Fogo', 'Ice': 'Gelo', 'Holy': 'Sagrado', 'Dark': 'Trevas', 'Skill': 'Hab.', 'Tech': 'Téc.', 'Aim': 'Pontaria',
 'Sharpshoot': 'Tiro Certeiro', 'Call': 'Chamar', 'Item': 'Itens', 'Items': 'Itens', 'Sabers': 'Sabres', 'Knives': 'Facas', 'Katanas': 'Katanas', 'Maces': 'Maças',
 'Bind': 'Prender', 'Slow': 'Lentidão', 'Haste': 'Acelerar'}
RACE = {'human': 'um humano', 'bangaa': 'um bangaa', 'nu mou': 'um nu mou', 'viera': 'uma viera', 'moogle': 'um moogle', 'monster': 'um monstro'}


def pen2(t):
    m = re.match(r'^(\[R\d\]) Nullifies:\fForbidden/(.+)\nRecommended/(.+)$', t)
    if m:
        a, b = TERM.get(m.group(2)), TERM.get(m.group(3))
        if a and b: return '%s Anula:\fProibido/%s\nRecomendado/%s' % (m.group(1), a, b)
        return None
    head = None
    for pat, rep in [
        (r'^(\[R\d\]) Penalty for a\nsuccessful hit with:\f', r'\1 Penalidade por golpe\nbem-sucedido com:\f'),
        (r'^(\[R\d\]) Penalty for a\nbow/greatbow/gun hit\.$', r'\1 Penalidade por golpe\nde arco/arcão/arma.'),
        (r'^(\[R\d\]) Penalty for using\nanything other than:\f', r'\1 Penalidade por usar\nalgo além de:\f'),
        (r'^(\[R\d\]) Penalty for:\nUsing combos\.\fOnly the initiating\nunit is penalized\.$', r'\1 Penalidade por:\nUsar combos.\fSó quem inicia\né penalizado.'),
        (r'^(\[R\d\]) Penalty for a\nsuccessful "Fight\."\fAbilities are not\npenalized\.$', r'\1 Penalidade por\n"Luta" bem-sucedida.\fHabilidades não são\npenalizadas.'),
        (r'^Judge point bonus for\na successful hit with:\f', 'Bônus de pontos de juiz\npor golpe com:\f'),
        (r'^Judge point bonus for\na successful:\fBow/greatbow/gun hit\.$', 'Bônus de pontos de juiz\npor golpe de:\fArco/arcão/arma.'),
        (r'^Judge point bonus for:\fMimicking action of\nprevious unit\.$', 'Bônus de juiz por:\fImitar a ação da\nunidade anterior.'),
        (r'^Judge point bonus for:\nUsing a combo\.\fOnly the initiating\nunit is rewarded\.$', 'Bônus de juiz por:\nUsar um combo.\fSó quem inicia\né premiado.'),
        (r'^Judge point bonus for\nan instrument hit\.$', 'Bônus de pontos de juiz\npor golpe de instrumento.')]:
        if re.match(pat, t): head = re.sub(pat, rep, t, count=1); break
    if head is None: return None
    # corpo
    m = re.match(r'^(.*?\f)?(.*)$', head, re.S)
    body = head
    if '\f' in head and not re.match(r'^(\[R\d\]) Penalidade por usar', head) or True:
        pre, _, rest = head.partition('\f') if '\f' in head else (head, '', '')
    else: pre, rest = head, ''
    if rest:
        r = rest
        r = re.sub(r'^"([\w ]+)"\nA-abilities\.', lambda mo: '"%s"\nhab. A.' % TERM.get(mo.group(1), mo.group(1)), r)
        r = re.sub(r'^"([\w ]+)" A-abilities\.', lambda mo: '"%s" hab. A.' % TERM.get(mo.group(1), mo.group(1)), r)
        r = r.replace('(ex: "Ninja Skill")', '(ex: "Hab. Ninja")').replace('(ex: "Battle Tech")', '(ex: "Téc. de Batalha")')
        r = r.replace('White, black, red, or\nblue magic.', 'Magia branca, negra,\nvermelha ou azul.').replace('White, black, red,\nand blue magic.', 'Magia branca, negra,\nvermelha e azul.')
        r = r.replace('A-abilities with area\neffect of 2+ panels.', 'Hab. A com área de\nefeito de 2+ casas.')
        r = r.replace('A-abilities affecting\nentire field.', 'Hab. A que afetam\no campo todo.').replace('A-abilities affecting\nthe entire field.', 'Hab. A que afetam\no campo todo.')
        r = r.replace('A-abilities that\nheal HP.', 'Hab. A que\ncuram HP.')
        r = re.sub(r'Offensive actions\nagainst a (nu mou|\w+)\.', lambda mo: 'Ações ofensivas\ncontra %s.' % RACE.get(mo.group(1), mo.group(1)), r)
        mo = re.match(r'^(\w+) actions/\nA-abilities\.\f(\w+) weapons\s*(?:are\s*)?\n?(?:are\s*)?not\s*\n?(penalized|rewarded)\.$', r)
        if mo:
            e = TERM.get(mo.group(1), mo.group(1)); pr = 'penalizadas' if mo.group(3) == 'penalized' else 'premiadas'
            r = 'Ações/hab. A de\n%s.\fArmas de %s não\nsão %s.' % (e, e, pr)
        rest = r
        out = pre + '\f' + rest
    else: out = pre
    # pendências em inglês?
    if re.search(r'A-abilit|Penalty|Judge|actions|against|panels|rewarded|penalized|Offensive', out): return None
    return out
