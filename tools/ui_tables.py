# -*- coding: utf-8 -*-
"""Tabelas de texto curto do slot inglês (mensagens de interface, nomes de clãs, títulos, manchetes, missões)."""

# 0x728F38: mensagens de interface
UI = {0: 'Sem símbolo', 1: 'Cercado por:', 2: 'Bar', 3: 'Loja', 4: 'Prisão', 5: 'Guarda-Cartas', 6: 'Banco de Monstros', 7: 'Caça ao Tesouro',
 8: 'Descartar item?', 9: '    Sim    Não', 10: 'Prêmio:', 12: 'Pts. Clã:', 13: 'pontos', 14: 'Nv. Hab.', 15: 'Clã subiu de nível!',
 16: 'Nv. Hab. subiu & Item!', 18: 'Candidato ao clã!', 19: 'Aceitar esta pessoa?', 20: 'Recusar esta pessoa?', 21: 'Remover esta pessoa?',
 23: 'áreas restantes.', 24: 'áreas restantes.', 25: 'Libertar', 26: 'Concluído!', 27: 'Livre!', 39: 'Sem informações.', 41: 'dominado',
 42: 'N/D', 43: 'Nível de hab. subiu!', 44: 'Itens demais.', 45: 'Escolha o item a descartar.', 47: ' trocado.', 48: ' recebido.',
 49: 'Equipar Itens', 50: 'Escolher Habil.', 51: 'Mudar Classe', 52: 'Sem Habilidades', 53: 'Sair do Clã', 54: ' foi tomada!', 55: 'h',
 57: 'Sem dados', 58: 'Retomar Batalha', 59: 'Carregar', 60: 'Escolha onde salvar.', 61: 'Escolha o que carregar.', 62: 'Salvando...',
 63: 'Carregando...', 64: 'Jogo salvo.', 65: 'Jogo carregado.', 66: 'Falha ao salvar!', 67: 'Falha ao carregar!', 68: 'Erro na memória de backup.',
 69: 'Todas as áreas livres!', 70: 'Retomar batalha salva.', 71: 'Sobrescrevendo este slot.', 72: 'Verificando dados.', 73: 'Missão Cumprida',
 74: 'Unidade enviada voltou.', 75: 'dominado', 76: 'Posicione o símbolo.', 77: 'Escolha um slot vazio.', 78: '......Buscando......',
 81: 'Achado', 83: 'está sob ataque!'}

# 0x728684: nomes de clãs/grupos
CLANS = {1: 'Patrulha da Guarda', 2: 'Bando de Cyril', 3: 'Cavaleiros Sprohm', 4: 'Clã Belmia', 5: 'Clã Banisa', 6: 'Bando Gaja', 7: 'Guardas',
 8: 'Clã Marble', 9: 'Feras Kudik', 10: 'Náiades Errantes', 11: 'Clã Clatz', 12: 'Clã Dip', 13: 'Bando Koring', 14: 'Clã Shalo', 15: 'Fantasmas Aisen',
 16: 'Dragões de Roda', 17: 'Formigas-Leão', 19: 'Espíritos Malandros', 20: 'Dragoons Brass', 21: 'Monstros Selvagens', 22: 'Bando Gertai',
 23: 'Bando Ramble', 24: 'Seita Zoara', 25: 'Monstros Perdidos', 26: 'Bandidos Tubola', 27: 'Clã Hounds', 28: 'Emissários Jagd', 29: 'Sanguinários',
 30: 'Facção Doned', 31: 'Procurado!', 32: 'Feras Fugitivas', 33: 'Clã Crow', 34: 'Dragões de Roda', 39: 'Equipe Mithril', 40: 'Redator Sprohm',
 41: 'Contrabandistas', 42: 'Resistência', 44: 'Morde-Arma', 45: 'Caçadores Ilegais', 46: 'Fada da Neve', 47: 'Weaver Louco', 48: 'Carteiro',
 49: 'Clã Baham', 122: 'Homens-Lagarto!?', 124: 'Rainha Remedi'}

