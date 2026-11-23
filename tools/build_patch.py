#!/usr/bin/env python3
"""Gera patches/FFTA_ptBR_slot_ingles.ips para a ROM europeia (AFXP) de FFTA.

Uso:  python3 tools/build_patch.py ROM.gba [saida.ips]

O que faz
  1. Pega as traduções de menu/status já feitas no slot italiano (reference/*.ips)
     e as aplica no slot INGLÊS (mesmos índices da tabela de ponteiros).
  2. Traduz os nomes de classes (tabela de nomes em 0x724C34, slot inglês).
  3. Cria glifos reais de ã e õ (a fonte da ROM não tem), sobrescrevendo ä e ö.

Layout descoberto
  - Tabela de menus:   EN 0x720D44 + 4*i   (IT = EN + 0x2A328)
  - Tabela de nomes:   EN 0x724C34 + 4*i   (IT = EN + 0x2A5F4)
  - Fonte: 0x4954DC, glifos 16x16 de 128 bytes (tiles TL,BL,TR,BR, 4bpp, valores 0-3)
  - Strings "01": 01 + códigos(glifo+1) + 00 | "80": pares 80 xx (xx = glifo), espaço = 40 73
"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(__file__))
from ips import parse

HERE = os.path.dirname(os.path.abspath(__file__))
REF_IPS = os.path.join(HERE, '..', 'reference', 'FFTA_ptBR_v2_menus_status_slot_italiano.ips')

EN_MENU, IT_MENU = 0x720D44, 0x74B06C
EN_NAMES = 0x724C34
TEXT_BASE = 0xFE5000          # espaço livre (o patch italiano usa 0xFE4000-0xFE4587)
FONT = 0x4954DC
G_A_TILDE, G_O_TILDE = 27, 40  # glifos ä e ö -> viram ã e õ

# ---------- codificação ----------
ACC01 = {'à': 0x19, 'á': 0x1A, 'â': 0x1B, 'ã': 0x1C, 'é': 0x1E, 'ê': 0x1F, 'í': 0x22,
         'ó': 0x27, 'ô': 0x28, 'õ': 0x29, 'ú': 0x2B, 'ç': 0x30,
         'Á': 0x04, 'Â': 0x05, 'Ê': 0x09, 'É': 0x08, 'Í': 0x0C, 'Ó': 0x11, 'Ú': 0x15}
PUNCT01 = {'+': 0xFE, '|': 0xFF, '.': 0xE5, ',': 0xED, '!': 0xEC, '?': 0xEB, ':': 0xEF, '/': 0xF2, "'": 0xF5}


def code01(ch):
    if 'A' <= ch <= 'Z': return 0xB1 + ord(ch) - 65
    if 'a' <= ch <= 'z': return 0xCB + ord(ch) - 97
    if '0' <= ch <= '9': return 0xA7 + int(ch)
    if ch in ACC01: return ACC01[ch]
    if ch in PUNCT01: return PUNCT01[ch]
    raise ValueError('caractere sem glifo: %r' % ch)


def enc(text, fmt):
    if fmt == 1:
        assert ' ' not in text
        return bytes([1]) + bytes(code01(c) for c in text) + b'\0'
    out = bytearray()
    for c in text:
        if c == ' ': out += b'\x40\x73'
        else: out += bytes([0x80, code01(c) - 1])
    return bytes(out) + b'\0'


# ---------- tradução das classes (idx da tabela de nomes -> PT-BR) ----------
CLASSES = {
    3: 'Mago Azul', 4: 'Mago Vermelho', 5: 'Assassino', 6: 'Alquimista', 10: 'Mordelâmina',
    11: 'Defensor', 12: 'Engenhoqueiro', 14: 'Gladiador', 16: 'Mago Negro', 17: 'Ilusionista',
    20: 'Ladrão', 21: 'Elementalista', 22: 'Malabarista', 23: 'Artilheiro', 24: 'Invocador',
    25: 'Mago Branco', 26: 'Atirador', 28: 'Sábio', 29: 'Soldado', 32: 'Lutador',
    33: 'Animista', 34: 'Mago Temporal', 35: 'Metamorfo', 39: 'Paladino', 40: 'Templário',
    41: 'Caçador', 42: 'Bispo', 43: 'Guerreiro', 44: 'Quebraqueixo', 45: 'Esgrimista',
    50: 'Monge Branco', 51: 'Domador', 52: 'Cavaleiro Mog', 55: 'Arqueiro', 63: 'Caçarunas',
    64: 'Hermético', 68: 'Juiz Mestre', 69: 'Juiz', 71: 'Bibliotecário', 91: 'Cavaleiro Negro',
    92: 'Cav. da Arca', 96: 'Espadachim', 107: 'Cav. Rúnico', 118: 'Mestre Espada',
}


# monstros, chefes e papéis de NPC da tabela de nomes (nomes próprios mantidos)
MONSTERS = {
    2: 'Flan de Gelo', 7: 'Formigaleão', 8: 'Creme', 9: 'Vampiro', 15: 'Granada',
    19: 'Trovodraco', 27: 'Duende', 30: 'Zumbi', 37: 'Mestre Tonberry', 46: 'Gelodraco',
    47: 'Pele Dura', 48: 'Olho Flutuante', 49: 'Bomba', 54: 'Malboro Grande',
    59: 'Gorro Vermelho', 60: 'Wyrm de Fogo', 61: 'Pantera Rubra', 62: 'Gelatina',
    70: 'Novato', 72: 'Líder de Turma', 73: 'Prof. de E.F.', 75: 'Enfermeira',
    76: 'Zelador', 77: 'Sr. Leslaie', 78: 'Rainha Guerreira', 83: 'Arrombador',
    84: 'Caixa', 85: 'Estátua', 86: 'Esfera', 87: 'Capo Borzoi', 88: 'Chefe Borzoi',
    94: 'Wyrm Mundial', 95: 'Chefe Ba', 98: 'Malboro Chefe', 99: 'Ferreiro',
    100: 'Armeiro', 101: 'Coeurl Supremo', 102: 'Perdido', 103: 'Sentinela',
    104: 'Corvo Sinistro', 106: 'Asas Rubras', 108: 'Rainha Lamia', 112: 'Lorde Sinistro',
    114: 'Chefe Hel', 115: 'Chefe Gelm', 116: 'Chefe Kagle', 117: 'Chefe Fes',
    120: 'Diaboro', 121: 'Clã Borzoi', 122: 'Oficial',
}
CLASSES.update(MONSTERS)

# espadas, lâminas e sabres (tabela de nomes 124-168); nomes lendários mantidos
WEAPONS = {
    124: 'Espada Curta', 125: 'Espada de Prata', 126: 'Espada Buster', 127: 'Espada Ladra',
    128: 'Espada Vendaval', 129: 'Espada Rubra', 132: 'Espada Mithril', 133: 'Espada Vitória',
    134: 'Espada Onion', 136: 'Espada Laglace', 137: 'Lâmina Ceifeira', 138: 'Lâmina Sombria',
    139: 'Lâmina Solar', 140: 'Lâmina Atmos', 141: 'Língua de Fogo', 142: 'Lâmina do Ar',
    143: 'Gume de Gelo', 144: 'Lâmina Kwigon', 145: 'Lâmina Ogun', 146: 'Lâmina Pérola',
    147: 'Lâmina Paraiba', 148: 'Lâmina Vênus', 149: 'Lâmina Materia', 150: 'Lâmina Mithril',
    151: 'Lâmina Ébano', 152: 'Lâmina Adaman', 153: 'Ayvuir Vermelho', 154: 'Ayvuir Azul',
    155: 'Sabre Azul', 157: 'Sabre Aqua', 159: 'Manganês', 160: 'Sabre Mithril',
    162: 'Sabre da Alma', 164: 'Apocalipse',
}
WEAPONS.update({
    171: 'Gume Mithril', 174: 'Sequência', 176: 'Espada Antiga', 177: 'Espada Diamante',
    178: 'Gume Duro', 181: 'Espada Mestra', 183: 'Prisma de Gelo', 185: 'Espada Sansão',
    187: 'Predador', 189: 'Espada El Cid', 194: 'Espada Fera', 195: 'Eclipse',
    197: 'Canivete', 198: 'Faca Kris', 202: 'Adaga Rondel', 205: 'Quebra Espada',
    206: 'Oricalco', 208: 'Faca Mithril', 211: 'Ferrão', 216: 'Florete de Prata',
    219: 'Esmaga Mago', 224: 'Florete Mithril', 225: 'Última Carta', 228: 'Buraco Aéreo',
    229: 'Faca Ninja', 233: 'Caça Pétalas', 236: 'Nuvem Celeste', 240: 'Épée Mithril',
    244: 'Cajado Branco', 245: 'Cajado Guarda', 246: 'Cajado Juiz', 247: 'Cajado Cura',
    248: 'Cajado Puro', 249: 'Cajado Bênção', 250: 'Cajado Cobra', 251: 'Cajado Fonte',
    252: 'Cajado Garnet', 253: 'Cajado Alegria', 254: 'Cajado Nirvana', 255: 'Cajado Mithril',
    256: 'Cajado Poder', 257: 'Vigia dos Sonhos',
})
WEAPONS.update({
    258: 'Bastão', 259: 'Bastão Ígneo', 260: 'Bastão Trovão', 261: 'Bastão Granizo',
    262: 'Bastão Terra', 263: 'Bastão Força', 264: 'Bastão Chama', 265: 'Bastão Thor',
    266: 'Bastão Frio', 267: 'Bastão Estelar', 268: 'Bastão Princesa', 269: 'Bastão Mithril',
    270: 'Bastão Herege', 272: 'Maça de Guerra', 273: 'Maça de Energia', 274: 'Maça Druida',
    275: 'Báculo Sábio', 276: 'Estrela Matutina', 277: 'Mandrágora', 278: 'Báculo da Vida',
    279: 'Maça Lótus', 280: 'Cauda Escorp.', 281: 'Maça Zeus', 282: 'Maça Mithril',
    283: 'Cacto', 285: 'Arco Longo', 286: 'Arco Carvão', 287: 'Arco Espinho', 288: 'Arco Prego',
    289: 'Arco de Prata', 290: 'Arco de Ártemis', 291: 'Arco Yoichi', 292: 'Arco Alvo',
    293: 'Arco Perseu', 294: 'Arco Mithril', 295: 'Arco Crescente', 296: 'Malarco',
    297: 'Arco Ventoso', 298: 'Arco Ranger', 299: 'Cranequim', 300: 'Arco Gêmeo',
    301: 'Arco Caça', 302: 'Arco Fada', 303: 'Arco Hades', 304: 'Arco Nike', 305: 'Arco Mestre',
    306: 'Arco Juramento', 307: 'Sétimo Céu', 308: 'Tiro Mithril', 309: 'Arco Marduk',
    310: 'Arco Gastra', 311: 'Balestra',
})
WEAPONS.update({
    312: 'Dardo', 313: 'Lança de Lava', 315: 'Lança de Gelo', 316: 'Partasana',
    317: 'Lança de Kain', 318: 'Tridente', 319: 'Barba de Dragão', 320: 'Lança Mithril',
    321: 'Lança de Odin', 322: 'Lança Fera', 323: 'Espeto Bangaa', 324: 'Sino Demônio',
    325: 'Sino de Vidro', 326: 'Clarim', 327: 'Concha', 328: 'Sino da Terra',
    329: 'Quena Negra', 330: 'Flauta Sátiro', 331: 'Harpa de Fada', 332: 'Flauta Aona',
    333: 'Sineta da Cura', 334: 'Cordas Rubras', 335: 'Sino Mithril', 336: 'Rabeca Sombria',
    337: 'Castanhola Fell', 338: 'Soqueira Dura', 339: 'Sol Nascente', 340: 'Soqueira Doente',
    341: 'Garras do Sonho', 342: 'Soqueira Kaiser', 343: 'Garras de Gato', 344: 'Sobrevivente',
    345: 'Presas Brancas', 346: 'Mão de Deus', 347: 'Presas de Tigre', 348: 'Garras da Morte',
    349: 'Garras Mithril', 350: 'Graxa Explosiva', 351: 'Mãos Mágicas', 352: 'Alma Goblin',
    353: 'Alma Flan', 354: 'Alma Bomba', 355: 'Alma Dragão', 356: 'Alma Lamia',
    357: 'Alma Inseto', 358: 'Alma Pantera', 359: 'Alma Malboro', 360: 'Alma Olho',
    361: 'Alma Mithril', 362: 'Alma Sinistra', 363: 'Alma Rukavi', 364: 'Arma Aiot',
    365: 'Canhão de Prata', 366: 'Arma Tumulto', 367: 'Rifle Caos', 368: 'Arma Perdida',
    369: 'Pacificador', 370: 'Arma Giot', 371: 'Cano Longo', 372: 'Forasteiro',
    373: 'Arma Mithril', 375: 'Arma Chamadora',
})
WEAPONS.update({
    376: 'Escudo Bronze', 377: 'Escudo Redondo', 378: 'Escudo Opala', 379: 'Escudo de Gelo',
    380: 'Escudo Chama', 381: 'Escudo Égide', 382: 'Escudo Genji', 383: 'Escudo Sacri',
    384: 'Escudo Shijin', 385: 'Escudo Choco', 387: 'Escudo Devaneio', 388: 'Elmo de Bronze',
    389: 'Elmo de Ferro', 390: 'Elmo Opala', 391: 'Elmo Cruz', 392: 'Elmo Diamante',
    393: 'Elmo Genji', 394: 'Elmo Desfile', 395: 'Elmo Hanya', 396: 'Elmo Bangaa',
    398: 'Presilha', 399: 'Fita', 400: 'Gorro de Pena', 401: 'Diadema', 402: 'Boina Verde',
    403: 'Bandana', 404: 'Chapéu de Mago', 405: 'Grampo de Ouro', 406: 'Chapéu Ladrão',
    407: 'Chapéu Negro', 408: 'Chapéu Branco', 409: 'Chapéu Acácia', 411: 'Couraça',
    412: 'Armad. Bronze', 413: 'Armad. de Ferro', 414: 'Placas', 415: 'Armad. de Ouro',
    416: 'Armad. Diamante', 417: 'Armadura Opala', 418: 'Malha Carabini', 419: 'Malha Espelho',
    420: 'Malha Dragão', 421: 'Armadura Genji', 423: 'Armad. Adaman', 424: 'Armad. Materia',
    425: 'Peitoral', 426: 'Traje de Couro', 427: 'Placa de Malha', 428: 'Colete Adaman',
    429: 'Colete Sobrev.', 430: 'Brigantina', 431: 'Kimono de Judô', 432: 'Faixa de Poder',
    433: 'Traje Gaia', 434: 'Placa Minerva', 435: 'Traje Ninja', 436: 'Traje Sombrio',
    438: 'Colete Miragem', 439: 'Traje Borracha', 440: 'Placa de Osso', 441: 'Único',
    442: 'Conjunto Brint', 443: 'Conjunto Galmia', 444: 'Casaco do Juiz', 445: 'Manto Templo',
    446: 'Manto Cânhamo', 447: 'Manto de Seda', 448: 'Manto Mago', 449: 'Manto de Visco',
    450: 'Manto Chama', 451: 'Manto Trovão', 452: 'Manto Rajada', 453: 'Manto Branco',
    454: 'Manto Negro', 455: 'Manto de Luz', 456: 'Manto Senhorial', 457: 'Casaco de Prata',
    458: 'Manto Vermelho', 459: 'Manto Sábio', 460: 'Manto Mágico', 461: 'Capa Ceifador',
})
WEAPONS.update({
    462: 'Botas de Batalha', 463: 'Botas Espinhos', 464: 'Botas Corrida', 465: 'Botas Vermelhas',
    466: 'Botas de Pena', 468: 'Sapatos Galmia', 469: 'Sapatos de Fada', 471: 'Tabi Ninja',
    472: 'Manoplas', 473: 'Braçal Ladrão', 474: 'Braçadeiras', 475: 'Braçal Genji',
    476: 'Luvas de Fogo', 477: 'Braçal de Osso', 478: 'Anel da Sorte', 479: 'Anel Mágico',
    480: 'Anel Angelical', 481: 'Escaravelho', 482: 'Brinco de Rubi', 483: 'Braçal Estrela',
    484: 'Gema Mindu', 485: 'Poção', 486: 'Hi|Poção', 487: 'X|Poção', 488: 'Éter',
    489: 'Elixir', 490: 'Antídoto', 491: 'Colírio', 492: 'Erva Eco', 493: 'Beijo da Donzela',
    494: 'Soft', 495: 'Água Benta', 496: 'Bandagem', 497: 'Cura Total', 498: 'Pena de Fênix',
})
WEAPONS.update({646: 'Fogo', 647: 'Gelo', 648: 'Raio', 649: 'Sagrado', 650: 'Vento'})   # elementos
CLASSES.update(WEAPONS)

# entradas do menu que o patch italiano não cobria (idx da tabela de menus -> PT-BR)
EXTRA_MENU = {34: 'Trocar Itens', 761: 'Lento', 762: 'Lento'}

# conjuntos de habilidades / categorias de menu (idx 95-139 da tabela de menus)
SKILLSETS = {
    95: 'Guardacartas', 96: 'Banco de Monstros', 97: 'Combate', 98: 'Magia', 99: 'Ferraria',
    100: 'Artesanato', 101: 'Avaliar', 102: 'Coletar', 103: 'Negociar', 104: 'Rastrear',
    105: 'Itens', 106: 'Magia Azul', 107: 'Magia Vermelha', 108: 'Truques', 109: 'Controle',
    110: 'Caça', 111: 'Cavalaria', 112: 'Oração', 113: 'Canção', 114: 'Magia Negra',
    115: 'Tal. Sagaz', 116: 'Tal. Fantasma', 117: 'Téc. Sagrada', 118: 'Chama',
    119: 'Tormenta de Areia', 120: 'Podridão', 121: 'Encurralar', 122: 'Acrobacia',
    123: 'Pontaria', 124: 'Defesa', 125: 'Invocação', 126: 'Fedor', 127: 'Magia Branca',
    128: 'Debilitar', 129: 'Magia Espirit.', 130: 'Téc. de Batalha', 131: 'Téc. de Monge',
    132: 'Tiro Certeiro', 133: 'Soco', 134: 'Investida', 135: 'Téc. de Lutador',
    136: 'Magia Temporal', 137: 'Téc. de Esgrima', 138: 'Wyrm de Gelo', 139: 'Metamorfose',
}
SKILLSET_MAX_PX = 82   # inglês/italiano usam até ~77px; exceções propositais: 96 e 119
EXTRA_MENU.update(SKILLSETS)

# habilidades individuais (idx 140-574; 146, 178 e 207 têm códigos de controle e ficam em inglês)
ABILITIES = {
    140: 'Derreter', 141: 'Tal. Ninja', 142: 'Roubar', 143: 'Mirar', 144: 'Pandora',
    145: 'Garrada', 147: 'Olhar', 148: 'Chamar', 149: 'Téc. de Dragão', 150: 'Tal. Alquímico',
    151: 'Rancor', 152: 'Runas', 153: 'Ocultismo', 154: 'Magia Sombria', 155: 'Intuição',
    156: 'Gênese', 157: 'Wicca', 158: 'Expulsar', 159: 'Magitormenta', 160: 'Golpe',
    161: 'Calafrio', 162: 'Chamuscar', 163: 'Bum!', 164: 'Dracochama',
    165: 'Dracoraio', 166: 'Presa Venenosa', 167: 'Aderir', 168: 'Esmagar',
    169: 'Malícia', 170: 'Arranhão', 171: 'Fedentina', 172: 'Brilho', 173: 'Iludir',
    174: 'Fluorescer', 175: 'Lei Avançada', 176: 'Julgamento', 177: 'Carta Branca',
    179: 'Turbo MP', 180: 'Cura da Terra', 181: 'Mirar: Armad.', 182: 'Sopro Gélido',
    183: 'Itens', 184: 'Parafuso Azul', 185: 'Mola Vermelha', 186: 'Roubar: Acess.',
    187: 'Investida Mog', 188: 'Olhar Maligno', 189: 'Pesadelo', 190: 'Mirar: Pernas',
    191: 'Astra', 192: 'Foice Mortal', 193: 'Ataque Mog', 194: 'Roubar: Habilid.',
    195: 'Carga Ultima', 196: 'Esmagar Ultima', 197: 'Tiro Ultima', 198: 'Espada Ultima',
    199: 'Golpe Ultima',
}
ABILITIES.update({
    200: 'Vida|Plena', 201: 'Não Morto', 202: 'Tiro de Fogo', 203: 'Capturar', 204: 'Zumbificar',
    205: 'Ifrit', 206: 'Fera de Pedra', 208: 'Mirar: Arma', 209: 'Água', 210: 'Vodu',
    211: 'Mirar: Braço', 212: 'Redemoinho', 213: 'Rajada de Ar', 214: 'Aero', 215: 'Éter',
    216: 'X|Poção', 217: 'Esuna', 218: 'Elixir', 219: 'Exilar', 220: 'Socorro', 221: 'Aura',
    222: 'Febre', 223: 'Grito de Guerra', 224: 'Beijo Donzela', 225: 'Guarda Mog',
    226: 'Sem|Guarda', 227: 'Carbuncle', 228: 'Onda Sonora', 229: 'Anular Magia',
    230: 'Cuidar', 231: 'Contra Ataque', 232: 'Atordoar', 233: 'Canto do Sapo',
    234: 'Bomba de Fogo', 235: 'Prender Sombra', 236: 'Pegada Macaco', 237: 'Véu de Fogo',
    238: 'Proteger', 239: 'Roubar: Elmo', 240: 'Mastigar', 241: 'Pancada', 242: 'Tiro de Gelo',
    243: 'Mola Amarela', 244: 'Giga Flare', 245: 'Pegar', 246: 'Mirar: Vitais',
    247: 'Ressoar', 248: 'Kirin', 249: 'Jogar Gil', 250: 'Assaltar', 251: 'Roubar: Gil',
    252: 'Animar', 253: 'Véu de Metal', 254: 'Disco de Prata', 255: 'Bateria de Ouro',
    256: 'Amolecer', 257: 'Apressar', 258: 'Rasgar Ar', 259: 'Mau Hálito', 260: 'Beijo',
    261: 'Demi', 262: 'Quarter', 263: 'Mithril', 264: 'Roubar: JP', 265: 'Lingote Negro',
    266: 'Cura', 267: 'Cura++', 268: 'Cura+', 269: 'Roubar: EXP', 270: 'Olhar Mau',
    271: 'Atq. de Arma+', 272: 'Conversar', 273: 'Goblin', 274: 'Soco Goblin', 275: 'Inseto',
    276: 'Tiro Confuso', 277: 'Círculo', 278: 'Cascavel', 279: 'Mirar: Carteira',
    280: 'Silêncio', 281: 'Tiro Mudo', 282: 'Cruz Estelar', 283: 'Culinária',
    284: 'Trovão', 285: 'Espada Raio', 286: 'Sopro Elétrico', 287: 'Trovão++', 288: 'Trovão+',
    289: 'Torm. de Areia', 290: 'Shiva', 291: 'Shell', 292: 'Afonia', 293: 'Raio Oleoso',
    294: 'Abanar Cauda', 295: 'Roleta', 296: 'Explodir', 297: 'Ar Brilhante', 298: 'Saltar',
    299: 'Julgar', 300: 'Absorver MP', 301: 'Miasma', 302: 'Meio MP', 303: 'Conselho',
    304: 'Lança Mog', 305: 'Véu de Água', 306: 'Pó de Estrela', 307: 'Estaca Sombria',
    308: 'Parar', 309: 'Tiro de Stop',
})
ABILITIES.update({
    310: 'Calafrio', 311: 'Quebra Veloc.', 312: 'Sorriso', 313: 'Sopro de Pena',
    314: 'Chuva do Sono', 315: 'Sono', 316: 'Lentidão', 317: 'Borboleta',
    318: 'Sinal Sagrado', 319: 'Concentrar', 320: 'Água Benta', 321: 'Cruz Santa',
    322: 'Ocultar', 323: 'Revelar', 324: 'Sujar Provas', 325: 'Sacar Arma',
    326: 'Esfera da Alma', 327: 'Último Suspiro', 328: 'Geomancia', 329: 'Reviver',
    330: 'Estrondo Sônico', 331: 'Tornado Feroz', 332: 'Ataque Enxame', 333: 'Escudeiro',
    334: 'Roubar: Escudo', 335: 'Impulso', 336: 'Espiada Mog', 337: 'Xeque Mate',
    338: 'Sufocar', 339: 'Tiro Encantado', 340: 'Chakra', 341: 'Provocar',
    342: 'Ataque Chocobo', 343: 'Rasgar Terra', 344: 'Ciclone', 345: 'Subjugar',
    346: 'Death', 347: 'Dispel', 348: 'Voz do Anjo', 349: 'Tempestade', 350: 'Hibernar',
    351: 'Sapo', 352: 'Sapo Venenoso', 353: 'Antídoto', 354: 'Garra Venenosa',
    355: 'Véu da Terra', 356: 'Amigo', 357: 'Dragão', 358: 'Mata Wyrm',
    359: 'Poder de Dragão', 360: 'Drenar', 361: 'Toque Drenante', 362: 'Tonberry',
    363: 'Falcão Noturno', 364: 'Adaga', 365: 'Ceifar', 366: 'Arremessar', 367: 'Quebra Ossos',
    368: 'Gema Cromática', 369: 'Espada Dupla', 370: 'Encarar', 371: 'Dilacerar', 372: 'Gosma',
    373: 'Fazer Mira', 374: 'Transpassar', 375: 'Cupido', 376: 'Guarda Experta', 377: 'Bio',
    378: 'Hi|Poção', 379: 'Tremor', 380: 'Exorcizar', 381: 'Contrafogo', 382: 'Punho Distante',
    383: 'Revidar', 384: 'Barreira', 385: 'Quebra Poder', 386: 'Grito Bangaa', 387: 'Pantera',
    388: 'Bandagem', 389: 'Caçada', 390: 'Cura Total', 391: 'Ajuda Mog', 392: 'Contar Ovelhas',
    393: 'Tapa', 394: 'Apressar Final', 395: 'Berserk Final', 396: 'Haste Final', 397: 'Fogo',
    398: 'Chicote de Fogo', 399: 'Espada de Fogo', 400: 'Sopro de Fogo', 401: 'Fogo++',
    402: 'Fogo+', 403: 'Acelerar', 404: 'Selo de Pedra', 405: 'Surra', 406: 'Fênix',
    407: 'Pena de Fênix', 408: 'Roubar: Arma', 409: 'Enterro', 410: 'Largar Arma',
    411: 'Meteorito', 412: 'Cegar', 413: 'Tiro Cegante', 414: 'Blaster', 415: 'Apagão',
    416: 'Piscada Gélida', 417: 'Gelo++', 418: 'Gelo', 419: 'Espada de Gelo',
})
ABILITIES.update({
    420: 'Gelo+', 421: 'Blitz', 422: 'Flan', 423: 'Golpe de Mana', 424: 'Flare', 425: 'Quebrar',
    426: 'Ataque Ígneo', 427: 'Olho Flutuante', 428: 'Protect', 429: 'Troca Elemental',
    430: 'Proeminência', 431: 'Haste', 432: 'Quebra Haste', 433: 'Pó Pesado', 434: 'Veneno',
    435: 'Esquecimento', 436: 'Def. de Arma+', 437: 'Faca', 438: 'Arremesso', 439: 'Poção',
    440: 'Holy', 441: 'Lâmina Sagrada', 442: 'Bola', 443: 'Bomba', 444: 'Vento Branco',
    445: 'Chama Branca', 446: 'Beijo Tóxico', 447: 'Guarda Poderosa', 448: 'Quebra Mente',
    449: 'Martelo Mágico', 450: 'Quebra Magia', 451: 'Erva de Gato', 452: 'Arqueiro Mortal',
    453: 'Madeen', 454: 'Magia Matra', 455: 'Retornar Magia', 456: 'Poder Mág.+', 457: 'Defesa',
    458: 'Raise', 459: 'Reflexo', 460: 'Engr. Verde', 461: 'Sensor', 462: 'Mutilar',
    463: 'Karma', 464: 'Colírio', 465: 'Meteor', 466: 'Imunidade', 467: 'Manutenção',
    468: 'Véu de Madeira', 469: 'Malboro', 470: 'Fogo de Volta', 471: 'Bloquear Flechas',
    472: 'Erva Eco', 473: 'Sacrifício', 474: 'Unicórnio', 475: 'Ácido', 476: 'Fada', 477: 'Noite',
    478: 'Roubar: Armad.', 479: 'Aprendizado', 480: 'Reduzir', 481: 'Quebra Vida', 482: 'Raspar',
    483: 'Investida', 484: 'Lamia', 485: 'Ramuh', 486: 'Tiro Raio', 487: 'Derretimento',
    488: 'Auto|Regen', 489: 'Reflect', 490: 'Luva Limite', 491: 'Lanceta', 492: 'Doma Wyrm',
    493: 'Dracocoração', 494: 'Mão Dupla', 495: 'Auto|Vida', 496: 'Vida', 497: 'Escudo Mog',
    502: 'Tiro Duplo', 503: 'Magia Dupla', 504: 'Dilúvio', 505: 'Golpe Selvagem', 506: 'Anel',
    507: 'Explodir', 508: 'Quietude', 509: 'Azoth', 510: 'Omega', 511: 'Abismo',
    512: 'Rasgar Vida', 513: 'Rasgar Coração', 514: 'Círculo Cortante', 515: 'Círculo de Fúria',
    516: 'Troca de Lei', 517: 'Brilho Âmbar', 518: 'Alpha', 519: 'Descida', 520: 'Magi',
    521: 'Feitiço', 522: 'Sopro de Deus', 523: 'Veloc. da Luz', 524: 'Rio de Fogo',
    525: 'Uivo de Fúria', 526: 'Presença', 527: 'Logos', 528: 'Adrammelech', 529: 'Mateus',
    530: 'Ultima', 531: 'Exodus', 532: 'Famfrit', 533: 'Abater', 534: 'Espada Juiz', 535: 'Prender',
    536: 'Dom de JP', 537: 'Clipe Amarelo', 538: 'Espada Juiz', 539: 'Carta Amarela',
    540: 'Palaistra', 541: 'Carta Branca',
    542: 'Combo Azul', 543: 'Combo Vermelho', 544: 'Combo Caça', 545: 'Combo Cavaleiro',
    546: 'Combo Oração', 547: 'Combo Negro', 548: 'Combo Sábio', 549: 'Combo Sagrado',
    550: 'Combo Ladrão', 551: 'Combo Letal', 552: 'Combo Malabar', 553: 'Combo Armas',
    554: 'Combo Defesa', 555: 'Combo Invoc.', 556: 'Combo Branco', 557: 'Combo Espírito',
    558: 'Combo Combate', 559: 'Combo Atirador', 560: 'Combo Magia', 561: 'Combo Carga',
    562: 'Combo Luta', 563: 'Combo Animal', 564: 'Combo Tempo', 565: 'Combo Esgrima',
    566: 'Combo Morfo', 567: 'Combo Ninja', 568: 'Combo Gadget', 569: 'Combo Arco',
    570: 'Combo Espada', 571: 'Combo Fera', 572: 'Combo Monge', 573: 'Combo Dragão',
    574: 'Combo Ouro',
})
ABILITIES.update({
    686: 'Espada?', 687: 'Espada Afiada?', 688: 'Espada Torta?', 689: 'Espada Oxidada?',
    690: 'Espadão?', 691: 'Espada Pesada?', 692: 'Faca?', 693: 'Espada Fina?', 694: 'Lâmina?',
    695: 'Cajado Velho?', 696: 'Bastão?', 697: 'Clava Pesada?', 698: 'Arco?', 699: 'Arco Grande?',
    700: 'Lança?', 701: 'Instrumento?', 702: 'Luvas?', 703: 'Bijuteria?', 704: 'Arma Velha?',
    705: 'Escudo?', 706: 'Elmo Oxidado?', 707: 'Gorro Velho?', 708: 'Armadura?',
    709: 'Roupas?', 710: 'Manto?', 711: 'Botas?', 712: 'Manopla?', 713: 'Berloque?', 714: 'Bolsa?',
    715: 'Metal?',
})
ABILITY_MAX_PX = 90
EXTRA_MENU.update(ABILITIES)


def px_width(rom, text):
    """largura em pixels (tabela 0x4F885B; espaço do formato 80 estimado em 4px)"""
    return sum(4 if c == ' ' else rom[0x4F885B + code01(c)] for c in text)


from extra_translations import MENU2, NAMES2
EXTRA_MENU.update(MENU2)
CLASSES.update(NAMES2)


# ---------- IPS ----------
def write_ips(path, recs):
    recs = sorted(recs.items())
    merged = []
    for off, b in recs:
        if merged and merged[-1][0] + len(merged[-1][1]) == off:
            merged[-1] = (merged[-1][0], merged[-1][1] + b)
        else:
            merged.append((off, b))
    out = bytearray(b'PATCH')
    for off, b in merged:
        for i in range(0, len(b), 0xFFFF):
            ch = b[i:i + 0xFFFF]
            out += (off + i).to_bytes(3, 'big') + len(ch).to_bytes(2, 'big') + ch
    out += b'EOF'
    open(path, 'wb').write(out)
    return merged


# ---------- fonte ----------
def read_glyph(rom, g):
    a = FONT + g * 128
    px = [[0] * 16 for _ in range(16)]
    for t, (ox, oy) in enumerate([(0, 0), (0, 8), (8, 0), (8, 8)]):
        d = rom[a + t * 32:a + t * 32 + 32]
        for y in range(8):
            for x in range(8):
                px[oy + y][ox + x] = (d[y * 4 + x // 2] >> (4 * (x & 1))) & 15
    return px


def glyph_bytes(px):
    out = bytearray()
    for ox, oy in [(0, 0), (0, 8), (8, 0), (8, 8)]:
        for y in range(8):
            for x in range(0, 8, 2):
                out.append(px[oy + y][ox + x] | (px[oy + y][ox + x + 1] << 4))
    return bytes(out)


def tilde_glyph(rom, base_g, tilde_g=36):
    """linhas 0-5 do til de ñ (g36) + linhas 6-15 do corpo de base_g"""
    t, b = read_glyph(rom, tilde_g), read_glyph(rom, base_g)
    px = [list(t[y]) if y < 6 else list(b[y]) for y in range(16)]
    return px


def main():
    rom = bytearray(open(sys.argv[1], 'rb').read())
    outp = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'patches', 'FFTA_ptBR_slot_ingles.ips')
    assert bytes(rom[0xA0:0xB0]).startswith(b'FFTA_INTER'), 'ROM inesperada'
    assert rom[0xAC:0xB0] == b'AFXP', 'precisa ser a ROM europeia (AFXP)'
    recs = {}

    # 1) menus/status: pega do IPS italiano
    ref = parse(REF_IPS)
    blob_off, blob = next((o, b) for o, b in ref if o == 0xFE4000)
    # o IPS só traz os bytes que mudaram (o byte 0x08 do ponteiro não muda): remonta slot a slot
    bytemap = {}
    for o, b in ref:
        if o != 0xFE4000:
            for k, v in enumerate(b): bytemap[o + k] = v
    slots = sorted({(o - IT_MENU) // 4 for o in bytemap if IT_MENU <= o < IT_MENU + 4 * 800})
    strings = []
    for s in blob.split(b'\0')[:-1] if blob.endswith(b'\0') else blob.split(b'\0'):
        if s: strings.append(s + b'\0')
    assert len(strings) == len(slots), (len(strings), len(slots))
    # confere: os ponteiros do IPS (bytes presentes) têm que bater com o offset sequencial no blob
    pos = 0
    for idx, s in zip(slots, strings):
        want = 0x08FE4000 + pos
        for k in range(3):
            o = IT_MENU + 4 * idx + k
            if o in bytemap: assert bytemap[o] == (want >> (8 * k)) & 0xFF, (idx, hex(want))
        pos += len(s)
    ptrs = dict(zip(slots, strings))
    text = bytearray()
    cursor = TEXT_BASE

    def add_string(data):
        nonlocal cursor
        addr = cursor + len(text)
        text.extend(data)
        return 0x08000000 + addr

    n_menu = 0
    for idx, s in sorted(ptrs.items()):
        # ã/õ: o patch italiano usava os glifos â/ô como substitutos
        if s[0] == 1:                       # formato 01
            b = bytearray(s)
            for i in range(1, len(b) - 1):
                if b[i] == 0x1B and b[i + 1] == 0xD9: b[i] = 0x1C      # "ão" -> ã
                elif b[i] == 0x28: b[i] = 0x29                            # ô -> õ
            s = bytes(b)
        else:                               # formato 80 (xx = glifo)
            b = bytearray(s); i = 0
            while i < len(b) - 1:
                if b[i] == 0x80:
                    if b[i + 1] == 0x1A: b[i + 1] = 0x1B                  # ã
                    i += 2
                else: i += 2 if b[i] == 0x40 else 1
            s = bytes(b)
        recs[EN_MENU + 4 * idx] = struct.pack('<I', add_string(s))
        n_menu += 1

    for idx, name in EXTRA_MENU.items():
        if idx in ABILITIES and px_width(rom, name) > ABILITY_MAX_PX:
            print('AVISO habilidade %dpx: %d %s' % (px_width(rom, name), idx, name))
        if idx in SKILLSETS and px_width(rom, name) > SKILLSET_MAX_PX:
            print('AVISO largura %dpx > %d: %d %s' % (px_width(rom, name), SKILLSET_MAX_PX, idx, name))
        recs[EN_MENU + 4 * idx] = struct.pack('<I', add_string(enc(name, 2 if ' ' in name else 1)))
        n_menu += 1

    # 2) classes
    en_fmt = lambda i: rom[struct.unpack_from('<I', rom, EN_NAMES + 4 * i)[0] - 0x08000000]
    for idx, name in CLASSES.items():
        w = px_width(rom, name)
        if idx in WEAPONS and w > 88: print('AVISO arma %dpx: %d %s' % (w, idx, name))
        if idx in MONSTERS and w > 85: print('AVISO nome largo %dpx: %d %s' % (w, idx, name))
        fmt = 80 if (' ' in name or en_fmt(idx) == 0x80) else 1
        recs[EN_NAMES + 4 * idx] = struct.pack('<I', add_string(enc(name, fmt)))

    assert cursor + len(text) < 0xFFF000
    recs[cursor] = bytes(text)

    # 3) fonte: ã e õ reais
    for g, base in ((G_A_TILDE, G_A_TILDE), (G_O_TILDE, G_O_TILDE)):
        recs[FONT + g * 128] = glyph_bytes(tilde_glyph(rom, base))[:64]

    merged = write_ips(outp, recs)
    print('menu/status: %d strings | classes: %d | texto: %d bytes em 0x%X | %d registros IPS -> %s' %
          (n_menu, len(CLASSES), len(text), cursor, len(merged), outp))


if __name__ == '__main__':
    main()
