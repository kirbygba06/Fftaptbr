# -*- coding: utf-8 -*-
"""Descrições de itens (banco 0x534D9C): texto de sabor por índice + categoria/efeitos traduzidos por regra."""
import re

FLAVOR = [
 'Espada de uma mão de\nuso comum.', 'Espada lindamente\nincrustada de prata.', 'Espada feita para\nabater monstros.',
 'Espada pesada, preferida\npor gente bruta.', 'Espada tão afiada que\ncorta o próprio vento.', 'Espada manchada pelo\nsangue de muitos.',
 'Espada misteriosa. Dizem\n"restaurar poder perdido".', 'Espada sagrada, chamada\n"Guardiã da Vida".', 'Espada feita de rara e\ncobiçada mithril.',
 'Espada dada ao campeão\ndo torneio. Símbolo de honra.', 'Espada sob encomenda do\nlendário "Cavaleiro Cebola".', 'Espada enterrada por\nmedo do seu poder.',
 'Espada feita do gelo mais\nfrio. Gélida na mão.', 'Lâmina para abater inimigos\nque se aproximam.', 'Lâmina pintada de preto\npara uso à noite.',
 'Lâmina que, dizem, guarda\no poder do próprio sol.', 'Lâmina de raio que faz o\nar ao redor tremer.', 'Lâmina que, dizem, lambe\no ar como língua de fogo.',
 'Lâmina feita, dizem, no\nformato de uma ventania.', 'Lâmina de gelo que\nnunca derrete.', 'Lâmina que ajuda o fluxo\nde poder pelo corpo.',
 'Lâmina carmesim feita para\ngarantir vitória em batalha.', 'Lâmina lisa como a\npele de uma pérola.', 'Lâmina valiosa cravejada\nde belas gemas.',
 'Lâmina de pedra, de\ncalor suave.', 'Lâmina incrustada\nde materita.', 'Lâmina de mithril forjada\ne temperada com esmero.',
 'Lâmina feita de poder\nsombrio. Assustadora.', 'Lâmina de adamantita\ncom brilho verde profundo.', 'Lâmina direita amada\npelo herói Gaol.',
 'Lâmina esquerda amada\npelo herói Gaol.', 'Sabre usado por\nacólitos de magos azuis.', 'Sabre mais largo, com\nclara curva na lâmina.',
 'Sabre ultramarino imbuído\ndo poder do mar.', 'Sabre usado por um herói\nlendário contra uma fera.', 'Sabre pintado com\nrara cor azulada.',
 'Sabre feito de minério\nde mithril refinado.', 'Sabre com guarda-mão.\nUsado pela guarda do palácio.', 'Lâmina divina que não\nsuporta noviços.',
 'Espada simples e\nprática.', 'Lâmina negra que encarna\na devastação da guerra.', 'Espada usada por cavaleiros\nde um rei lendário.',
 'Espada feita para\nencerrar batalhas.', 'Espada digna de um\nnobre cavaleiro.', 'Espada sagrada. Orações\nestão gravadas na lâmina.',
 'Espada feita como prova\ndo poder de um líder.', 'Só os cavaleiros mais fiéis\nempunham esta espada.', 'Espada de cavaleiro de\nmithril, feita com esmero.',
 'Versão aprimorada da\nExcalibur. Muito afiada.', 'Espada de cavaleiro à\nRagnarok, mas melhor.', 'Esta espada lendária dormiu\npor anos. Agora vive...',
 'Espadão pesado, mas\nbem equilibrado.', 'Técnicas antigas foram\nusadas nesta espada.', 'Estilhaços de diamante\ndeixam a lâmina afiadíssima.',
 'Esta espada é reta e\npesada como barra de ferro.', 'Espada feita em honra\naos bravos guerreiros.', 'Espada poderosa com\nlâmina em forma de cruz.',
 'Só mestres espadachins\npodem empunhá-la.', 'Espada de nobres. Símbolo\nde coragem e bondade.', 'Esta espada foi presente\nde uma fada da neve.',
 'Espada afiada temperada\nsob a lua cheia.', 'Montante com o nome do\nmais forte dos heróis.', 'Montante pesado, feito\npara decepar membros.',
 'Espada do berserker,\nperigosa a todos ao redor.', 'Espada que, dizem, muda\no rumo da batalha.', 'Espada empunhada pelo\nprotetor da terra.',
 'Espada bem afiada, só\nde uns poucos escolhidos.', 'Espada que já foi do\ndeus de outra terra.', 'Esta espada é popular\npelo peso leve.',
 'Espada dos gigantes. Pesada\ndemais para uma mão.', 'Montante achado nas costas\nde uma besta de pedra.', 'Espada de dois gumes feita\ndurante um eclipse solar.',
 'Espada levemente luminosa\nfeita de uma estrela cadente.', 'Faca dobrável pequena\no bastante para a palma.', 'Faca com lâmina e cabo\nlindamente adornados.',
 'Faca de lâmina curva\npara máxima letalidade.', 'Faca de lâmina fina\ne ponta afiada.', 'Adaga impressionantemente\ngrande.',
 'Faca com cabo texturizado\ne fácil de segurar.', 'Faca curva como\num chifre de animal.', 'Faca temperada por\num famoso ferreiro.',
 'Faca com um dente para\nprender espadas.', 'Faca feita da rara\nliga de oricalco.', 'Faca larga, no\nformato de uma mão.',
 'Faca com lâmina de\nmithril reluzente.', 'Faca feita para espantar\ntonberries e afins.', 'Faca feita para\nataques rápidos e múltiplos.',
 'Espada fina feita para\nperfurar, não cortar.', 'Embora fina, esta espada\ncorta metal.', 'Espada de estocada com\nguarda-mão acima do cabo.',
 'Espada de lâmina carmesim\nbrilhante e flamejante.', 'Espada de estocada com\nlâmina ondulada.', 'Espada de estocada com\nbela guarda de renda.',
 'Espada feita para lembrar\num redemoinho.', 'Espada batizada com a\nalegria da vitória.', 'Esta espada já foi usada\npara caçar magos renegados.',
 'Espada feita para manter\na razão em batalha.', 'Espada com pomo\nem forma de Y.', 'Espada com uma lâmina\nextra no pomo.',
 'Espada que muda de cor\nquando balançada.', 'Espada de lâmina de\nmithril fina e temperada.', 'Florete reluzente. 26a peça\ndo ferreiro Pemier.',
 'Florete rubro que, dizem,\nprende um demônio nela.', 'Florete rubro capaz de\ncortar a mão do destino.', 'Chamada espada-vento\npelo golpe amplo.',
 'Esta espada ninja serve\npara muitos fins.', 'Orvalho sobe na lâmina\npara lavar o sangue.', 'Espada flamejante que\nguia o dono à batalha.',
 'Espada exímia que corta\num elmo de ferro.', 'Espada que, dizem, soa\nao ser embainhada.', 'Lâmina tosca, mas\nmortalmente afiada.',
 'Espada tão bela que\né pena usá-la.', 'Lâmina divina tirada da\ncauda de um dragão maligno.', 'Lâmina de guerra feita\nem terra estrangeira.',
 'Espada famosa pelo desenho\nde ondas na lâmina.', 'Espada gigante gravada com\npalavras de destruição.', 'Lâmina temperada de\nmithril muito polido.',
 'Masamune que não perde o\nfio nem após 100 anos.', 'Lâmina de origem ignorada\ncom sombra flamejante.', 'Espada afiadíssima\nfeita como uma flor.',
 'Cajado branco puro,\nabençoado por um arquimago.', 'Cajado enfeitiçado para\nproteger o dono.', 'Este cajado foi atingido\npelo raio de Ramuh.',
 'Cajado curativo.', 'Cajado de purificação.\nPurifica o dono.', 'Cajado que, dizem,\nespalha bênçãos dos deuses.',
 'Cajado talhado com\ndesenhos de serpentes.', 'Cajado adornado com\nsímbolos de água sagrada.', 'Cajado com uma poderosa\njoia de granada.',
 'Cajado de cor estranha que,\ndizem, energiza o portador.', 'Cajado de quem\nabandonou desejos baixos.', 'Cajado feito de mithril.',
 'Grande cajado revigorante\nde árvore do deserto.', 'Este cajado protege o\nsono dos bons.', 'Bastão usado como foco\nde poder mágico.',
 'Bastão que arde ao ser\nbalançado no ar.', 'Bastão que chama raios\ncom um grande rugido.', 'Bastão que congela o ar,\nchamando uma nevasca.',
 'Bastão feito de osso de\ndragão desenterrado.', 'Bastão que extrai a força\ninterior do portador.', 'Bastão feito de\nchama cristalizada.',
 'Bastão feito de\nraio imóvel.', 'Bastão feito de\nneve endurecida.', 'Bastão gravado com os\nsímbolos do zodíaco.',
 'Bastão das guardas\nfemininas da rainha.', 'Bastão com excelente\ngravação em mithril.', 'Bastão de aspecto letal\ncoberto de runas invertidas.',
 'Bastão que prova maestria\nnas artes mágicas.', 'Bastão com cabeça de\nmetal pesado para golpear.', 'Maça que sente o\nfluxo de energia.',
 'Maça dourada usada\ncomo objeto cerimonial.', 'Maça para quem tem\nsabedoria e habilidade.', 'Maça terminada em bola\ncom espetos de metal.',
 'Maça feita de mandrágora\nvenenosa.', 'Maça que dá...\ne tira a vida.', 'Maça feita do\nfogo de Ifrit.',
 'Maça com cabeça como\ncauda de escorpião.', 'Maça sagrada feita para\nafastar o mal.', 'Maça com cabeça\nrevestida de mithril.',
 'Maça eriçada de\nespinhos de cacto.', 'Maça de reis. Brilha até\nna escuridão mais profunda.', 'Arco longo simples,\nfácil de achar.',
 'Arco manchado de carvão\npara emboscadas.', 'Arco adornado com\nespinhos longos e cruéis.', 'Arco que atira projéteis\nparecidos com pregos.',
 'Arco com prata para\nmais poder e alcance.', 'Arco que, dizem, pertence\nà deusa da caça.', 'Canções foram cantadas\nsobre este arco.',
 'Um engenheiro projetou\neste arco potente.', 'Arco longo carmesim para\nderrotar monstros.', 'Arco de mithril\ncom corda de mithril.',
 'Arco adornado com\nsímbolos de estrela e lua.', 'Arco fétido feito de\ntentáculos de malboro.', 'Flechas deste arco voam\nretas em qualquer vento.',
 'Arco flexível preferido\npor arqueiros experientes.', 'Exige grande força\npara usar este arco.', 'Arco modificado para\natirar várias flechas rápido.',
 'Arco de caçador. Feito\npara golpes críticos.', 'Arco leve feito por\nfadas da floresta.', 'Arco sombrio. Suas flechas\nsão convites ao inferno.',
 'Arco abençoado pela\ndeusa da batalha.', 'Para amadores, é duro\ndemais até de puxar.', 'Arco laqueado preto, sinal\nde pacto demoníaco.',
 'Arco divino que adorna o\ntrono dos deuses.', 'Versão mais forte do\ncomum arco de mithril.', 'Dizem que este arco\nescolhe quem o empunha.',
 'Este arco gigante é forte,\nmas difícil de disparar.', 'Grande arco destrutivo\nque faz o chão tremer.', 'Lança com ponta pequena,\nmas afiada.',
 'Lança flamejante com ponta\nbrilhando como magma.', 'Lança como a de um herói\nmeio-fera de outrora.', 'O sopro de Shiva mantém\nesta lança de gelo afiada.',
 'Lança com cabeça aberta\ncomo penas de flecha.', 'Lança negra de um lendário\nlanceiro dragão.', 'Lança do deus do mar que\ninstila coragem em combate.',
 'Lança de metal fundido\ne escamas de dragão.', 'Lança que aproveita a\nleveza do mithril.', 'Símbolos estranhos cobrem\nesta lança dos deuses.',
 'Lança cravada nas costas\nde uma besta de pedra.', 'Lança preciosa das\ntribos bangaa.', 'Sino vermelho tocado à\nnoite para afastar demônios.',
 'Sino de vidro com\nbelo timbre.', 'Trombeta para tocar a\nmarcha para a batalha.', 'Flauta feita furando\numa concha torcida.',
 'Sino de barro feito de\nterra de muitas terras.', 'Flauta negra. Sua música\npode apaziguar espíritos.', 'Flauta em forma de um\namante de música meio-fera.',
 'Fadas passam as horas\ntocando estas harpas.', 'Muitos mestres já\ntocaram esta flauta.', 'O som claro deste sino\ncura a alma.',
 'Esta harpa drena a força\ndos homens com sua canção.', 'O mithril deste sino\ndá o seu som suave.', 'Instrumento outrora famoso,\nhoje esquecido.',
 'Estas castanholas soam\ncomo passos da morte.', 'Soqueira de metal\nfeita para combate.', 'O calor do sol imbui\nestas soqueiras flamejantes.',
 'Garras venenosas saem\ndestas soqueiras.', 'Poucos acordam do sono\nque estas soqueiras causam.', 'Soqueira letal como\nlança ou espada.',
 'Soqueira pequena com\ngarras afiadas.', 'Estas soqueiras poderosas\nsão leves e resistentes.', 'As "presas brancas" destas\nsoqueiras dão sorte.',
 'Soqueira conhecida como\n"Mãos do Criador".', 'Soqueira feita para lembrar\nas garras de uma fera.', 'Soqueira com sinistras\ngarras vermelhas.',
 'Soqueira com garras\nafiadas de mithril.', 'Tempestades podem começar\ncom um golpe destas.', 'Soqueira tão leve\nque se esquece dela.',
 'Alma marrom e turva.\nSolta por goblins.', 'Alma mole e borrachuda.\nSolta por flans.', 'Alma de fogo vacilante.\nSolta por bombas.',
 'Alma como olho de dragão.\nSolta por dragões.', 'Bela alma aquosa.\nSolta por lâmias.', 'Alma como casca de árvore.\nSolta por insetos.',
 'Alma vermelha vívida.\nSolta por panteras.', 'Alma verde pegajosa.\nSolta por malboros.', 'Alma de ahriman. Tão\nfunda que não tem fim.',
 'Mithril moldado\nmagicamente em alma.', 'Uma aura quente cerca\nesta alma benévola.', 'Esta alma uiva e rosna\ncomo se estivesse viva.',
 'Esta arma de fogo simples\né fácil de usar e limpar.', 'Esta arma usa balas\nespeciais arredondadas.', 'Esta arma tem cano longo\npara mais precisão.',
 'Este rifle longo derruba\num alvo em segundos.', 'Arma feita com técnicas\nantigas de engenheiros.', 'Arma lindamente trabalhada.\nObra de arte mortal.',
 'Arma de grosso calibre\ncom poder tremendo.', 'Esta famosa arma, dizem,\nsempre acerta o alvo.', 'Esta arma foi usada\nnum assassinato.',
 'Arma com cano de mithril.', 'Rifle pesado, mas potente.\nPreciso e fácil de mirar.', 'Arma perdida, usada para\ninvocar bestas fabulosas.',
 'Escudo simples de\ncobre trabalhado.', 'Ataques parecem escorregar\ndeste escudo redondo.', 'Escudo de opala com\nbrilho branco reluzente.',
 'Este escudo mágico emana\numa fina aura fria.', 'Símbolos mágicos de fogo\ncobrem este escudo.', 'Escudo sagrado usado contra\num terrível inimigo.',
 'Escudo de terra estrangeira.\nParte de um conjunto.', 'Escudo carregado pelos\ncavaleiros dos céus.', 'Escudo de mithril dedicado\naos quatro deuses shijin.',
 'Escudo emplumado de\ncouro de chocobo curtido.', 'Este escudo da sorte foi\npresente dos deuses.', 'Escudo que muda de cor\nconforme o ângulo.',
 'Elmo de cobre\ne couro.', 'Elmo de ferro pesado,\nmas muito resistente.', 'Elmo formal usado\nem cerimônias.',
 'Este elmo cobre\no rosto inteiro.', 'Este elmo é caro,\nmas muito confiável.', 'Elmo estrangeiro de\nacabamento primoroso.',
 'Elmo com grande pluma\ncarmesim. Usado em cerimônias.', 'Elmo assustador em\nforma de demônio.', 'Elmo forte e resistente\nusado por bangaa.',
 'Palavras de bênção enfeitam\neste adorno feminino vermelho.', 'Grampo feminino enfeitado\ncom pedras da sorte.', 'Esta fita feminina\nafasta todos os males.',
 'Gorro resistente com\numa pena longa.', 'Adorno feito para proteger\ncontra magias nocivas.', 'Este chapéu é dado a quem\ntem uma missão especial.',
 'Esta faixa serve para\nfocar o espírito.', 'Este chapéu pontudo é o\nclássico chapéu de mago.', 'Grampo com fino trabalho em\nouro. Feito por feiticeira.',
 'Chapéu que, dizem, era de\num famoso ladrão.', 'Chapéu preto pontudo\nde fio mágico.', 'Chapéu branco com orelhas\npeludas. De fio mágico.',
 'Estranho chapéu amarelo\nque cresce com o dono.', 'Tiara dourada dada à\nmais bela das mulheres.', 'Peitoral de fibras\nfirmemente trançadas.',
 'Armadura de placas de\ncobre entrelaçadas.', 'Armadura pesada com\naço no peito.', 'Armadura completa de placas\nde metal sobre cota de malha.',
 'Armadura cara folheada\na ouro.', 'Esta armadura é\ncravejada de diamantes.', 'Bela armadura de opala\ncom curvas requintadas.',
 'Armadura leve de ferro\nfundido com mithril.', 'Armadura mais leve imbuída\nde aura refletora mágica.', 'Armadura de metal\nfundido com escamas de dragão.',
 'Armadura única de\numa terra estrangeira.', 'Esta armadura traz o brasão\ndo "Último Cavaleiro".', 'Armadura de adamantita\nverde lindamente temperada.',
 'Armadura duríssima\nfeita de materita.', 'Armadura pesada, mas\nresistente. Para chocobo de guerra.', 'Roupa resistente de\ncouro em camadas.',
 'Camisa de anéis de\nferro ligados.', 'Camisa tecida de\nliga de adamantita.', 'Roupa leve de algodão\npara absorver impactos.',
 'Roupa feita para que as\ntiras de metal não rocem.', 'Roupa de luta preferida\npelos monges.', 'Corda trançada para\nprender roupas soltas.',
 'Estas roupas azuis foram\nabençoadas pela terra.', 'Roupa feminina usada pela\ndeusa da vitória.', 'Roupa ninja feita com\ntécnicas secretas especiais.',
 'Roupa preta usada em\noperações noturnas.', 'Roupa usada por um\nantigo rei herói.', 'Estas roupas brilham\nmisticamente na luz.',
 'Roupa feminina\nisolante.', 'Roupa feita de ossos\nde monstros conectados.', 'Túnica resistente. A única\nroupa de que você precisa.',
 'O mais novo do famoso\nestilista "Brint".', 'Última criação de Galmia.\nUsa luxuoso couro de chocobo.', 'Toda criança de Ivalice quer\num destes casacos de juiz.',
 'Uniforme de uma ordem de\ncavaleiros extinta.', 'Manto simples de\ncânhamo.', 'Manto macio feito da\nmelhor seda.',
 'Manto com capuz\npreferido por magos.', 'Manto da sorte tingido\ncom suco de visco.', 'Este manto não queimaria\nno meio de um incêndio.',
 'Este manto transforma raios\nem poder para o usuário.', 'Manto tecido com\numa nevasca.', 'Manto branco puro que\nprotege de magia negra.',
 'Manto cor de laca que\nfortalece a magia negra.', 'Este belo manto\nevita a exaustão.', 'Manto usado por todos\nos líderes de outrora.',
 'Este casaco tem um\nbrilho prateado místico.', 'Manto elegante feito\npara magos vermelhos.', 'Manto de pano macio dado\na sábios consumados.',
 'Manto cor do céu usado só\npelos honestos e humildes.', 'Manto tingido de preto\ncom sangue.', 'Botas de couro\nduro.',
 'Sapatos com pontas para\nsaltar melhor.', 'Sapatos velozes para\nmover-se mais rápido.', 'Sapatos vermelhos tingidos\ncom ervas medicinais.',
 'Botas de pena. O usuário\npode andar na água.', 'Botas resistentes para escalar.\nMelhoram muito os saltos.', 'Botas do popular estilista\n"Galmia Pepe".',
 'Botas emplumadas que\nvoam para qualquer lugar.', 'Botas usadas pelos guardas\nreais da era dos reis.', 'Botas de movimento rápido\nusadas por espiões.',
 'Luvas que vão do cotovelo\naté os dedos.', 'Braçadeiras que permitem\nmáximo movimento dos dedos.', 'Braceletes de couro que\nnão atrapalham as mãos.',
 'Estas braçadeiras coloridas\nsão lindamente adornadas.', 'Luvas à prova de fogo.\nBoas como pegadores.', 'Braçadeiras de osso de\nanimal para aparar ataques.',
 'Anel com uma pedra\nde poder.', 'Anel gravado com símbolos\nque aumentam a magia.', 'Anel de bênção que, dizem,\nfoi feito por anjos.',
 'Broche de escaravelho\nque brilha como arco-íris.', 'Brincos com rubis\nem forma de lágrima.', 'Bracelete usado por um\ngrande adivinho de outrora.',
 'Dizem as lendas que esta\né a alma de Mindu.', 'Poção mágica que\ncura carne ferida.', 'Poção feita em\nconcentração maior.',
 'A mais potente poção\ndisponível.', 'Este elixir restaura\npoder mágico perdido.', 'Este elixir fabuloso cura\ne restaura magia.',
 'Esta poção é antídoto\npara a maioria dos venenos.', 'Beba esta poção para\nenxergar no escuro.', 'Beba esta poção para\nquebrar o silêncio.',
 'Beba esta poção para\nvoltar à forma real.', 'Beba esta poção para\namolecer a pele de pedra.', 'Água benta devolve a\nverdadeira vida aos zumbis.',
 'Enfaixe membros feridos\npara recuperar movimento.', 'Elixir fabuloso que\ncura alterações de status.', 'Pena de cauda mágica\nque revive aliados caídos.',
]
assert len(FLAVOR) == 375, len(FLAVOR)
for _i, _t in {270: 'Elmo com grande pluma\ncarmesim. Cerimonial.', 290: 'Armadura completa de placas\nde metal sobre malha.',
               296: 'Armadura de metal fundido\ncom escamas de dragão.', 301: 'Armadura pesada e firme.\nPara chocobo de guerra.',
               319: 'Última criação de Galmia.\nCouro de chocobo luxuoso.', 322: 'Manto simples de cânhamo.', 338: 'Botas de couro duro.',
               343: 'Botas firmes para escalar.\nMelhoram muito os saltos.', 349: 'Braçadeiras de máxima\nmobilidade dos dedos.'}.items():
    FLAVOR[_i] = _t

