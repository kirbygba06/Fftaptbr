# FFTA PT-BR: notas do patch (Rebalance v2)

Tudo o que muda em relação ao jogo original (ROM EU "AFXP", slot inglês). Patch: `final_v2/FFTA_ptBR_rebalance_v2.ips`, que inclui a tradução PT-BR. Aplique sobre a ROM limpa e comece um save novo. Gerado automaticamente a partir das tabelas de antes/depois (`final_v1/csv`, `final_v2/csv`).

## Resumo

- **Classes:** atributos base e crescimento rebalanceados; Velocidade e Evade comprimidos (menos extremos).
- **Equipamento:** armas raras menos absurdas, armaduras de topo mais fortes, escudos com o dobro de Evade e preços coerentes.
- **Habilidades:** 15 habilidades novas no lugar de habilidades inúteis; dezenas de ajustes de MP, poder, área e AP.
- **Magias:** Fogo, Gelo e Raio passam a ter funções diferentes.
- **Contra-jogo:** itens de loja baratos dão imunidade a Encanto e Confusão.
- **Sem mudanças de rotina do jogo (ASM):** só valores das tabelas.

## Habilidades novas

Elas ocupam o lugar de habilidades que quase não tinham uso. Quem aprendia a antiga aprende a nova, com a mesma arma e o mesmo custo de AP.

| Nova | Substitui | Classes | Efeito | MP |
|---|---|---|---|---|
| **Golpe Seco** | Magicbreak | Soldado, Guerreiro | golpe com a arma: dano + atrasa o turno | — |
| **Formação** | Sensor | Soldado | Proteção (aliados ao redor) | 10 |
| **Égide** | Parley | Paladino | Proteção + Barreira | 12 |
| **Empurrão** | Drop Weapon | Paladino, Defensor | golpe com a arma: dano + empurra | — |
| **Baluarte** | Hibernate | Defensor | Barreira (aliados ao redor) | 10 |
| **Sangue Wyrm** | Wyrmtamer | Dragoon | Regen + reforça o próximo ataque (em si mesmo) | — |
| **Rastreio** | Oust | Caçador | golpe com a arma: metade do dano + Lento | — |
| **Pregar** | Burial | Arqueiro | golpe com a arma: dano + imobiliza | — |
| **Shuriken** | Unspell | Ninja | dano + paralisa | 6 |
| **Mog Empurra** | Mog Peek | Cavaleiro Mog | golpe com a arma: dano + empurra | — |
| **Mantra** | Holy Sign | Monge Branco | Regen (aliados ao redor) | — |
| **Lâmina Vampira** | Featherblow | Esgrimista | golpe com a arma: dano + recupera HP = dano | — |
| **Faca Venenosa** | Gil Toss | Malabarista | golpe com a arma: dano + veneno | — |
| **Coragem** | Friend | Animista | reforça o próximo ataque (aliados ao redor) | 12 |
| **Tiro Choque** | Aim: Wallet | Atirador | golpe com a arma: dano + atrasa o turno | — |

## Magias: Fogo, Gelo e Raio

No original, as três eram idênticas (poder 30/40/50, MP 6/12/24). Agora cada elemento tem um papel:

| Magia | Poder | MP | Efeito novo |
|---|---|---|---|
| Fogo | 30→33 | 6 | — |
| Fogo+ | 40→51 | 12→14 | — |
| Fogo++ | 50→75 | 24→30 | — |
| Trovão | 30→27 | 6 | atrasa o turno se acertar |
| Trovão+ | 40→41 | 12→14 | atrasa o turno se acertar |
| Trovão++ | 50→61 | 24→30 | atrasa o turno se acertar |
| Gelo | 30→24 | 6 | causa Lento se acertar |
| Gelo+ | 40→37 | 12→14 | causa Lento se acertar |
| Gelo++ | 50→54 | 24→30 | causa Lento se acertar |

**Fogo** causa mais dano. **Gelo** causa menos dano, mas deixa o alvo Lento. **Raio** fica no meio e atrasa o turno do alvo.

