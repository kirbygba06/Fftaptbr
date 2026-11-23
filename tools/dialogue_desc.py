# -*- coding: utf-8 -*-
"""Descrições de habilidade (banco 0x529514, por índice) e penalidades/bônus de lei (banco 0x54382C, por regras)."""
import re

DESC = {
 1: 'Dobra o uso de MP para\nmais dano e acerto.', 3: 'Tiro que destrói a\narmadura do alvo.',
 4: 'Sopro gélido.\nCausa dano.', 8: 'Rouba o acessório\nusado pelo inimigo.',
 10: 'O olhar silencia e\ncausa cegueira.', 14: 'Golpe horrivelmente\nrápido que condena.',
 15: 'Causa dano e empurra\no alvo.', 16: 'Rouba a hab. A do\ninimigo para você usar.',
 17: 'Ataque de investida\nnascido da magia Ultima.', 18: 'Ataque assassino nascido\nda magia Ultima.',
 19: 'Ataque de caça nascido\nda magia Ultima.', 20: 'Ataque de magilâmina\nnascido da magia Ultima.',
 21: 'Poderoso ataque sábio\nnascido da magia Ultima.', 23: 'Controla zumbis e\nvampiros.',
 24: 'Dispara bala de fogo\ncristalizado.', 27: 'Invoca Ifrit para\ncausar dano de fogo.',
 28: 'Controla mordelâminas\ne peles duras.', 30: 'Tiro que destrói a\narma do alvo.',
 31: 'Envolve o alvo em uma\nesfera de água.', 32: 'Ataque com uma maldição\npoderosa e letal.',
 35: 'Cria um redemoinho\nde vento à frente.', 36: 'Cria um turbilhão\nde vento.',
 37: 'Item: "Éter"\nRestaura 80 MP.', 39: 'Luz purificadora.\nCura status negativos.',
 41: 'Varre os monstros\ndo campo de batalha.', 42: 'Desinfeta feridas para\ncurar HP e status.',
 44: 'Causa calafrios febris\npara retardar o alvo.', 45: 'Reduz a velocidade\nde unidades próximas.',
 46: 'Item: "Beijo da Donzela"\nCura forma de sapo.', 49: 'Invoca a fada Carbúnculo\npara lançar "Refletir".',
 51: 'Neutraliza melhorias\nde status.', 54: 'Atordoa monstro. (Perde\nhab. A e R por um tempo)',
 59: 'Jutsu de fogo. Causa\ndano e confunde o alvo.', 63: 'Golpe forte. Fere também\na unidade atacante.',
 64: 'Dispara bala de gelo\ncristalizado.', 66: 'Versão mais forte de\n"Labareda". Atinge área.',
 70: 'Invoca Kirin para\ncurar HP aos poucos.', 73: 'Rouba gil do inimigo.',
 75: 'Jutsu de metal. Causa\ndano e cegueira.', 77: 'Cura HP...\nmas de quem?',
 78: 'Item: "Soft"\nCura petrificação.', 83: 'Campo de gravidade. Drena\n1/2 do HP do alvo.',
 84: 'Mini campo de gravidade.\nDrena 1/4 do HP do alvo.', 86: 'Rouba pontos de juiz\ndo inimigo.',
 91: 'Rouba EXP do inimigo.', 93: 'Melhora ataques de arma\npara causar mais dano.',
 95: 'Controla goblins e\ngorros vermelhos.', 96: 'Soco total. O dano\nvaria.',
 98: 'Causa dano e confunde\no alvo.', 100: 'Ataque de chicote. Dano\npesado a monstros.',
 102: 'Rouba a voz, silenciando\no alvo.', 103: 'Causa dano e silencia\no alvo.',
 104: 'Poder das estrelas\ncausa dano a todos.', 107: 'Lâmina carregada de\neletricidade. Causa dano.',
 108: 'Nuvem carregada de\neletricidade. Causa dano.', 109: 'Magia de raio mais forte.\nLança vários raios.',
 110: 'Poderosa magia de raio.\nLança um raio gigante.', 112: 'Invoca Shiva para\ncausar dano de gelo.',
 116: 'Balanço de cauda.\nEncanta o alvo.', 122: 'Absorve o MP usado em\nmagia contra você.',
 124: 'Reduz à metade o MP\nusado em habilidades.', 126: 'Investida do cavaleiro mog.\nAtinge inimigos longe.',
 127: 'Jutsu de água. Causa\ndano e silencia o alvo.', 131: 'Causa dano e para o alvo.',
 133: 'Reduz a velocidade do alvo.', 135: 'Rajada de golpes. Boa\nprecisão, dano leve.',
 136: 'Joga bola de água para\nretardar o alvo.', 140: 'Símbolo sagrado. Neutraliza\nmelhorias de status.',
 141: 'Foca a mente para\naumentar a precisão.', 142: 'Item: "Água Benta"\nCura zumbificação.',
 143: 'Aura abençoada. Causa\ndano sagrado em área.', 144: 'Fica transparente até\na próxima ação.',
 148: 'Aura que rouba almas.\nCausa dano ao MP.', 151: 'Envia energia pelo corpo\npara reviver unidade KO.',
 156: 'Rouba o escudo\ndo inimigo.', 159: 'Ataque capaz de acabar\ncom a vida. Condena o alvo.',
 160: 'Ataque sufocante.\nAlvo perde o próximo turno.', 161: 'Causa dano e encanta\no alvo.',
 164: 'Debandada de chocobos!\nCausa dano.', 165: 'Ataque tão forte que\nrasga a própria terra.',
 171: 'Tempestade. Dano de raio\na todos os inimigos.', 173: 'Transforma o alvo em sapo.',
 175: 'Item: "Antídoto"\nCura envenenamento.', 177: 'Jutsu de terra. Causa\ndano e retarda o alvo.',
 178: 'Invoca criatura aleatória\ndo mundo espiritual.', 183: 'Toque maligno. Drena e\nabsorve HP do alvo.',
 188: 'Joga item do estoque\npara causar dano.', 192: 'Olhar assustador.\nConfunde o alvo.',
 194: 'Gosma pegajosa.\nImobiliza o alvo.', 195: 'Tiro bem mirado. Boa\nprecisão, metade do dano.',
 198: 'Evita todo dano de MP\ne HP por um turno.', 202: 'Chakra que bane o mal.\nDestrói zumbis.',
 208: 'Grito de guerra bangaa.\nCausa dano.', 211: 'Golpe fulminante com\nestilo. Rende mais JP.',
 218: 'Fica acelerado se\ngravemente ferido.', 219: 'Gera uma bola de\nfogo que causa dano.',
 221: 'Lâmina flamejante.\nCausa dano.', 222: 'Sopro incendiário.\nCausa dano.',
 223: 'Magia de fogo mais forte.\nCausa dano incrível.', 224: 'Poderosa magia de fogo.\nCausa grande dano.',
 227: 'Ataque agressivo. Pouca\nprecisão, muito dano.', 230: 'Rouba a arma\ndo inimigo.',
 231: 'Enterra unidades\nzumbificadas na hora.', 234: 'Borrifa gás de tinta.\nCausa cegueira.',
 235: 'Causa dano e\ncegueira.', 239: 'Magia de gelo mais forte.',
 240: 'Cria um bloco de gelo\npara causar dano.', 241: 'Lâmina gélida.\nCausa dano.',
 242: 'Poderosa magia de gelo.\nLança bloco maior.', 244: 'Controla flans de gelo,\ngeleias e cremes.',
 245: 'Atinge direto a vontade\ndo alvo, ferindo o MP.', 246: 'Súbita alta de temperatura.\nCausa dano.',
 249: 'Controla olhos flutuantes\ne ahrimans.', 252: 'Poder do sol. Dano de fogo\na todos os inimigos.',
 253: 'Mexe no fluxo do tempo\npara ganhar velocidade.', 255: 'Lança um bloco de terra\npara ferir e imobilizar.',
 258: 'Reduz o dano de\nataques de arma.', 259: 'Facada de tonberry.\nReduz o HP a 1/10.',
 260: 'Joga item do estoque\npara causar dano.', 262: 'Emite luz sagrada\npara causar dano.',
 263: 'Ataque de coração puro.\nCausa dano sagrado.', 264: 'Bate na cabeça com bola\npara confundir o alvo.',
 265: 'Controla bombas e\ngranadas.', 267: 'Fogo de fada calmante.\nCura HP.',
 269: 'Aumenta def. de arma e\nres. mágica por batalha.', 270: 'Reduz o poder\nmágico do alvo.',
 271: 'Martelo místico.\nCausa dano ao MP.', 272: 'Causa dano ao MP.',
 273: 'Erva de gato!\nDeixa o alvo berserk.', 275: 'Invoca Madeen para\ncausar dano sagrado.',
 276: 'Troca o HP e o MP\ndo alvo.', 277: 'Rebate ataque mágico\ncom a mesma magia.',
 283: 'Detecta equipamento\noculto do inimigo.', 284: 'Absorve HP do alvo.',
 290: 'Jutsu de madeira. Causa\ndano e imobiliza o alvo.', 293: 'Esquiva ataques de\narco e arco longo.',
 294: 'Item: "Erva Eco"\nCura silêncio.', 297: 'Líquido corrosivo. Causa\nstatus negativo aleatório.',
 300: 'Rouba a armadura\ndo inimigo.', 302: 'Rouba vida para reduzir\no HP do alvo em 1/2.',
 303: 'Causa dano igual ao\nHP perdido.', 304: 'Causa dano ao MP.', 306: 'Controla lâmias\ne liliths.',
 307: 'Invoca Ramuh para causar\ndano de raio.', 308: 'Dispara bala de raio\ncristalizado.',
 309: 'Auto-KO. Dano em área\nigual ao próprio HP.', 311: 'Reflete magia branca,\nvermelha, temporal e negra.',
 313: 'Absorve HP do alvo.', 314: 'Convence dragão a deixar\no campo de batalha.',
 315: 'Revive automaticamente\nunidade ferida por arma.', 317: 'Revive unidade KO auto.',
 318: 'Revive unidade KO.\nCausa dano a zumbis.', 324: 'Ataca duas vezes em\nsequência rápida.',
 325: 'Lança duas magias em\nsequência rápida.', 328: 'Joga argola para\nparar o alvo.',
 331: 'Alquimia secreta. Faz\ntodos os inimigos dormirem.', 333: 'Evoca decomposição para\nferir e envenenar o alvo.',
 336: 'Mais rápido que a luz.\nFere unidades ao redor.', 338: 'Poder primordial. Muda as\nleis atuais aleatoriamente.',
 341: 'Invoca totema aleatório.', 347: 'Reduz a velocidade das\nunidades ao redor.',
 355: 'Vira goblins e\ngorros vermelhos.', 357: 'Vira bombas e\ngranadas.', 359: 'Vira lâmias e\nliliths.',
 363: 'Vira olhos flutuantes\ne ahrimans.', 365: 'Golpe que fere e\nrouba JP.', 367: 'Dá o próprio JP a um\namigo merecedor.',
 368: 'Anula um cartão amarelo\ndo registro.', 369: 'Golpe que fere e\nrouba JP.', 370: 'Dá um cartão\namarelo ao alvo.',
 371: 'Giro mortal para\ncausar dano ao redor.',
}