ELEM = {'Fire': 'Fogo', 'Water': 'Água', 'Earth': 'Terra', 'Wind': 'Vento', 'Lightning': 'Trovão', 'Ice': 'Gelo', 'Dark': 'Trevas', 'Holy': 'Sagrado'}
STAT = {'Petrify': 'Pedra', 'Doom': 'Morte', 'Slow': 'Lentidão', 'Confusion': 'Confusão', 'Confuse': 'Confusão', 'Poison': 'Veneno', 'KO': 'KO',
        'Charm': 'Encanto', 'Blind': 'Cegueira', 'Silence': 'Silêncio', 'Berserk': 'Fúria', 'Sleep': 'Sono', 'Stop': 'Parar', 'Zombie': 'Zumbi',
        'Frog': 'Sapo', 'Immobilize': 'Imobilizar', 'Disable': 'Incapacitar'}
BASE = {'Sword': ('Espada', 'f'), 'Holy Sword': ('Espada Sagrada', 'f'), 'Blade': ('Lâmina', 'f'), 'Saber': ('Sabre', 'm'), 'Knightsword': ('Esp. Cav.', 'f'),
        'Greatsword': ('Espadão', 'm'), 'Broadsword': ('Montante', 'm'), 'Knife': ('Faca', 'f'), 'Rapier': ('Florete', 'm'), 'Katana': ('Katana', 'f'),
        'Staff': ('Cajado', 'm'), 'Rod': ('Bastão', 'm'), 'Mace': ('Maça', 'f'), 'Bow': ('Arco', 'm'), 'Greatbow': ('Arcão', 'm'), 'Spear': ('Lança', 'f'),
        'Instrument': ('Instr.', 'm'), 'Knuckles': ('Soqueira', 'f'), 'Soul': ('Alma', 'f'), 'Gun': ('Arma de Fogo', 'f'), 'Shield': ('Escudo', 'm'),
        'Helmet': ('Elmo', 'm'), 'Ribbon': ('Fita', 'f'), 'Hat': ('Chapéu', 'm'), 'Armor': ('Armadura', 'f'), 'Clothing': ('Roupa', 'f'), 'Robe': ('Manto', 'm'),
        'Shoes': ('Calçado', 'm'), 'Armlets': ('Braçadeira', 'f'), 'Accessory': ('Acessório', 'm'), 'Wind Sword': ('Espada do Vento', 'f')}
