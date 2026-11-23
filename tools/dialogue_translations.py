# -*- coding: utf-8 -*-
"""Textos de ajuda/diálogo (bancos de strings do inglês). Chave: endereço do banco -> {índice: texto}.
'\\n' = quebra de linha do jogo. Só entram strings "simples" (sem variáveis/compressão)."""

_TIPOS = {'r': 'Combo à distância', 'f': 'Combo infalível', 'w': 'Combo equilibrado', 'l': 'Combo de longo alcance'}


def _c(tipo, quem):
    return _TIPOS[tipo] + '\npara ' + quem + '.'


DIALOGUE = {
    # ajuda dos comandos de menu
    0x527704: {
        0: 'Veja a ordem de turno\ndas unidades.', 3: 'Altere várias opções\ndo jogo.',
        4: 'Saia da batalha e\nabandone a missão.', 6: 'Veja as leis desta\nbatalha.',
        8: 'Defina a ação que\numa unidade executará.', 9: 'Fique parado. O próximo\nturno chega mais rápido.',
        10: 'Veja o status da unidade.', 11: 'Lute com as mãos nuas\nou com a arma equipada.',
        12: 'Jogue uma bola de neve.\nSem pedras, por favor.',
        13: 'Chame o totema da raça.\nGasta todo o JP.',
        18: 'Mova o cursor para a\nárea selecionada.', 20: 'Salve o jogo atual.',
        22: 'Volte ao título. Jogos\nnão salvos são perdidos.',
        25: 'Volte ao mapa do mundo.', 31: 'Volte ao mapa do mundo.', 36: 'Volte ao mapa do mundo.',
        43: 'Volte ao mapa do mundo.', 32: 'Compre itens\nna loja.', 33: 'Venda itens que carrega.',
        35: 'Veja a lista de\nmonstros capturados.', 40: 'Ouça os rumores\nda taverna.',
        44: 'Troque armaduras,\narmas etc.', 45: 'Troque as habilidades.', 47: 'Remova a unidade do clã.',
        54: 'Execute a ação escolhida.', 55: 'Cancele a ação escolhida.', 56: 'Confirme a seleção.',
        58: 'Veja os detalhes da\nmissão em andamento.', 59: 'Veja a lista de\nmissões cumpridas.',
        60: 'Veja os territórios do\nclã em Ivalice.', 62: 'Veja informações do\nclã do amigo conectado.',
        63: 'Nada equipado.', 69: 'Una-se ao clã de um\namigo em uma missão.',
        70: 'Troque itens e cartas\nde lei com um amigo.', 71: 'Troque membros do clã\ncom um amigo.',
        72: 'Fim da metamorfose.', 75: 'Ofereça armas e armaduras\npara troca.',
        76: 'Ofereça itens de missão\npara troca.', 77: 'Ofereça cartas de lei\npara troca.',
        93: 'Aqui você encontra\nmissões para aceitar.', 96: 'Monstros capturados\nficam neste local.',
    },
    # descrição dos combos por classe
    0x534264: {
        0: _c('r', 'magos azuis'), 2: _c('r', 'caçadores'), 3: _c('f', 'paladinos'),
        4: _c('r', 'bispos'), 5: _c('r', 'magos negros'), 6: _c('w', 'sábios'),
        7: _c('f', 'templários'), 8: _c('f', 'ladrões'), 11: _c('l', 'artilheiros'),
        13: _c('r', 'invocadores'), 14: _c('r', 'magos brancos'), 15: _c('w', 'elementalistas'),
        16: _c('f', 'soldado e guerreiro'), 17: _c('r', 'atiradores'), 18: _c('r', 'ilusionistas'),
        21: _c('f', 'animistas'), 22: _c('r', 'magos temporais'), 23: _c('f', 'esgrimistas'),
        24: _c('f', 'metamorfos'), 25: _c('f', 'ninjas'), 26: _c('l', 'engenhoqueiros'),
        27: _c('l', 'arqueiros'), 28: _c('f', 'gladiadores'), 31: _c('f', 'dragoons'),
        32: _c('w', 'alquimistas'),
    },
}