# 0x729484: prefixos de título de clã
TITLES = {1: 'Perdedor ', 2: 'Trapaceiro ', 3: 'Barato ', 4: 'Facção Baham ', 5: 'Explorador ', 6: 'Mestre ', 7: 'Sem Igual ', 8: 'Super ', 9: 'Quebra-Risco ',
 10: 'Jamago ', 11: 'Meister ', 12: 'Mão Ágil ', 13: 'Olho Divino ', 14: 'Faro Fino ', 15: 'Negociador ', 16: 'Mata-Dragão ', 17: 'Aventureiro ',
 18: '1 em 10.000 ', 19: 'Perito ', 20: 'Mestre Guerra ', 21: 'Gamago ', 22: 'Mestre Ferreiro ', 23: 'Mão de Ouro ', 24: 'Olho Certeiro ', 25: 'Nariz de Palha ',
 26: 'Conselheiro ', 27: 'Mata-Urso ', 28: 'Viajante ', 29: '1 em 1.000 ', 30: 'Intermediário ', 31: 'Comandante ', 32: 'Ramago ', 33: 'Ferreiro ',
 34: 'Mão de Prata ', 35: 'Olho Limpo ', 36: 'Faro de Fungo ', 37: 'Sabe-Tudo ', 38: 'Pastor ', 39: 'Escudeiro ', 40: '1 em 100 ', 41: 'Iniciante ',
 42: 'Guerreiro ', 43: 'Amago ', 44: 'Artesão ', 45: 'Mão de Cobre ', 46: 'Olho Torto ', 47: 'Nariz de Junco ', 48: 'Contador ', 49: 'Caça-Ratos ',
 50: 'Sonhador ', 51: '1 em 10 '}

# 0x729C74: manchetes
NEWS = {8: 'Leis Injustas!', 9: 'Choque de Clãs', 10: 'Monstros Loucos', 12: 'Os Cristais', 13: 'Leis Rígidas', 14: 'Loja Secreta', 17: 'Os Jagds',
 18: 'Mercadorias', 19: 'Cartaz Procurado', 20: 'Novo Relógio', 21: 'Busca Séria', 23: 'Juízes Sozinhos', 24: 'Mateus', 25: 'Dia de Audiência',
 26: 'Preços Disparam', 27: 'Férias Reais', 28: 'Nova Aventura', 29: 'Clã Borzoi', 30: 'Segredo Sujo', 31: 'Ladrão Exposto', 32: 'Área Livre!',
 33: 'Nossos Heróis!', 34: 'Plano do Borzoi', 35: 'Fim do Borzoi', 36: 'Gukko Sumiu', 37: 'Navio Estrangeiro', 38: 'Quadrilha', 39: 'Os Asas Vermelhas',
 40: 'Monopólio!', 42: 'A Pedra-Espírito', 43: 'Os Sábios', 44: 'Paz, Enfim', 45: 'Fim de Grissom', 46: 'Menestrel Estranho', 47: 'Demônios de Fora',
 48: 'Heróis', 49: 'Volta de Gukko', 50: 'Viva!', 52: 'Os Libertadores', 53: 'Torneio', 54: 'Os Torneios', 55: 'Liga de Clãs', 56: 'Passagem Nevada',
 57: 'Caça Ilegal', 58: 'Ruínas Achadas', 59: 'Juízes Injustos?', 60: 'Cartões em Branco', 61: '! Habilidades', 62: '! Tipos de Habil.', 63: '! Mudar Classe',
 64: '! Classes Expert', 65: '! Metamorfose', 66: '! Condições', 67: '! Combos', 68: '! Isenção', 69: '! Os Totemas', 71: '! Leis', 72: '! Ranking de Leis',
 73: '! Prisão', 75: '! Cartas de Lei', 77: '! Negociações', 79: '! Caça ao Tesouro', 81: '! Pedidos', 83: '! Itens de Missão', 85: '! Nível do Clã',
 86: '! Níveis de Habil.', 87: '! Território', 89: '! Ligação', 91: '! Mercadorias'}