ADJ = {'Fire': ('de Fogo', 'de Fogo'), 'Water': ('de Água', 'de Água'), 'Earth': ('de Terra', 'de Terra'), 'Wind': ('de Vento', 'de Vento'),
       'Lightning': ('de Trovão', 'de Trovão'), 'Ice': ('de Gelo', 'de Gelo'), 'Dark': ('de Trevas', 'de Trevas'), 'Holy': ('Sagrado', 'Sagrada')}
FIXED = {'1-hand': '1 mão', '2-hand': '2 mãos', "Drains target's HP.": 'Drena HP do alvo.', 'Removes "doom" from target': 'Remove "morte" do alvo',
         "Heals target's HP": 'Cura HP do alvo', 'Absorbs HP from target': 'Absorve HP do alvo', 'Improves chance to steal': 'Aumenta chance de roubo',
         'Auto-Reflect': 'Auto-Refletir', 'Auto-Raise': 'Auto-Reviver', 'Teleportation': 'Teletransporte', 'Waterwalking': 'Andar na água',
         'Ignore elevation.': 'Ignora altura.', 'Cannot walk over water.': 'Não anda na água.', 'Walk to any height with': 'Anda em qualquer altura,',
         'ease, but not in water.': 'mas não na água.', '[null]All status ailments': '[null]Todas as alterações'}


