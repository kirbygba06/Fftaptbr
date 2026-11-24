# -*- coding: utf-8 -*-
"""Itens lendários/materiais (banco 0x54BB58): sabor por índice; rótulos de atributo e efeitos por regra."""
import re

F2 = [
 'Troféu tradicional de torneio\nde magos. Marca de poder.', 'Troféu honroso de torneio de\ncombate. Marca de força.', 'Troféu esportivo. Marca\nde bom trabalho em equipe.',
 'Taça com runas dada\nao deus Elda.', 'Prova da derrota do\nDragão do Mundo, Ogma.', 'Belo recipiente de\nouro puro. Muito valioso.',
 'Medalha que muda de cor\nquando se usa magia.', 'Medalha gasta recuperada\nde uma ruína antiga.', 'Medalha dada pelo povo\nà guarda costeira.',
 'Medalha de honra da guarda\nda cidade. Verdade e bravura.', 'O brilho deste broche não\nse apaga. Marca de amizade.', 'Só os justos de\ncoração ganham a medalha.',
 'Distintivo de participação.\nÓtima lembrança.', 'Joia de sete cores achada\nno fim do arco-íris.', 'Joia em forma de 3 cobras.\nAfasta o mal.',
 'Lágrima chorada por um gato\npreto. Brilha à noite.', 'Joia vermelha chamada\n"Deusa da Guerra Rouge".', 'Há raios dentro\ndesta gema.',
 'Ventos rodopiantes são\nvistos dentro desta gema.', 'Só se conhecem\ntrês destas gemas.', 'Joia de alquimistas que\ndá a visão de um ahriman.',
 'Rubi que, dizem, é o olho\ndo Rei Dragão.', 'Bracelete da Shara.\nMarca do Clã Ritz.', 'Pedra de minério que, dizem,\nrepresenta os 12 signos.',
 'Minério mágico. Venenoso se\nmal processado.', 'Minério de Materiwood.\nBom para fazer ferramentas.', 'Minério de alquimistas.\nMuda de dureza com o tempo.',
 'Minério verde-esmeralda\nde adamantoise.', 'Pedra sagrada em\nforma de alma.', 'Âmbar especial. Chamado\n"Sol de Ivalice".',
 'Liga de adamantita. Usada\npara armaduras e armas.', 'Poucos sabem trabalhar esta\nliga mágica da era Mysidia.', 'Fadas fazem esta liga\npara os de coração puro.',
 'Pedra usada em alquimia.\nFeita de uma alma viva.', 'Fio imbuído de magia negra\npara aumentar o poder.', 'Fio imbuído de magia branca\npara aumentar a resistência.',
 'Obter couro de chocobo\nnão é tarefa simples.', 'Tecido de algodão mágico\npara aumentar o poder.', 'Algodão mágico colhido\nda planta valda.',
 'Só os mortos usam este\nxale de sangue demoníaco.', 'Asa de ahriman. Ingrediente\nalquímico valioso.', 'Asa de fada. Derrete\nna água.',
 'Casca de uma Bomba que\nexplodiu. Quente ao toque.', 'Pele de pantera. Rígida\ne resistente.', 'Pele de tigre kudik. Popular\npela textura macia.',
 'Carneiro defumado. Boa\nração para viagem.', 'Vegetal famoso como o\nfavorito dos chocobos.', 'Ovo enorme. Rico em\nproteína e colesterol.',
 'Fungo de esporos dourados.\nCresce a cada 10 anos.', 'Água purificada para rituais\ne têmpera de armas.', 'Molho picante que\nlimpa mesmo a cabeça.',
 'Sorvete de mel. Uma\niguaria famosa em Cyril.', 'Doce em forma\nde chocobo.', 'Gratin de cheiro gostoso que\nnem chocobos resistem.',
 'Pão pequeno, de uma\nmordida. Difícil comer um só.', 'Pão macio comido\nem todo Ivalice.', 'Vinho com aparas de malboro.\nMuito forte.',
 'Sopa quente da Ilha de Ged,\nfeita de Bombas e ovos.', 'Escritos não traduzidos\nnuma escrita antiga.', 'Velino místico. Escreva\ncom o dedo.',
 'Distintivo da justiça. Todos\nos juízes usam um.', 'Distintivo de amizade. Todos\nos líderes de clã usam um.', 'Rascunho do novo romance\nde Runba, o Aventureiro.',
 'História do herói Gaol e da\ncorajosa Lini em 4 capítulos.', 'Só existem 4 cópias destas\nescrituras edaroyanas.', 'Anotações de lição de casa.\nMais preciosas que a vida.',
 '500 volumes com todo o\nconhecimento do mundo.', 'Dicionário pesado. Usado\ncomo arma por eruditos.', 'Guia prático de\nmonstros, com figuras.',
 'Livro-caixa secreto, não\nlido até agora.', 'Os desenhos deste livro\nganham vida e lutam!', 'Fragmento das memórias que\nMewt deixou.\fAchado num urso de\npelúcia da mãe do Mewt.',
 'Rabo da sorte de um\nrato do deserto.', 'Rabo do coelho de orelhas\ncompridas. Item da sorte.', 'Madeira de Danbukwood.\nPara armas e armaduras.',
 'A madeira macia da lua é\nfácil de esculpir.', 'Variwood e stradiwood\nfazem ótimos instrumentos.', 'Este pilar da torre do relógio\nfoi atingido por um raio.',
 'Suposta caneta-tinteiro\nde alta qualidade.', 'Tampões de ouvido favoritos\ndo merceeiro Mulchin.', 'Cristal do vidente\nTalkof.',
 'Estátua em ruínas do deus\nguardião das Minas Meden.', 'Broche de membro da\nRede Vizinho.', 'Harpa da Leanan. Faria um\nmonstro feroz dormir.',
 'Espada enferrujada e inútil.', 'Esta espada foi tão batida\nque é irreconhecível.', 'Espada de lâmina torta.\nInútil assim.',
 'Lança enferrujada. Inútil\na menos que consertada.', 'Um espírito de fogo\ncristalizado magicamente.', 'Um espírito de água\ncristalizado magicamente.',
 'Um espírito de vento\ncristalizado magicamente.', 'Um espírito de terra\ncristalizado magicamente.', 'O mundo se revela\nnas profundezas deste cristal.',
 'Este cristal de poder\nrealiza todos os desejos.', 'Distintivo de pena de\nchocobo branco.', 'Brasão em forma de\npluma branca.',
 'Estes óculos facilitam\nachar aliados.', 'Estes óculos facilitam achar\naliados mais fortes.', 'Quem olha esta caixa\nfica mudo para sempre.',
 'Dados viciados. Lembre:\nnão é legal trapacear.', 'Escudo de rituais.\nEm forma de olho de cobra.', 'Fio mágico. Pode parar\no tempo para o portador.',
 'Picareta de mithril\nlindamente trabalhada.', 'Fragrância leve feita numa\nterra a sudoeste.', 'Fragrância popular entre\nas mulheres de Cyril.',
 'Lampião de tonberry. Brilha\nde forma sinistra no escuro.', 'Ler estas escrituras\nfoca mente e espírito.', 'Item essencial para fazer\nbelos arranjos de flores.',
 'Osso de dragão. Pesado\ndemais para carregar fácil.', 'Osso de animal ignorado.\nUsado em magia.', 'De quem é este crânio que\nbate os dentes à noite?',
 'Esta chave de osso é\nestranhamente quente.', 'Peça essencial de um\ngrande relógio.', 'Peça de arma de liga adaman\nque absorve o coice.',
 'Dispositivo para apagar\nchamas.', 'Flor branca usada para fazer\npanaceia. Dura pouco.', 'Flor frágil usada para fazer\npanaceia. Murcha fácil.',
 'Bela flor que desabrocha\nnuma caverna escura.', 'Flor do deserto de\ncheiro calmante.', 'Flores plantadas para\naliviar a tristeza de uma irmã.',
 'Fruta vermelha viva. Dizem\nque cresce no Paraíso.', 'Fruta que aumenta magia.\nAmarga demais.', 'Fruta que aumenta força.\nDoce demais.',
 'Fruta de picância forte.\nRealmente acorda.', 'Gil roubado. Achado\nescondido na comporta.', 'Este dinheiro da Era dos Reis\ntem valor artístico.',
 'Moedas de ouro da Era dos\nReis. Enfeitavam placa de bar.',
]
assert len(F2) == 127, len(F2)