# 0x72C3F8: títulos de missão
MISSIONS = {1: 'Guerra de Neve', 2: 'Outro Mundo', 3: 'Colher Ervas', 4: 'Caça à Tese', 5: 'Os Guepardos', 6: 'Perigo no Deserto', 7: 'Fluxo Torcido', 8: 'Antileis',
 9: 'Chuva de Diamantes', 10: 'Despertar Quente', 11: 'Bosque Mágico', 12: 'Forte Esmeralda', 13: 'Pálida Cia.', 14: 'Caça em Jagd', 15: 'A Recompensa',
 16: 'Relógio Dourado', 17: 'Hora da Busca', 18: 'O Grande Achado', 19: 'Patrulha Deserto', 20: 'Areias Quietas', 21: 'Materita Já!', 22: 'Dia do Presente',
 23: 'Veio Escondido', 24: 'Ao Vale Âmbar', 25: 'Além da Colina', 26: 'Vale Real', 28: 'Procurado!', 29: 'Procurado!', 30: 'Procurado!', 31: 'Procurado!',
 32: 'Procurado!', 33: 'Procurado!', 34: 'Rubi Vermelho', 35: 'Ruínas da Torre', 36: 'Batalha em Aisen', 37: 'Dragão-Mago', 38: 'Forte Salika',
 39: 'Espadas Gêmeas', 40: 'Caça na Vila', 41: 'Fogo! Fogo!', 42: 'O Andarilho', 43: 'Torneio Batalha', 44: 'Torneio Magos', 45: 'Prova Natação', 46: 'Liga de Clãs',
 47: 'Neve em Lutia', 48: 'Mago Gélido', 49: 'Prof. em Apuros', 50: 'Receita Quente', 51: 'S.O.S.', 52: 'Anel Perdido', 53: 'Olhos Fixos', 54: 'Rosa do Deserto',
 55: 'Amigo em Apuros', 57: 'Por uma Canção', 58: 'Flores Brancas', 59: 'Nova Antilei', 60: 'Fuga da Prisão', 61: 'Ruínas Reais', 62: 'Ladrão de Esboços',
 63: 'Confronto!', 64: 'De Novo', 65: 'Sapos do Oásis', 66: 'Prof. Sumido', 67: 'Covil do Mal', 68: 'Exploração', 69: 'Ajuda do Dragão', 71: 'Miau Sumiu',
 72: 'Ladrão de Aves', 73: 'Libertem Sprohm!', 74: 'Juramento Raven', 75: 'Base Nubswood', 76: 'Limpa Lutia', 77: 'Queda do Borzoi', 78: 'Guarda de Cadoan',
 79: 'Libertem Cadoan!', 80: 'Selo do Fogo', 81: 'Libertem Baguba!', 82: 'Selo da Água', 83: 'Selo do Vento', 84: 'Selo da Terra', 85: 'Os Asas Vermelhas',
 86: 'Libertem Muscadet!', 87: 'Demônio Externo', 88: 'Demônio Externo', 89: 'Demônio Externo', 90: 'Última Defesa', 91: 'Libertem Bervenia!', 92: 'Dragão Mundial',
 93: 'Noiva Moogle', 94: 'Lei do Clã', 95: 'Desafiantes?', 96: 'Noiva Amaldiçoada', 97: 'Fuga de Flans!', 98: 'Sinto, Amigo', 99: 'Cenoura!', 100: 'Clã Sombra',
 101: 'A Lâmina Negra', 102: 'A Lâmina Heroica', 103: 'A Lâmina Fada', 104: 'Corrida Demônio', 105: 'Cerco aos Clãs', 106: 'Dragões Acordam', 107: 'Yellow Powerz',
 108: 'Blue Geniuses', 109: 'Brown Rabbits', 110: 'White Kupos', 111: 'Corrida Mithril', 112: 'Furo Roubado', 113: 'Fim Contrabando', 114: 'Resistência',
 116: 'Velhos Amigos', 117: 'Caçadores Ilegais', 118: 'Fada da Neve', 119: 'Vingança', 120: 'Recupere a Carta!', 121: 'Um Desafio', 123: 'Procura-se Humano',
 124: 'Procura-se Bangaa', 125: 'Procura-se Nu Mou', 126: 'Procura-se Viera', 127: 'Procura-se Moogle', 128: 'Observando Você', 129: 'Gil Dourado', 130: 'Duelo por Outro',
 131: 'Fantasma Gulug', 132: 'Cidade da Água', 133: 'Torre Miragem', 134: 'Terra Estéril', 135: 'Encontro Cadoan', 136: 'Encontro Sprohm', 137: 'Corrida Divertida',
 138: 'Fantasma Faminto', 139: 'Piratas à Vista', 141: 'Entrega de Vinho', 142: 'Música Quebrada', 143: 'Falcão Fugiu', 144: 'Passagem Perigosa', 145: 'Estrelas na Névoa',
 146: 'Liga Adaman', 147: 'Liga Mysidia', 148: 'Liga Crusita', 149: 'Bonecas sem Rosto', 150: 'Fada Fiel', 151: 'Pela Dama', 152: 'Sete Noites', 153: 'Negócios Suspeitos',
 154: 'Cores da Terra', 155: 'Herança Perdida', 156: 'Amor Jovem', 157: 'Fantasmas Guerra', 158: 'O Último Dia', 159: 'O Sino Toca', 160: 'Cidade Goblin',
 161: 'Livros Secretos', 162: 'Palavras de Amor', 163: 'Você, Imortal', 164: 'Torre Relógio', 165: 'Uma Educação', 166: 'Manhãs de Dor', 167: 'Pé no Chão', 168: 'Rumo a Meden',
 169: 'Vizinho!', 170: 'Honra Perdida', 171: 'Inspiração', 172: 'Folga do Coo', 173: 'A Luta', 174: 'O Mar Profundo', 175: 'Olho Digno', 176: 'Perdido na Névoa',
 177: 'Pestes!', 178: 'Medo de Palco', 179: 'Dilema do Diário', 181: 'Garoto Fugitivo', 182: 'Alquimista Louco', 183: 'Guarda Caravana', 184: 'Obra da Vida',
 185: 'Risadas Baratas', 186: 'Carinho', 187: 'Fonte Congelada', 188: 'Sem Perfume', 189: 'Sobre as Ondas', 190: 'Garoto Animado', 191: 'Medo de Pólvora', 192: 'O Raio Azul',
 193: 'Papo Doce', 194: 'Cicatriz', 195: 'Cidade Miragem', 196: 'Desejo Soldado', 197: 'Seca', 198: 'Feira de Trocas', 199: 'Pedido Adaman', 200: 'Magia Mysidia',
 201: 'Enigma', 202: 'Noite de Sorte', 203: 'Busca de Tutor', 204: 'Por Que Molhado?', 205: 'Corra Conosco', 206: 'Amuleto', 207: 'Menino Alquimista', 208: 'Sonhos Espinhosos',
 209: 'Libertem Cyril!', 210: 'Preciso de Navio', 211: 'Ceffyl da Mente', 212: 'Ceffyl do Corpo', 213: 'Pedra-Espírito', 214: 'Garota Apaixonada', 215: 'Ajuda Chocobo!',
 216: 'O Poste Celeste', 217: 'Estudo de Ruínas', 218: 'Cava, Cava', 219: 'Atrás de Prata', 220: 'Materita', 221: 'O Buraco', 222: 'Caça ao Metal', 223: 'Matemática Difícil',
 224: 'A Testemunha', 225: 'Vida ou Morte', 226: 'Dia do Karlos', 227: 'Ao Pai', 228: 'Ah, Milese', 229: 'Hora de Esfolar', 230: 'Rio Bravo', 231: 'Tecido Mágico',
 232: 'Guarda Algodão', 233: 'Ajude o Pai', 234: 'Borracha ou Real', 235: 'Rumo à Mata', 236: 'Dias de Charque', 237: 'Novos Campos', 238: 'Fogos Estranhos',
 239: 'Vida Melhor', 240: 'Caça ao Malboro', 241: 'Trabalho Chocobo', 242: 'Noite de Festa', 243: 'Sabor da Mamãe', 244: 'Labirinto do Poço', 245: 'Ela Se Foi',
 246: 'Velino Mágico', 247: 'Romance Alpino', 248: 'Calafrio', 249: 'Dor de Pão', 250: 'Livros Bagunça', 251: 'Mais Um Rabo', 252: 'Hora de Relaxar!', 253: 'Selva de Foma',
 254: 'Por uma Flor', 255: 'Planície Giza', 256: 'Passagem Lutia', 257: 'Nubswood', 258: 'Areias Eluut', 259: 'Rio Ulei', 260: 'Aisenfield', 261: 'Vulcão Roda',
 262: 'Ajuda Viagem', 263: 'Salikawood', 264: 'Caverna Nargai', 265: 'Picos Kudik', 266: 'Areias Jeraw', 267: 'Pântano Uladon', 268: 'Areias Gotor', 269: 'Dunas Delia',
 270: 'Caça-Insetos', 271: 'Caverna Tubola', 272: 'Planície Deti', 273: 'Garganta Siena', 274: 'Jagd Ahli', 275: 'Jagd Helje', 276: 'Jagd Dorsa', 277: 'Vale Âmbar',
 278: 'Ozmonfield', 279: 'Espadas em Cyril', 280: 'Salão Novatos', 281: 'Boneca Vodu', 282: 'Apareça', 283: 'Comida p/ Verdade', 284: 'Caverna Alba', 285: 'O Artista',
 286: 'Mais Uma Vez', 287: 'Árvore da Mola', 288: 'Quem Sou Eu?', 289: 'Boatos Ceifador', 290: 'Dias de Cão', 291: 'Pão Bom', 292: 'Preciso de Espada', 293: 'El Ritmo',
 294: 'Grande Passo', 295: 'Não Olhe!', 296: 'Dever Faxineiro', 297: 'Estrela Azarada', 298: 'Cuida do Curral', 299: 'Arma Fera', 301: 'Falsa Valiosa', 302: 'Guerra Weaver',
 303: 'Espada Lendária', 304: 'Reforma', 305: 'Segredo da Pedra', 306: 'Coisas de Espada', 307: 'Noite de Tempestade', 308: 'Canção Menestrel', 309: 'Louco por Armas',
 310: 'Chapéu Preto', 311: 'Chapéu p/ Garota', 313: 'Armadura Negra', 314: 'Mundo da Moda', 315: 'Alvoroço da Moda', 316: 'Primeira Missão', 318: 'Sou o Ezel!', 319: 'MonIrmão',
 320: 'Recompensa', 321: 'Llednar', 325: 'Recado do Cid', 326: 'Lago Brilhante', 327: 'Lago Brilhante', 328: 'Receita Molho', 329: 'Receita Molho', 330: 'Herói de Outrora',
 331: 'Herói de Outrora', 332: 'Minha Missão', 333: 'Minha Missão', 334: 'Minha Missão', 335: 'Sonho de Jade', 336: 'Ajude Nubs!', 337: 'Ajude Giza!', 338: 'Ajude Kudik!',
 339: 'Ajude Uladon!', 340: 'Ajude Jeraw!', 341: 'Ajude Lutia!', 342: 'Ajude Koring!', 343: 'Ajude Ulei!', 344: 'Ajude Aisen!', 345: 'Ajude Roda!', 346: 'Ajude Eluut!',
 347: 'Ajude Nargai!', 348: 'Ajude Salika!', 349: 'Ajude Delia!', 350: 'Ajude Gotor!', 351: 'Ajude Ozmon!', 352: 'Ajude Deti!', 353: 'Ajude Siena!', 354: 'Ajude Mwood',
 355: 'Ajude Tubola!', 356: 'Ajude Dorsa!', 357: 'Ajude Helje!', 358: 'Ajude Ahli!', 359: 'Encontro', 360: 'Ajuda Humano?', 361: 'Ajuda Bangaa?', 362: 'Ajuda Nu Mou?',
 363: 'Ajuda Viera?', 364: 'Ajuda Moogle?', 365: 'Pam Le Fay', 366: 'Andarilho Sombrio', 367: 'Demônio Redux', 368: 'Caça Novatos', 369: 'Caça de Verdade', 370: 'Caça Expert',
 371: 'Carta do Ezel', 372: 'Carta da Ritz', 373: 'Carta do Cid', 377: 'Reconciliação', 378: 'Deixado p/ Trás', 379: 'Com Babus', 380: 'Neve Mortal', 381: 'Grito da Donzela',
 382: 'Hora da Limpeza', 383: 'Memórias', 384: 'Tédio!', 385: 'Doned Aqui!', 386: 'Oferta da Ritz', 387: 'Missão do Cid', 388: 'Regra Sem Armas', 389: 'Regra do Beijo',
 390: 'Passe Imunidade', 391: 'Sem HP Cheio', 392: 'Sem Letramento', 393: 'Favoritismo', 394: 'Sem Respostas', 395: 'Sem Pular', 396: 'Hora da Decisão'}

