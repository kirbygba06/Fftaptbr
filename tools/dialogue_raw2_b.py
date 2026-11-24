# -*- coding: utf-8 -*-
"""Mais entradas com códigos de controle: opções, combos, locais e notícias."""
RAW2 = {
 0x54B7C8: {
  0: 'Escolha uma de três\nconfigurações de cor.', 1: 'Escolha o movimento do\ncursor na batalha.', 3: 'Escolha um de dois tipos\nde mensagem de evento.',
  4: 'Liga/desliga nomes de\nataque na batalha.', 6: 'Liga/desliga mensagens de\npontos de juiz na batalha.', 7: 'Mostrar itens não\nequipáveis ao equipar.',
  8: 'Atribui o comando principal\nda batalha ao botão L.',
 },
 0x534264: {
  1: 'Combo fácil de encadear\npara magos vermelhos.', 9: 'Combo infalível\npara assassinos.', 10: 'Combo fácil de encadear\npara malabaristas.',
  12: 'Combo fácil de encadear\npara defensores.', 19: 'Combo fácil de encadear\npara cavaleiros mog.', 20: 'Combo fácil de encadear\npara lutadores.',
  29: 'Combo infalível\npara domadores.', 30: 'Combo muito fácil de\nencadear p/ monges.',
 },
 0x53356C: {
  0: 'Capital de Ivalice. O\npalácio fica no centro.', 1: 'Cidade movimentada. Banco\nde monstros nos arredores.', 2: 'Cidade montanhosa bangaa.\nAbriga a prisão.',
  3: 'Cidade viera escondida\nno fundo da mata.', 4: 'Cidade nu mou. Sede do\nsaber e da alquimia.', 6: 'Floresta escura e profunda.\nEsconderijo de ladrões.',
  7: 'Planícies verdes ondulam.\nMuscmaloi cresce aqui.', 8: 'Picos imponentes. Lar de\num tigre ameaçado.', 9: 'Pântano fundo e perigoso\ncheio de ilhas.',
  10: 'Areias quentes sopram no\nmaior deserto de Ivalice.', 14: 'Planícies onde lutaram os\ntreze cavaleiros da lenda.', 16: 'Deserto perigoso{81 16} lar de\nmonstros e tesouros.',
  17: 'Vento frio sopra desta\ncaverna.\fUma cidade antiga dizem\ndormir lá no fundo.', 18: 'Sempre se ouve o canto\ndos pássaros aqui.\fUm forte abandonado fica\nno meio da mata.',
  19: 'Deserto das areias que\nlatem.\fDizem vir dos ossos de\numa besta celeste.', 20: 'Deserto de miragens e\nchocobos vermelhos.', 21: 'Planícies onduladas e\npragas de insetos.',
  22: 'Terras planas de areia\namarela e terra vermelha.\fÂmbar costuma ser achado\naqui entre as rochas.', 24: 'Floresta verde, famosa\npelo minério de materita.', 25: 'Cavernas antigamente\nexploradas por mithril.',
  27: 'Jagd sem lei onde se\nouvem vozes fantasmas.', 28: 'Jagd sem lei destruído\npela magia selvagem.', 29: 'Belo vale onde as rochas\nbrilham em âmbar.\fOs reis de Ivalice tinham\num palácio de verão aqui.',
 },
 0x513A8C: {
  7: '[Leis Injustas!]\nO ressentimento contra a\nRainha Remedi cresce nos\núltimos anos.\fMotivo? Mudanças\nfrequentes e aparentemente\narbitrárias nas leis. Já\nchegou ao ponto de alguns\ndizerem que ela "faz isso\npara agradar o pirralho\ndo príncipe."',
  32: '[Nossos Heróis!]\nOs membros do Clã\n{40 25 03} são\nnossos heróis!\nMostrem aos clãs Borzoi\nquem manda!',
  40: '[Falgabird]\nOuvi dizer que o esquadrão\nespecial "Falgabird" dos\nAsas Vermelhas procura\no Clã {40 25 03},\ndepois do que fizeram\ncom o Clã Borzoi...',
  43: '[Paz, Enfim]\nOs Asas Vermelhas foram\nexpulsos de Ivalice\nenfim!\nObrigado,\nClã {40 25 03}!',
  47: '[Heróis do Povo]\nOs Asas Vermelhas se\nforam de Ivalice para\nsempre desta vez!\nDevemos a vida a vocês,\nClã {40 25 03}!',
  57: '[Ruínas em Nargai!]\nRuínas antigas foram\nachadas no fundo da\nCaverna de Nargai.\nO Clã {40 25 03} leva\no crédito.\fA entrada das ruínas\nparece ser uma estátua\nna caverna. Talvez haja\noutras estátuas\npor aí?',
  60: '[! Habilidades !]\nPara vencer ao engajar,\ndomine habilidades! Suas\narmas e armaduras definem\nquais habilidades usar,\nentão escolha com cuidado.\fVocê também precisa de\nPontos de Habilidade (AP)\npara aprendê-las{81 16} ganhe-os\nequipando armaduras e armas\ne cumprindo missões.\fTodos que vão numa missão\npodem ganhar AP, então\nleve seus amigos! Só isso,\nboa sorte!',
  61: '[! Tipos de Habilidade !]\nHabilidades de Ação:\n{40 3e 0a}Ações padrão, como\n{40 3e 0a}Magia Negra ou Téc. Monge.\nHab. de Reação:\n{40 3e 0a}Esquivar ou revidar\n{40 3e 0a}ao ser atacado.\fHab. de Apoio:\n{40 3e 0a}Reforços como\n{40 3e 0a}Espada Dupla.\nHab. de Combo:\n{40 3e 0a}Ativadas quando um\n{40 3e 0a}aliado usa um "combo."',
  65: '[! Condições de Vitória !]\nAchou que engajar era só\nderrotar o inimigo? Pense\nde novo--há vários tipos\nde vitória conforme o\nengajamento.\fVeja a condição durante o\nengajamento escolhendo\n"Missão" no menu principal.\nMas há também condição de\nderrota, cuidado!\fSe {40 25 00} sair do\nengajamento, seja preso ou\nzumbificado e eliminado,\nvocê perde!',
  85: '[! Níveis de Habilidade !]\nHá oito níveis de\nhabilidade:\n{40 67 86} Combate{40 3e 1b}{40 67 87} Magia\n{40 67 88} Forja{40 3e 16}{40 67 89} Ofício\n{40 67 8a} Avaliar{40 3e 15}{40 67 8b} Coleta\n{40 67 8c} Negociar{40 3e 10}{40 67 8d} Rastro',
  88: '[! Link !]\nConecte um cabo Game Boy\nAdvance{81 e6} Game Link{81 e6}\npara se ligar a outros.\nPodem lutar juntos,\ntrocar itens e até\ntrocar membros do clã!',
  90: '[! Itens de Troca !]\nItens de troca se compram\ncomo itens comuns, e\nalguns são barbadas!\nQuanto mais você faz link,\nmais itens o Nono oferece,\nfaça link sempre, kupo--!',
 },
}