## Habilidades alteradas

| Habilidade | Classes | Mudança |
|---|---|---|
| Abanar Cauda | Animista | MP 8→6 |
| Apressar | Mago Temporal | MP 24→19; alvo único → área (raio 1) |
| Ar Brilhante | Elementalista | MP 12→10; poder 30→40 (+33%); alvo único → área (raio 1) |
| Ataque Chocobo | Animista | MP 12→10; poder 45→52 (+16%) |
| Carbúnculo | Invocador | MP 12→10 |
| Chama Branca | Elementalista | MP 24→19 |
| Chicote de Fogo | Elementalista | poder 30→40 (+33%) |
| Chuva do Sono | Elementalista | MP 12→10; poder 30→40 (+33%); alvo único → área (raio 1) |
| Contar Ovelhas | Animista | MP 8→6 |
| Cruz Estelar | Ilusionista | poder 17→30 (+76%) |
| Cruz Santa | Paladino | MP 24→18; poder 35→45 (+29%) |
| Cuidar | Paladino | poder 30→45 (+50%) |
| Culinária | Animista | MP 32→26; alvo único → área (raio 1) |
| Cupido | Arqueiro | MP 0→8 |
| Cura+ | Mago Branco, Bispo | AP 200→100 |
| Dilúvio | Ilusionista | poder 17→30 (+76%) |
| Esquecimento | Ninja, Assassino | alvo único → área (raio 1) |
| Febre | Assassino | MP 12→10; alvo único → área (raio 1) |
| Lâmina Sagrada | Paladino | MP 32→24 |
| Pancada | Guerreiro | poder 45→52 (+16%) |
| Pesadelo | Assassino | MP 18→14 |
| Piscada Gélida | Ilusionista | poder 20→30 (+50%) |
| Proeminência | Ilusionista | poder 20→30 (+50%) |
| Provocar | Soldado | alvo único → área (raio 1) |
| Punho Distante | Lutador, Monge Branco | poder 35→40 (+14%) |
| Pó Pesado | Elementalista | MP 12→10; poder 30→40 (+33%); alvo único → área (raio 1) |
| Pó de Estrela | Ilusionista | poder 20→30 (+50%) |
| Rasgar Ar | Lutador, Monge Branco | poder 45→52 (+16%) |
| Rasgar Terra | Monge Branco | poder 34→39 (+15%) |
| Redemoinho | Monge Branco | poder 25→29 (+16%) |
| Reduzir | Guerreiro | alvo único → área (raio 1) |
| Sagrado | Bispo | MP 32→26; poder 50→57 (+14%) |
| Sapo | Alquimista | alvo único → área (raio 1) |
| Selo de Pedra | Assassino | MP 32→40 |
| Socorro | Soldado, Guerreiro | poder 25→40 (+60%) |
| Sujar Provas | Ilusionista | poder 17→30 (+76%) |
| Tempestade | Ilusionista | poder 17→30 (+76%) |
| Tiro Cegante | Artilheiro | MP 0→4 |
| Tiro Confuso | Artilheiro | MP 0→4 |
| Tiro Encantado | Artilheiro | MP 0→4 |
| Tiro Mudo | Artilheiro | MP 0→4 |
| Tiro de Stop | Artilheiro | MP 0→4 |
| Tornado Feroz | Ilusionista | poder 17→30 (+76%) |
| Tremor | Defensor | poder 30→34 (+13%) |
| Unicórnio | Invocador | AP 200→100 |
| Vento | Bispo, Sábio | MP 12→10; poder 34→39 (+15%) |
| Véu da Terra | Ninja | poder 15→28; MP 4→8 |
| Véu de Fogo | Ninja | poder 15→28; MP 4→8 |
| Véu de Madeira | Ninja | poder 15→28; MP 4→8 |
| Véu de Metal | Ninja | poder 15→28; MP 4→8 |
| Véu de Água | Ninja | poder 15→28; MP 4→8 |
| Água | Bispo, Sábio | MP 12→10; poder 34→39 (+15%) |

