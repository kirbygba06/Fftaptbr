# FFTA — Rebalance FINAL v1 (somente dados)

## Como aplicar
- ROM: a mesma do slot inglês da tradução (EU "AFXP", 16 MB).
- Ordem: a tradução PT-BR (`patches/FFTA_ptBR_slot_ingles.ips`) e o rebalance não se sobrepõem em nenhum byte. A ordem não importa.
- Para jogar tudo: aplique `FFTA_rebalance_final_v1.ips`.
- Para testar por partes, os módulos são independentes:
  - `bal20_classes.ips` — atributos base e crescimento das classes, Evade e Velocidade.
  - `bal21_itens.ips` — ATK das armas raras, DEF/RES das armaduras, Evade dos escudos, preços.
  - `bal22_habilidades.ips` — MP, poder, área e AP de 47 habilidades.
  - `bal23_magias.ips` — o trio Fire/Blizzard/Thunder do Black Mage.
- Para desfazer: aplique o arquivo equivalente em `reverter/` (restaura os bytes originais). Use **um save novo**: o save guarda atributos já crescidos, então mudar de patch no meio da campanha mistura as duas versões.

## O que conferir jogando
- Blizzard/Blizzara/Blizzaga agora podem causar **Slow**, e Thunder/Thundara/Thundaga **atrasam o turno** do alvo (o alvo volta para o fim da fila). O texto de descrição no jogo ainda não fala disso.
- Toad, Provoke, Downsize, Ague, Oblivion, Heavy Dust, Sliprain, Shining Air, Cuisine e Quicken agora atingem **área (raio 1)**. Elas também acertam aliados que estiverem dentro da área.
- Os tiros de status do Gunner custam 4 MP (originalmente 0) e o Cupid custa 8.

`csv/` tem o valor original e o novo de cada campo alterado. `verificacao.json` mostra 0 divergências, 0 sobreposições e reversão idêntica à ROM original.