HIT = {'sword': 'espada', 'blade': 'lâmina', 'saber': 'sabre', 'knightsword': 'espada cav',
       'greatsword': 'espadão', 'broadsword': 'espada larga', 'knife': 'faca', 'rapier': 'florete',
       'katana': 'katana', 'spear': 'lança', 'instrument': 'instrumento', 'knuckles': 'soqueira',
       'soul': 'alma', 'staff': 'cajado', 'rod': 'bastão', 'mace': 'maça'}
VERB = {'petrifying': 'petrificar', 'frogshaping': 'virar sapo', 'poisoning': 'envenenar',
        'confusing': 'confundir', 'driving berserk': 'enlouquecer', 'silencing': 'silenciar',
        'charming': 'encantar', 'immobilizing/disabling': 'imobilizar/incapacitar', 'addling': 'atordoar',
        'slowing a unit': 'retardar uma unidade', 'stopping a unit': 'parar uma unidade',
        'causing status ailment': 'causar status negativo',
        'imbuing with "shell."': 'dar "Muralha."', 'imbuing with "protect."': 'dar "Proteção."',
        'imbuing with "haste."': 'dar "Pressa."'}
SKILL = {'Aim': 'Mira', 'Steal': 'Roubar', 'Sharpshoot': 'Tiro Certeiro', 'Call': 'Chamar', 'Items': 'Itens',
         'Dark': 'Sombria', 'Fire': 'Fogo', 'Ice': 'Gelo', 'Holy': 'Sagrado', 'Sabers': 'Sabres',
         'Knives': 'Facas', 'Katanas': 'Katanas', 'Maces': 'Maças', 'Poison': 'Veneno', 'Bind': 'Prender',
         'Slow': 'Lentidão', 'Status': 'Status', 'Haste': 'Pressa', 'Dmg2 Animal': 'Dano2 Animal'}