## Itens de contra-jogo

- **Manoplas** (à venda na loja): agora imune a Encanto.
- **Botas Batalha** (à venda na loja): agora imune a Confusão.

## Classes

Regras gerais:

- Velocidade comprimida em torno de 100 (70% da distância original): as classes muito rápidas perdem um pouco e as lentas ganham.
- Evade comprimido em torno de 50 (60% da distância).
- ATK e PM base ×1,12 para acompanhar a compressão das armas raras.
- Orçamento de atributos ajustado por classe a partir de 12 rodadas de simulação 5v5 (milhares de batalhas por nível).
- Blue Mage, Ladrão, Morpher, Domador e Engenhoqueiro recebem só o ajuste global, porque o simulador não modela os kits deles.

Valores: base → novo. "Cresc." é o crescimento por nível. Só aparece o que mudou.

| Classe | Raça | HP | MP | Vel. | ATK | DEF | PM | RM | Evade | Cresc. ATK | Cresc. DEF | Cresc. PM | Cresc. RM | Cresc. HP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Arqueiro | Humano | 36→35 | = | 106→104 | 72→79 (+10%) | 72→71 (-1%) | 64→71 (+11%) | 80→79 (-1%) | = | 7.2→8.6 | 7.2→6.7 | 6.4→6.5 | 8.1→7.7 | 7.2→6.9 |
| Caçador | Humano | 34→30 | = | 112→108 | = | 68→60 (-12%) | = | 84→75 (-11%) | 55→53 | 8.8→9.5 | 6.8→5.7 | 6.8→6.2 | 8.4→7.2 | 6.8→5.9 |
| Ilusionista | Humano | 26→28 | 38→32 | 89→92 | 60→72 (+20%) | 64→69 (+8%) | 92→111 (+21%) | 84→90 (+7%) | 30→38 | 6.1→6.6 | 6.4→6.9 | 9.2→11.6 | 8.4→9.5 | 5.2→5.6 |
| Ladrão | Humano | = | = | 110→107 | 76→85 (+12%) | = | 76→85 (+12%) | = | 65→59 | 7.6→8.7 | 7.6→7.1 | 7.6→8.3 | 6.4→6.1 | 6.6→6.1 |
| Lutador | Humano | 36→35 | = | 104→103 | 92→100 (+9%) | 80→78 (-2%) | 56→61 (+9%) | 68→66 (-3%) | 45→47 | 9.2→10.8 | 8.1→7.5 | = | 6.8→6.4 | 7.2→6.9 |
| Mago Azul | Humano | = | = | = | 80→90 (+12%) | = | 84→94 (+12%) | = | 55→53 | 8.1→8.4 | = | 8.4→9.9 | 9.2→10.1 | = |
| Mago Branco | Humano | 30→27 | = | 108→106 | 60→61 (+2%) | 73→67 (-8%) | 84→86 (+2%) | 80→73 (-9%) | 40→44 | 6.2→5.9 | 7.3→6.7 | 8.4→9 | 8.2→8.3 | 6.1→5.6 |
| Mago Negro | Humano | = | 36→31 | 96→97 | 64→72 (+12%) | = | 88→99 (+12%) | = | 35→41 | 6.4→6.5 | = | 8.8→10.4 | 9.6→10.1 | = |
| Ninja | Humano | = | = | 120→114 | 84→92 (+10%) | 72→71 (-1%) | 80→88 (+10%) | 76→75 (-1%) | 60→56 | 8.4→9.4 | 7.2→6.6 | 8.1→8.7 | 7.6→7.2 | 5.8→5.3 |
| Paladino | Humano | 38→40 | = | 98→99 | 80→95 (+19%) | 92→98 (+7%) | 72→86 (+19%) | 88→94 (+7%) | 35→41 | 8.1→9.4 | 9.2→11 | 7.2→7.9 | 8.8→9.8 | 7.6→8.9 |
| Soldado | Humano | 40→42 | = | = | 88→104 (+18%) | 88→93 (+6%) | 60→71 (+18%) | 72→76 (+6%) | = | 8.8→10.1 | 8.8→10.4 | 6→6.5 | 7.2→8 | 8.4→9.8 |
| Bispo | Bangaa | 30→35 | = | 88→92 | 72→93 (+29%) | 68→78 (+15%) | 88→114 (+30%) | 76→88 (+16%) | 30→38 | 7.2→8.7 | 6.8→7.8 | 8.8→11.9 | 7.6→9.6 | 6.1→7 |
| Defensor | Bangaa | 42→39 | = | 92→94 | 88→92 (+5%) | 94→88 (-6%) | 65→68 (+5%) | 72→67 (-7%) | 35→41 | 8.8→8.9 | 9.4→9.8 | 6.5→6.3 | 7.2→7.1 | 8.4→8.6 |
| Dragoon | Bangaa | 40→36 | = | 104→103 | = | 84→75 (-11%) | = | 60→53 (-12%) | 40→44 | 9.6→10.3 | 8.4→7.1 | 5.6→5.1 | 6.4→5.5 | 8.2→7.1 |
| Gladiador | Bangaa | 40→37 | = | 97→98 | 94→98 (+4%) | 88→82 (-7%) | 59→61 (+3%) | 64→59 (-8%) | 45→47 | 9.4→10.6 | 8.8→7.8 | 5.9→5.6 | 6.4→5.7 | 8.2→7.5 |
| Guerreiro | Bangaa | 46→48 | = | 95→96 | 92→107 (+16%) | 84→87 (+4%) | 62→72 (+16%) | 68→71 (+4%) | = | 9.2→10.4 | 8.4→9.8 | 6.2→6.6 | 6.8→7.4 | 9.2→10.5 |
| Monge Branco | Bangaa | 32→29 | = | 108→106 | 80→81 (+1%) | 76→68 (-11%) | 83→84 (+1%) | 68→61 (-10%) | 60→56 | 8.1→8.3 | 7.6→6.4 | 8.3→8.2 | 6.8→5.9 | 6.4→5.4 |
| Templário | Bangaa | 36→38 | = | 86→90 | 92→109 (+18%) | 97→103 (+6%) | 84→100 (+19%) | 72→76 (+6%) | 40→44 | 8.2→9.4 | 9.7→11.5 | 8.4→9.2 | 7.2→8 | 7.2→8.4 |
| Alquimista | Nu Mou | 30→33 | 48→41 | 92→94 | 59→72 (+22%) | 65→71 (+9%) | 92→113 (+23%) | 96→105 (+9%) | 35→41 | 5.9→6.5 | 6.5→7.1 | 9.2→11.8 | 9.6→11 | 6.1→6.7 |
| Domador | Nu Mou | = | = | 104→103 | 88→99 (+12%) | = | 68→76 (+12%) | = | 55→53 | 8.8→9.2 | = | 6.8→8 | 8.4→9.2 | = |
| Ilusionista | Nu Mou | 25→26 | 46→39 | 89→92 | 57→67 (+18%) | 64→67 (+5%) | 96→113 (+18%) | 88→93 (+6%) | 30→38 | 5.7→6.1 | 6.4→6.7 | 9.6→11.9 | 8.8→9.7 | 5.1→5.4 |
| Mago Branco | Nu Mou | 29→26 | = | 108→106 | = | 73→65 (-11%) | = | 84→75 (-11%) | 40→44 | 5.7→5.3 | 7.3→6.5 | 8.8→9.2 | 8.4→8.2 | 5.8→5.2 |
| Mago Negro | Nu Mou | 27→26 | 42→36 | 96→97 | 62→68 (+10%) | 68→66 (-3%) | 92→101 (+10%) | 100→98 (-2%) | 35→41 | 6.2→6.1 | 6.8→6.6 | 9.2→10.6 | 10.2→10.5 | 5.4→5.3 |
| Mago Temporal | Nu Mou | 26→29 | = | 98→99 | 56→71 (+27%) | 68→77 (+13%) | 100→127 (+27%) | 96→109 (+14%) | 30→38 | 5.6→6.6 | 6.8→7.7 | 10.2→13.6 | 9.6→12 | 5.2→5.9 |
| Metamorfo | Nu Mou | = | = | 110→107 | 70→78 (+11%) | = | 76→85 (+12%) | = | 30→38 | 7.1→7.4 | = | 7.6→8.9 | 8.1→8.9 | = |
| Sábio | Nu Mou | 38→35 | 38→32 | 85→90 | 84→88 (+5%) | 76→71 (-7%) | 92→96 (+4%) | 76→71 (-7%) | = | 8.4→7.9 | 7.6→7.1 | 9.2→10.1 | 7.6→7.5 | 7.6→7.1 |
| Arqueiro | Viera | 36→35 | = | 112→108 | 80→86 (+8%) | 68→65 (-4%) | 72→77 (+7%) | 76→73 (-4%) | = | 8.1→9.4 | 6.8→6.2 | 7.2→7.1 | 7.6→7 | 7.2→6.8 |
| Assassino | Viera | 26→25 | = | 125→118 | 88→95 (+8%) | 68→66 (-3%) | 92→100 (+9%) | 72→70 (-3%) | 65→59 | 8.8→9.7 | 6.8→6.1 | 9.2→9.8 | 7.2→6.7 | 5.2→4.7 |
| Atirador | Viera | 31→30 | = | 105→104 | 94→101 (+7%) | 68→65 (-4%) | 76→82 (+8%) | 76→73 (-4%) | 60→56 | 9.4→10.9 | 6.8→6.2 | 7.6→7.5 | 7.6→7 | 6.2→5.8 |
| Elementalista | Viera | 34→33 | 18→15 | 104→103 | 80→88 (+10%) | 76→75 (-1%) | 88→97 (+10%) | 76→75 (-1%) | = | 8.1→8 | 7.6→7.5 | 8.8→10.2 | 7.6→7.9 | 6.8→6.7 |
| Esgrimista | Viera | 38→40 | = | 110→107 | 84→99 (+18%) | 80→84 (+5%) | 76→89 (+17%) | 72→75 (+4%) | 60→56 | 8.4→10 | 8.1→7.9 | 7.6→8.7 | = | 7.6→7.4 |
| Invocador | Viera | 28→31 | 34→29 | 90→93 | 65→79 (+22%) | 64→70 (+9%) | 100→122 (+22%) | 80→87 (+9%) | 30→38 | 6.5→7.1 | 6.4→7 | 10.1→12.9 | 8.4→9.6 | 5.6→6.1 |
| Mago Branco | Viera | 30→27 | = | 115→110 | = | 72→64 (-11%) | = | 76→68 (-11%) | 40→44 | 6.2→5.7 | 7.2→6.4 | 8.8→9.2 | 7.6→7.4 | 6.2→5.5 |
| Mago Vermelho | Viera | 34→31 | 22→19 | 96→97 | 81→84 (+4%) | 76→70 (-8%) | 84→87 (+4%) | 76→70 (-8%) | = | 8.1→7.6 | 7.6→7 | 8.4→9.1 | 7.6→7.4 | 6.8→6.3 |
| Animista | Moogle | 36→32 | = | = | = | 88→78 (-11%) | = | 88→78 (-11%) | 55→53 | 7.6→7 | 8.8→7.8 | 7.2→7.5 | 8.8→8.6 | 7.2→6.4 |
| Artilheiro | Moogle | 30→27 | = | 95→96 | = | 92→82 (-11%) | = | 80→71 (-11%) | 65→59 | 6.8→7.3 | 9.2→7.8 | 5.6→5.1 | 8.1→6.9 | 6.2→5.4 |
| Cavaleiro Mog | Moogle | 35→39 | = | 98→99 | 88→111 (+26%) | 96→108 (+12%) | 60→76 (+27%) | 80→90 (+12%) | 45→47 | 8.8→10.8 | 9.6→12.1 | 6.2→7.2 | 8.3→9.8 | 7.1→8.8 |
| Engenhoqueiro | Moogle | = | = | 90→93 | 80→90 (+12%) | = | 80→90 (+12%) | = | = | 8.2→8.9 | 9.6→10.8 | 8.3→8.6 | 10.2→10.7 | 7.2→7.9 |
| Ladrão | Moogle | = | = | 110→107 | 73→82 (+12%) | = | 68→76 (+12%) | = | 70→62 | 7.3→8.3 | 8.4→7.8 | 6.8→7.5 | 7.6→7.3 | 5.8→5.4 |
| Mago Negro | Moogle | 27→28 | 28→24 | 96→97 | 57→67 (+18%) | 76→80 (+5%) | 84→99 (+18%) | 97→102 (+5%) | 35→41 | 5.7→6 | 7.6→8 | 8.4→10.4 | 9.7→10.7 | 5.4→5.7 |
| Mago Temporal | Moogle | 26→29 | = | 98→99 | 56→71 (+27%) | 76→86 (+13%) | 92→117 (+27%) | 94→107 (+14%) | 30→38 | 5.6→6.6 | 7.6→8.6 | 9.2→12.3 | 9.4→11.7 | 5.2→5.9 |
| Malabarista | Moogle | 34→33 | = | 108→106 | 80→87 (+9%) | 100→97 (-3%) | 64→69 (+8%) | 64→62 (-3%) | 40→44 | 8.2→9 | 9.9→8.9 | 6.4→6.8 | 6.4→5.9 | 6.8→6.1 |