# 0x725C40: nomes (apenas papéis/objetos; nomes próprios ficam)
NAMES = {23: 'Juiz', 55: 'Cavaleiro Negro', 59: 'Caixa Misteriosa', 60: 'Estátua Estranha', 61: 'Aparelho Mágico', 73: 'Dragões de Delia', 78: 'Rainha Lamia',
 69: 'Lorde Fantasma', 82: 'Lorde do Medo', 84: 'Arqui-Demônio', 85: 'Mamaflan', 79: 'Adamantoise'}

# menu (0x720D44) restantes
MENU = {65: '/usado', 91: 'Jagd', 720: 'AP Fim', 721: 'Item Fim', 724: 'HP MAX', 725: 'MP MAX', 749: 'EXP?', 146: 'Téc. Gladiador', 178: 'Dano {81 03} MP', 207: '100{81 07} Lã', 498: 'NV? S-Flare', 499: 'NV3 Sem Def', 500: 'NV5 Morte', 501: 'NV? Sagrado'}

# 0x724C34 (tabela de nomes): leis, categorias de arma, status, locais, luas
LAWS = {655: 'Em Grupo', 656: 'HP Cheio', 658: 'Imitador', 659: 'Luta', 660: 'Alvo: Área', 661: 'Alvo: Todos', 662: 'Espadas', 663: 'Lâminas',
 664: 'Sabres', 665: 'Esp. Cavaleiro', 666: 'Espadões', 667: 'Montantes', 668: 'Facas', 669: 'Floretes', 670: 'Katanas', 671: 'Lanças', 672: 'Instrumentos',
 673: 'Soqueiras', 674: 'Alma', 675: 'Projéteis', 676: 'Trevas', 677: 'Cajados', 678: 'Bastões', 679: 'Maças', 680: 'Mãos Nuas',
 681: 'Dano {81 03} 100', 682: 'Cura {81 02} 50', 683: 'Cura {81 02} 100', 684: 'Cura {81 03} 50', 685: 'Cura {81 03} 100', 686: 'Cura',
 687: 'Pedra', 688: 'Sapo', 689: 'Veneno', 690: 'Confusão', 691: 'Fúria', 692: 'Silêncio', 693: 'Encanto', 694: 'Prender', 695: 'Atordoar', 696: 'Lentidão',
 697: 'Parar', 699: 'Barreira', 700: 'Proteger', 701: 'Acelerar', 702: 'Dano2: Humano', 703: 'Dano2: Bangaa', 704: 'Dano2: Nu Mou', 705: 'Dano2: Viera',
 706: 'Dano2: Moogle', 707: 'Dano2: Animal', 708: 'Cartas de Lei', 709: 'Só Mag. Cura', 710: '(não usado)', 711: 'Antilei R1', 712: 'Antilei R2',
 713: 'Antilei R3', 714: 'Antilei R4', 715: 'Antilei R5', 716: 'Antilei R6', 717: 'Onipotente', 718: 'Palácio Bervenia', 723: 'Porto Baguba',
 725: 'Planície Giza', 726: 'Picos Kudik', 727: 'Pântano Uladon', 728: 'Areias Jeraw', 729: 'Passagem Lutia', 731: 'Rio Ulei', 733: 'Vulcão Roda',
 734: 'Areias Eluut', 735: 'Caverna Nargai', 737: 'Dunas Delia', 738: 'Areias Gotor', 740: 'Planície Deti', 741: 'Garganta Siena', 743: 'Caverna Tubola',
 747: 'Vale Âmbar', 748: 'Lua do Rei', 749: 'Lua Louca', 750: 'Lua do Sábio', 751: 'Lua do Caçador', 752: 'Lua do Bardo', 596: 'Ache Aliados 2'}