def _cat(s):
    m = re.match(r'^(\w+) (.+)$', s)
    if s in BASE: return BASE[s][0]
    if m and m.group(1) in ADJ and m.group(2) in BASE:
        b, g = BASE[m.group(2)]; a = ADJ[m.group(1)]
        return b + ' ' + (a[0] if g == 'm' else a[1])
    return None


def _tr_line(l):
    l = l.strip()
    if l in FIXED: return FIXED[l]
    m = re.match(r'^(\d)-panel (range|pierce)$', l)
    if m: return ('Alcance %s casas' if m.group(2) == 'range' else 'Perfura %s casas') % m.group(1)
    m = re.match(r'^(\[\w+\])(.+)$', l)
    if m:
        toks = []
        for t in re.split(r'/| ', m.group(2)):
            toks.append(ELEM.get(t) or STAT.get(t) or t)
        return m.group(1) + '/'.join(toks)
    c = _cat(re.sub(r' \(weak:(\w+)\)$', '', l))
    if c:
        w = re.search(r'\(weak:(\w+)\)$', l)
        return (c.replace(' de ', ' ') if w else c) + (' (fraco:%s)' % ELEM.get(w.group(1), w.group(1)) if w else '')
    return None


def item_rule(idx, txt):
    pages = txt.split('\f')
    if not pages[0].count('\n') <= 1 or idx >= len(FLAVOR): return None
    out = [FLAVOR[idx]]
    for pg in pages[1:]:
        res = []
        for ln in pg.split('\n'):
            t = _tr_line(ln) if ln.strip() else ''
            if t is None and '/' in ln:
                ps = [_tr_line(x) for x in ln.split('/')]
                if all(x is not None for x in ps): t = '/'.join(ps)
            if t is None: return None
            res.append(t)
        out.append('\n'.join(res))
    r = '\f'.join(out)
    if idx == 360: r = r.replace('Cegueira', 'Cego').replace('Silêncio', 'Mudo')
    return r