ABIL = {'Steal': 'Roubar', 'Control': 'Controle', 'Morph': 'Metamorfose'}


def pen(txt):
    """penalidades/bônus de lei: texto inglês decodificado -> PT, ou None"""
    m = re.match(r'^(\[R\d\]) Penalty for (?:a|an)\n(\w+) hit\.$', txt)
    if m and m.group(2) in HIT: return '%s Penalidade por\ngolpe de %s.' % (m.group(1), HIT[m.group(2)])
    m = re.match(r'^(\[R\d\]) Penalty for\n(.+)\.$', txt) or re.match(r'^(\[R\d\]) Penalty for\n(.+\.")$', txt)
    if m:
        v = m.group(2).rstrip('.') if m.group(2).endswith('.') else m.group(2)
        key = v if v in VERB else v + '.' if (v + '.') in VERB else None
        for k in (m.group(2), v, v + '.'):
            if k in VERB:
                out = VERB[k]; return '%s Penalidade por\n%s%s' % (m.group(1), out, '' if out.endswith('.') else '.')
    m = re.match(r'^(\[R\d\]) Penalty for using\nan antilaw card\.$', txt)
    if m: return '%s Penalidade por usar\numa carta antilei.' % m.group(1)
    m = re.match(r'^(\[R\d\]) Penalty for a\nsuccessful:\f"(\w+)" A-abilities\.$', txt)
    if m and m.group(2) in ABIL: return '%s Penalidade por\nsucesso:\f"%s" hab. A.' % (m.group(1), ABIL[m.group(2)])
    m = re.match(r'^(\[R\d\]) Penalty for:\n"(\w+)" A-abilities\.$', txt)
    if m and m.group(2) in ABIL: return '%s Penalidade por:\n"%s" hab. A.' % (m.group(1), ABIL[m.group(2)])
    m = re.match(r'^(\[R\d\]) Penalty for:\fMimicking action of\nprevious unit\.$', txt)
    if m: return '%s Penalidade por:\fImitar a ação da\nunidade anterior.' % m.group(1)
    m = re.match(r'^(\[R\d\]) Nullifies:\fForbidden/(.+)\nRecommended/(.+)$', txt)
    if m:
        a, b = (SKILL.get(x) for x in m.groups()[1:])
        if a and b: return '%s Anula:\fProibido/%s\nRecomendado/%s' % (m.group(1), a, b)
    m = re.match(r'^(\[R\d\]) Nullifies (R\d) laws\.$', txt)
    if m: return '%s Anula leis %s.' % (m.group(1), m.group(2))
    m = re.match(r'^(\[R\d\]) Nullifies all laws\.$', txt)
    if m: return '%s Anula todas as leis.' % m.group(1)
    m = re.match(r'^Judge point bonus\nfor successful:\f"(\w+)" A-abilities\.$', txt)
    if m and m.group(1) in ABIL: return 'Bônus de pontos de juiz\npor sucesso:\f"%s" hab. A.' % ABIL[m.group(1)]
    m = re.match(r'^Judge point bonus for\na (\w+) hit\.$', txt)
    if m and m.group(1) in HIT: return 'Bônus de pontos de juiz\npor golpe de %s.' % HIT[m.group(1)]
    m = re.match(r'^Judge point bonus for\n(.+)\.$', txt)
    if m and m.group(1) in VERB: return 'Bônus de pontos de juiz\npor %s.' % VERB[m.group(1)]
    return None