TABLES = [(0x728F38, UI), (0x728684, CLANS), (0x729484, TITLES), (0x729C74, NEWS), (0x72C3F8, MISSIONS), (0x725C40, NAMES), (0x720D44, MENU), (0x724C34, LAWS)]


UI.update({45: 'Descarte um item.', 71: 'Sobrescrever slot.'})
CLANS.update({10: 'Náiades', 19: 'Espíritos', 41: 'Muambeiros', 45: 'Caça Ilegal', 122: 'Lagartos!?'})
NEWS.update({26: 'Preços Sobem', 46: 'Menestrel', 59: 'Juiz Injusto?', 60: 'Cartas Brancas', 64: '! Classes Exp.', 79: '! Caça Tesouro'})
MISSIONS.update({10: 'Despertar', 39: 'Espadas Gêm.', 49: 'Prof. Apuros', 55: 'Amigo Apuros', 57: 'Uma Canção', 74: 'Voto de Raven', 85: 'Asas Verm.',
 86: 'Livre Muscad.', 96: 'Noiva Maldita', 113: 'Fim Contrab.', 117: 'Caça Ilegal', 120: 'Ache a Carta!', 128: 'Vigiando Você', 130: 'Duelo Sub.',
 135: 'Reun. Cadoan', 136: 'Reun. Sprohm', 137: 'Corrida Leve', 142: 'Música Falha', 145: 'Estrelas Névoa', 149: 'Bonecas Mudas', 153: 'Trato Suspeito',
 155: 'Herança Perd.', 161: 'Livros Secr.', 176: 'Perdido Névoa', 183: 'Escolta', 185: 'Risos Baratos', 187: 'Fonte Gelada', 204: 'Molhado?',
 208: 'Sonhos Espin.', 214: 'Garota Amada', 223: 'Mat. Difícil', 234: 'Borracha/Real', 238: 'Fogo Estranho', 240: 'Caça Malboro', 241: 'Lida Chocobo',
 279: 'Esgrima Cyril', 283: 'Prova Comida', 289: 'Boato Ceifador', 296: 'Zelador', 297: 'Má Estrela', 303: 'Espada Lenda', 307: 'Noite Tormenta',
 308: 'Canção Bardo', 309: 'Louco p/ Armas', 311: 'Chapéu Garota', 313: 'Armad. Negra', 366: 'Errante Negro'})