## Equipamento

- **Armas:** as que passam de 45 de ATK são comprimidas (45 + 55% do excesso). As armas de loja não mudam.
- **Armaduras, elmos e chapéus:** a DEF e a RM crescem em curva. As peças fracas quase não mudam e as de topo chegam a ×3.
- **Escudos:** Evade ×2.
- **Preços:** dentro de cada tipo de arma, arma mais forte nunca é mais barata. O preço de venda é metade do de compra.

### Armas (ATK) (46 itens)

| Item | ATK |
|---|---|
| Alma Malboro | 47→46 (-2%) |
| Alma Rukavi | 67→57 (-15%) |
| Alma Sinistra | 49→47 (-4%) |
| Arco Gastra | 51→48 (-6%) |
| Arco Juramento | 61→54 (-11%) |
| Arma Chamado | 59→53 (-10%) |
| Ayvuir Azul | 51→48 (-6%) |
| Ayvuir Rubro | 62→54 (-13%) |
| Cacto | 62→54 (-13%) |
| Carvão Aceso | 47→46 (-2%) |
| Castanhola Fell | 47→46 (-2%) |
| Chirijiraden | 65→56 (-14%) |
| Cinquedea | 57→52 (-9%) |
| Claymore | 49→47 (-4%) |
| Eclipse | 76→62 (-18%) |
| Espada Arcana | 48→47 (-2%) |
| Espada El Cid | 47→46 (-2%) |
| Espada Fera | 50→48 (-4%) |
| Espada Mestra | 59→53 (-10%) |
| Espeto Bangaa | 53→49 (-8%) |
| Estreledge | 77→63 (-18%) |
| Excalibur | 47→46 (-2%) |
| Excalibur2 | 87→68 (-22%) |
| Graxa Explos. | 59→53 (-10%) |
| Lança Fera | 51→48 (-6%) |
| Lança de Kain | 47→46 (-2%) |
| Lança de Odin | 55→50 (-9%) |
| Lua de Seda | 55→50 (-9%) |
| Lâmina Adaman | 65→56 (-14%) |
| Lâmina Ébano | 84→66 (-21%) |
| Malarco | 55→50 (-9%) |
| Manganês | 47→46 (-2%) |
| Masamune | 65→56 (-14%) |
| Masamune 100 | 79→64 (-19%) |
| Mulher Fatal | 49→47 (-4%) |
| Mãos Mágicas | 52→49 (-6%) |
| Nagrarok | 75→62 (-17%) |
| Oblige | 48→47 (-2%) |
| Oricalco | 60→53 (-12%) |
| Quebra Isca | 51→48 (-6%) |
| Rhomphaia | 57→52 (-9%) |
| Tabarise | 47→46 (-2%) |
| Tiro Preso | 47→46 (-2%) |
| Tridente | 50→48 (-4%) |
| Tulwar | 55→50 (-9%) |
| Zankplus | 49→47 (-4%) |