EFF = {
 'Enhances the power of lightning.': 'Aumenta o poder\nde trovão.', 'Enhances the power of wind.': 'Aumenta o poder\nde vento.',
 'Enhances the power of the dark.': 'Aumenta o poder\ndas trevas.', 'Enhances the power of fire.': 'Aumenta o poder\nde fogo.',
 'Enhances the power of earth.': 'Aumenta o poder\nde terra.', 'Enhances the power of ice.': 'Aumenta o poder\nde gelo.',
 'Enhances holy power.': 'Aumenta o poder sagrado.', 'Enhances dark power.': 'Aumenta o poder sombrio.',
 'Enhances dark and holy power.': 'Aumenta poder sombrio\ne sagrado.', 'Enhances the power of wind and water.': 'Aumenta o poder de\nvento e água.',
 'Enhances the power of water and ice.': 'Aumenta o poder de\nágua e gelo.', 'Increases AP received.': 'Aumenta o AP recebido.', 'Doubles AP received.': 'Dobra o AP recebido.',
}
LAB2 = [('Weapon Atk{40 3e 03}:', 'Atq. Arma{40 3e 03}:'), ('Magic{40 3e 0f}Pow:', 'Mág.{40 3e 0f}Pod:'), ('Weapon Atk', 'Atq. Arma')]


def items2(get_markup, px):
    out = {}
    for idx in range(len(F2)):
        t = get_markup(idx)
        pages = t.split('\f')
        si = next((i for i, p in enumerate(pages) if 'Weapon Atk' in p), None)
        if si is None: continue
        stat = pages[si]
        def a1(mo): return 'Atq. Arma{40 3e %02x}:' % max(0, int(mo.group(1), 16) + px('Weapon Atk') - px('Atq. Arma'))
        def a2(mo): return 'Mág.{40 3e %02x}Pod:' % max(0, int(mo.group(1), 16) + px('Magic') - px('Mág.'))
        stat = re.sub(r'Weapon Atk\{40 3e ([0-9a-f]{2})\}:', a1, stat)
        stat = re.sub(r'Magic\{40 3e ([0-9a-f]{2})\}Pow:', a2, stat)
        stat = stat.replace('Weapon Atk', 'Atq. Arma')
        eff = []
        for p in pages[si + 1:]:
            key = ' '.join(p.split('\n')).replace('  ', ' ').strip()
            eff.append(EFF.get(key, p))
        out[idx] = '\f'.join([F2[idx]] + [stat] + eff)
    return out