MISSIONS.update({309: 'Louco Armas', 378: 'Deixado Atrás', 388: 'Sem Armas', 390: 'Imunidade', 392: 'Sem Leitura'})
NAMES.update({55: 'Cav. Negro', 59: 'Caixa Mist.', 61: 'Máq. Mágica'})
LAWS.update({698: 'Estado', 718: 'Pal. Bervenia', 719: 'Cyril', 724: 'Bosque Nubs', 730: 'Bosque Koring', 732: 'Campo Aisen', 736: 'Bosque Salika',
             739: 'Campo Ozmon', 742: 'Bosque Materi'})
MISSIONS.update({56: 'Carne & Osso', 140: 'Protesto', 180: 'Cem Olhos', 300: 'Lâmina & Casco', 312: 'Armad. & Casco',
                 317: 'Preocupação', 322: 'No Palácio', 323: 'Cadê o Mewt?', 324: 'Encontro Doned'})
CLANS.update({35: 'Força Amarela', 36: 'Gênios Azuis', 37: 'Coelhos Pardos', 38: 'Kupos Brancos'})
MISSIONS.update({107: 'Força Amarela', 108: 'Gênios Azuis', 109: 'Coelhos Pardos', 110: 'Kupos Brancos', 260: 'Campo Aisen', 278: 'Campo Ozmon'})
NEWS.update({7: 'Leis: História'})
MENU.update({16: 'Clã'})
# tabelas de 5 ponteiros (inglês, francês, alemão, italiano, espanhol) usadas direto pelo código; só a entrada 0 (inglês) muda
CODE5 = {0x39526C: 'Clã suspenso:', 0x3952B4: 'dias', 0x395330: 'Batalha(s)', 0x395378: 'Taxa', 0x3953C8: 'Nível', 0x395420: 'Cartas',
         0x395470: 'Nível'}