### Armaduras e acessórios (DEF / RM) (82 itens)

| Item | DEF | RM |
|---|---|---|
| Anel Mágico | = | 10→20 |
| Armad. Adaman | 58→174 | = |
| Armad. Bronze | 30→34 | = |
| Armad. Diam. | 40→58 | = |
| Armad. Ferro | 34→42 | = |
| Armad. Materia | 52→119 | 16→32 |
| Armad. de Ouro | 42→65 | = |
| Armadura Genji | 46→82 | 12→16 |
| Armadura Opala | 42→65 | = |
| Bandana | 6→10 | = |
| Botas Batalha | 7→10 | = |
| Botas Rubras | = | 5→10 |
| Braçadeiras | 12→36 | = |
| Braçal Genji | 10→20 | = |
| Braçal de Osso | 6→7 | 8→11 |
| Brigantina | 37→82 | = |
| Brinco de Rubi | = | 6→7 |
| Cachusha | 2→6 | 5→10 |
| Calígula | 10→30 | = |
| Capa Ceifador | 32→96 | 36→44 |
| Casaco Prata | 30→76 | 38→49 |
| Casaco do Juiz | 38→89 | 28→56 |
| Chapéu Branco | = | 14→17 |
| Chapéu Ladrão | 8→24 | = |
| Chapéu Mago | = | 10→11 |
| Chapéu Negro | = | 16→23 |
| Colete Adaman | 30→46 | = |
| Colete Miragem | 32→54 | 16→18 |
| Colete Sobrev. | 34→63 | = |
| Conj. Galmia | 26→34 | 18→21 |
| Conjunto Brint | 28→39 | 16→18 |
| Couraça | 28→31 | = |
| Elmo Bangaa | 16→48 | 6→8 |
| Elmo Cruz | 9→11 | = |
| Elmo Desfile | 13→24 | = |
| Elmo Diamante | 11→16 | 5→6 |
| Elmo Genji | 15→38 | 6→8 |
| Elmo Hanya | 12→20 | 8→16 |
| Elmo Opala | 7→8 | = |
| Esc. Devaneio | 5→6 | = |
| Escaravelho | = | 8→11 |
| Escudo Genji | 10→30 | = |
| Escudo Sacri | 5→6 | = |
| Escudo Égide | 5→6 | = |
| Faixa de Poder | 34→63 | = |
| Fita | 2→6 | 5→10 |
| Grampo Ouro | = | 12→14 |
| Kimono de Judô | 34→63 | = |
| Luvas de Fogo | 8→11 | 10→20 |
| Malha Carabini | 38→52 | = |
| Malha Dragão | 40→58 | = |
| Malha Espelho | 36→47 | = |
| Manto Branco | 21→29 | 38→49 |
| Manto Chama | 19→24 | 30→33 |
| Manto Cânhamo | 15→16 | 22→23 |
| Manto Mago | 15→16 | 30→33 |
| Manto Mágico | 24→39 | 36→44 |
| Manto Negro | 21→29 | 36→44 |
| Manto Rajada | 19→24 | 30→33 |
| Manto Rubro | 22→32 | 31→35 |
| Manto Senhorial | 28→61 | 42→60 |
| Manto Sábio | 24→39 | 52→104 |
| Manto Templo | 36→75 | 16→18 |
| Manto Trovão | 19→24 | 30→33 |
| Manto de Luz | 25→44 | 40→54 |
| Manto de Seda | 15→16 | 28→30 |
| Manto de Visco | 19→24 | 30→33 |
| Maximiliano | 46→82 | 10→12 |
| Peitoral | 28→31 | = |
| Placa Minerva | 28→39 | 14→15 |
| Placa de Malha | 28→39 | = |
| Placa de Osso | 42→126 | = |
| Placas | 38→52 | = |
| Presilha | 2→6 | 5→10 |
| Tiara | 8→24 | 20→40 |
| Traje Borracha | 28→39 | 16→18 |
| Traje Gaia | 24→29 | = |
| Traje Ninja | 30→46 | = |
| Traje Sombrio | 32→54 | = |
| Traje de Couro | 18→19 | = |
| Wygar | 35→69 | = |
| Único | 34→63 | 24→37 |

