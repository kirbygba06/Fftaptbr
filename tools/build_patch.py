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
         'Á': 0x04, 'É': 0x08, 'Í': 0x0C, 'Ó': 0x11, 'Ú': 0x15}
PUNCT01 = {'.': 0xE5, ',': 0xED, '!': 0xEC, '?': 0xEB, ':': 0xEF, '/': 0xF2, "'": 0xF5}


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

# habilidades individuais (idx 140-199; 146 e 178 têm códigos de controle e ficam em inglês)
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
ABILITY_MAX_PX = 90
EXTRA_MENU.update(ABILITIES)


def px_width(rom, text):
    """largura em pixels (tabela 0x4F885B; espaço do formato 80 estimado em 4px)"""
    return sum(4 if c == ' ' else rom[0x4F885B + code01(c)] for c in text)


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