TABLES = [(0x728F38, UI), (0x728684, CLANS), (0x729484, TITLES), (0x729C74, NEWS), (0x72C3F8, MISSIONS), (0x725C40, NAMES), (0x720D44, MENU),
          (0x724C34, LAWS)] + [(a, {0: t}) for a, t in CODE5.items()]

import re as _re
_STEPS = [(r'^(O|A|Os|As) ', ''), (r' (de|da|do|dos|das) ', ' '), (r'^Libertem ', 'Livre '), (r'^Ajude ', 'Ajuda '), (r'^Procura-se ', 'Busca '),
          (r'Caverna ', 'Cav. '), (r'Planícies? ', 'Pl. '), (r'Passagem ', 'Pass. '), (r'Garganta ', 'Garg. '), (r'Vulcão ', 'Vulc. '), (r'Pântano ', 'Pânt. '),
          (r'Torneio ', 'Torn. '), (r'Demônio', 'Dem.'), (r'Estrangeiro', 'Estr.'), (r'Habilidades', 'Habil.'), (r'Missão', 'Miss.'), (r'Batalha', 'Bat.'),
          (r'Procurado', 'Procur.'), (r'Fantasma', 'Fant.'), (r'Dragões', 'Drag.'), (r'Espíritos', 'Espír.'), (r'Cavaleiros', 'Cav.'), (r'Monstros', 'Mon.'),
          (r'Estátua', 'Est.'), (r'Aparelho', 'Aparel.'), (r'Mestre', 'Mest.'), (r'Ferreiro', 'Ferr.'), (r'Nariz', 'Nar.'), (r'Guerra', 'Guer.'),
          (r'Ruínas', 'Ruín.'), (r'Perigo', 'Perig.'), (r'Deserto', 'Des.'), (r'Diamantes', 'Diam.'), (r'Esmeralda', 'Esm.'), (r'Fogo! Fogo!', 'Fogo!'),
          (r'Receita', 'Rec.'), (r'Alquimista', 'Alq.'), (r'Libertem', 'Livre')]


def shorten(text, limit, pw):
    t = text
    for pat, rep in _STEPS:
        if pw(t) <= limit: break
        t = _re.sub(pat, rep, t)
    return t