### Escudos (Evade) (12 itens)

| Item | Evade |
|---|---|
| A Seráfica | 15→30 |
| Esc. Devaneio | 10→20 |
| Escudo Bronze | 4→8 |
| Escudo Chama | 9→18 |
| Escudo Choco | 10→20 |
| Escudo Genji | 10→20 |
| Escudo Opala | 7→14 |
| Escudo Redondo | 5→10 |
| Escudo Sacri | 10→20 |
| Escudo Shijin | 7→14 |
| Escudo de Gelo | 9→18 |
| Escudo Égide | 10→20 |

### Preços (36 itens)

| Item | Compra | Venda |
|---|---|---|
| Adaga Rondel | 10000→8500 | 5000→4250 |
| Arco Espinho | 1500→2050 | 750→1025 |
| Arco Gêmeo | 8000→8400 | 4000→4200 |
| Arco Ranger | 2000→8250 | 1000→4125 |
| Arco Ventoso | 3000→8300 | 1500→4150 |
| Arco de Prata | 2500→2000 | 1250→1000 |
| Bastão Granizo | 1500→1600 | 750→800 |
| Bastão Trovão | 1500→1550 | 750→775 |
| Báculo Sábio | 9000→7500 | 4500→3750 |
| Cranequim | 5000→8350 | 2500→4175 |
| Defensor | 5000→6050 | 2500→3025 |
| Esmaga Mago | 8000→6500 | 4000→3250 |
| Faca Kris | 3000→2350 | 1500→1175 |
| Flamberge | 5000→6550 | 2500→3275 |
| Gae Bolg | 14000→12000 | 7000→6000 |
| Gume de Gelo | 8000→9050 | 4000→4525 |
| Jambiya | 1700→2400 | 850→1200 |
| Kard | 7000→8550 | 3500→4275 |
| Khukuri | 5000→16050 | 2500→8025 |
| Kikuichimonji | 12000→13550 | 6000→6775 |
| Lâmina Atmos | 4000→8250 | 2000→4125 |
| Lâmina Kwigon | 10000→9000 | 5000→4500 |
| Lâmina Paraiba | 22000→8200 | 11000→4100 |
| Lâmina Solar | 3000→8300 | 1500→4150 |
| Lâmina do Ar | 7000→8400 | 3500→4200 |
| Língua de Fogo | 5000→8350 | 2500→4175 |
| Maça Druida | 6000→7550 | 3000→3775 |
| Maça Energia | 3500→2750 | 1750→1375 |
| Maça de Guerra | 2000→2800 | 1000→1400 |
| Nuvem Celeste | 15000→13500 | 7500→6750 |
| Partasana | 10000→12050 | 5000→6025 |
| Predador | 4000→4550 | 2000→2275 |
| Ragnarok | 7000→6000 | 3500→3000 |
| Striborg | 5000→4500 | 2500→2250 |
| Sétimo Céu | 23000→8200 | 500→4100 |
| Tiptaptwo | 27000→16000 | 500→8000 |

## Não muda

- Rotinas do jogo: fórmulas de dano, duração de status, Combo, Doublecast, Dragonheart.
- Mapas, missões, inimigos fixos, leis e textos da história (além da tradução).
- As descrições das magias Gelo e Raio no jogo ainda não citam o Lento e o atraso de turno.
