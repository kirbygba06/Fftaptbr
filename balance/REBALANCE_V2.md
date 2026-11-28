# Rebalance v2: habilidades e mecânicas novas

**Para jogar:** aplique `final_v2/FFTA_ptBR_rebalance_v2.ips` sobre a ROM limpa (EU "AFXP"). É um patch único com:
- a tradução PT-BR, já com os nomes e descrições das habilidades novas;
- o rebalance v1 (classes, itens, habilidades e magias);
- o v2 (habilidades novas e itens de contra-jogo).

Use um save novo.

## 1. O que estudei e o que levei para o FFTA

| Jogo | Ideia de design | Como entra no FFTA |
|---|---|---|
| **Into the Breach** | Empurrar é o verbo central: o dano importa menos que a posição. Clareza acima de esperteza. | **Empurrão** como ferramenta de tanque (Paladino, Defensor, Cavaleiro Mog). O motor já tem "Knockback", que só o Tremor usava. |
| **Triangle Strategy** | Cada ação mexe no tabuleiro (flanco, seguimento). Turno é recurso. | **Ritmo**: atrasar o turno do inimigo (Raio, Golpe Seco, Tiro Choque) e deixá-lo Lento (Gelo, Rastreio). Controle de tempo vira identidade de classe. |
| **Tactics Ogre Reborn** | Classes fracas ganharam ferramentas próprias (auto-habilidades, buffs) em vez de só números maiores. | As classes do fundo do ranking ganham uma **função** nova, não só +X%. |
| **FFTA2** | Precisão deixou de ser a principal forma de equilibrar. Leis punem menos. | Nada de "habilidade boa com 30% de acerto": as novas usam efeitos dependentes do acerto do golpe (Eff1Dep). |
| **FFT / FFV** | Papéis claros (tanque, suporte, controlador) e combinação de conjuntos. Contra-jogo por equipamento (Ribbon, anéis). | **Itens de contra-jogo** acessíveis: imunidade a Encanto e Confusão em itens de loja baratos. |

Os princípios que segui:
1. Toda habilidade nova precisa de um motivo para ser escolhida e de um custo (dano menor, MP, turno gasto).
2. Mecânica é melhor que número.
3. Nada pode virar a escolha óbvia.
4. Tem que ser legível: o efeito está no nome e na descrição.

## 2. Como as habilidades novas foram feitas (sem ASM)
- **Efeitos:** o motor tem 183 efeitos (catalogados em `fx_catalog.json`): empurrão, atraso, dreno, Regen, Proteção, Barreira, Boost, imobilizar, paralisar, veneno e outros. Cada habilidade tem 4 espaços de efeito, e o 2º pode depender do acerto do 1º.
- **Slots reaproveitados:** troquei habilidades inúteis, que o simulador mostrou com 0% de uso e que no jogo são de nicho (Sensor, Parley, Wyrmtamer, Oust, Burial, Mog Peek, Gil Toss etc.). Cada uma herda do slot antigo o ID, o custo de AP, quem aprende e a arma que ensina. Do "template" vêm animação, flags e IA. Depois troco os efeitos, poder, MP, alcance e área.
- **Textos:** os nomes e descrições em PT entram pela tradução:
  - o nome fica no menu `0x720D44`, no índice NNNN − 1 da lista de habilidades da raça;
  - a descrição fica no banco `0x529514`, no índice DDDD − 105;
  - as listas de habilidades por raça ficam em `0x6DF4D4` (5 ponteiros, registros de 8 bytes).

## 3. As 15 habilidades novas

| Classe | Antes (inútil) | Agora | Efeito | Uso no simulador (nv. 25 / 45) |
|---|---|---|---|---|
| Soldado, Guerreiro | Magicbreak | **Golpe Seco** | golpe com a arma + atrasa o turno do alvo | 20% / 2% · 12% / 3% |
| Soldado | Sensor | **Formação** | Proteção nos aliados ao redor (10 MP) | – / 3% |
| Paladino | Parley | **Égide** | Proteção + Barreira em um aliado (12 MP) | 47% / 9% |
| Paladino, Defensor | Drop Weapon | **Empurrão** | golpe com a arma + empurra | 17% / 2% |
| Defensor | Hibernate | **Baluarte** | Barreira nos aliados ao redor (10 MP) | 2% / 2% |
| Dragoon | Wyrmtamer | **Sangue Wyrm** | Regen + Boost em si mesmo | 37% / 37% |
| Caçador | Oust | **Rastreio** | tiro com metade do dano + Lento | 55% / 17% |
| Arqueiro | Burial | **Pregar** | flecha + imobiliza | 23% / 19% |
| Ninja | Unspell | **Shuriken** | arremesso (poder 35, alcance 4) + paralisa (6 MP) | 32% / 23% |
| Cavaleiro Mog | Mog Peek | **Mog Empurra** | golpe + empurra | 4% / 2% |
| Monge Branco | Holy Sign | **Mantra** | Regen nos aliados ao redor | 7% / 7% |
| Esgrimista | Featherblow | **Lâmina Vampira** | golpe + recupera HP igual ao dano | 3% / 2% |
| Malabarista | Gil Toss | **Faca Venenosa** | golpe + veneno | 18% / 6% |
| Animista | Friend | **Coragem** | Boost nos aliados ao redor (12 MP) | – / 2% |
| Atirador | Aim: Wallet | **Tiro Choque** | tiro + atrasa o turno | 4% / 2% |

Também mudam:
- **Véus do Ninja:** poder 15 → 28 e MP 4 → 8.
- **Contra-jogo:** Gauntlets (loja, 2000 gil) ficam imunes a Encanto, e Battle Boots (loja, 1000) imunes a Confusão. Isso dá resposta ao Encanto sem ASM.

Testei em duas rodadas. Na primeira, Golpe Seco e Tiro Choque com meio dano, Fumaça (cegueira em área) e Tudo ou Nada quase não eram usadas, e Rastreio dominava. Corrigi para a versão da tabela.

## 4. Resultado no simulador (5v5, progressão real; 12 mil batalhas no nível 25, 4 mil no 10, 6 mil no 45)

| | σ entre classes (nv. 10 / 25 / 45) | máx. (25 / 45) |
|---|---|---|
| v1 (F3) | 8,7 / 8,3 / 6,3 | +12 / +14 |
| **v2** | 9,3 / 8,4 / 6,5 | +13 / +15 |

- **Mais opções sem quebrar:** 13 das 15 habilidades novas passam de 3% de uso, e o equilíbrio geral fica igual (dentro do ruído).
- **Quem mais ganhou:** Dragoon +3, Arqueiro (Viera) +3, Ninja +2, Elementalist +2.
- **Ressalva, Paladino:** −4 no simulador. A IA gasta muitos turnos com Égide, e o simulador subestima Proteção e Barreira. Jogando, você só usa quando vale a pena. Se ele parecer fraco no jogo, o próximo passo é mais orçamento de atributos.
- **Pouco usadas:** Baluarte, Coragem e o Empurrão do Defensor ficam abaixo de 3%. O Defensor já tem Mow Down como golpe principal.

## 5. E classes novas?
Criar uma classe do zero ainda não é viável. Ela precisa de:
- sprite e animações para a raça;
- entrada no menu de troca de classe;
- nome, descrição e requisitos.

Requisitos e lista de habilidades são dados (`0x30` do registro da classe e a lista por raça), mas o menu de classes por raça e os sprites não estão mapeados. O que dá para fazer agora, e foi feito, é **dar papéis novos às classes fracas**:
- **Paladino** protege: Égide e Empurrão.
- **Arqueiro** controla: Pregar.
- **Caçador** rastreia: Rastreio.
- **Ninja** atrapalha: Shuriken e Véus úteis.
- **Dragoon** se sustenta: Sangue Wyrm.
- **Soldado** é vanguarda: Golpe Seco e Formação.

## 6. Próximos passos
Com dados (sem ASM):
- **Afinidades elementais por classe:** o registro da classe tem 3 bits por elemento (fraco, normal, nulo, absorve, resiste). Combinado com bastões que reforçam um elemento, isso cria builds elementais.
- **Requisitos de classe:** a tabela é de dados. Dá para liberar o Paladino mais cedo, por exemplo.
- **Armas com efeito ao acertar** (dreno, Auto-Vida) usando os 3 slots de efeito dos itens.

Com ASM (rotinas a localizar com mGBA + GDB):
- Encanto com 2 turnos.
- Dragonheart uma vez por batalha.
- Doublecast custando o dobro de MP.
- Ataque em pinça ou de seguimento, como em Tactics Ogre Reborn e Triangle Strategy.
- JP do Combo (a instrução já foi localizada em `0x134122`; trocar o multiplicador de 4 para 2 é 1 byte).

## 7. Arquivos
- `v2_design.py`: fonte única do design (simulador, patch e textos).
- `make_v2_ips.py`: gera os módulos, os de reversão, os CSV, `tools/v2_text.py` e o patch único.
- `final_v2/`: `bal24_habilidades_novas.ips`, `bal25_contrajogo.ips`, `reverter/`, `csv/` e `FFTA_ptBR_rebalance_v2.ips`.
- `exp12_v2.py`: o teste.
- `sim2.py`: agora modela dreno, empurrão e golpes com acerto modificado (Beatdown e Blitz apareciam como 0%).

Fontes: [Into the Breach: clareza acima de ideias legais](https://gamedeveloper.com/design/-i-into-the-breach-i-dev-on-ui-design-sacrifice-cool-ideas-for-the-sake-of-clarity-every-time-), [Into the Breach: falha e telegrafia](https://www.gamedeveloper.com/design/reimagining-failure-in-strategy-game-design-in-i-into-the-breach-i-), [Tactics Ogre Reborn: novidades](https://www.square-enix-games.com/news/tactics-ogre-reborn-new-features), [Tactics Ogre Reborn: ajustes de equilíbrio](https://gematsu.com/2022/10/tactics-ogre-reborn-details-unit-development-charms-battle-updates-balance-adjustments-shop-improvements-classes-and-characters), [Triangle Strategy: dicas de batalha](https://www.nintendo.com/en-ca/whatsnew/tips-for-getting-started-with-triangle-strategy/), [Triangle Strategy: TP](https://nintendolife.com/guides/triangle-strategy-tips-and-battle-tactics-walkthrough-tactical-points-phases-kudos-quietuses-guide), [FFTA2 (TV Tropes)](https://www.tvtropes.org/pmwiki/pmwiki.php/VideoGame/FinalFantasyTacticsA2), [FFTA2 (Siliconera)](https://www.siliconera.com/final-fantasy-tactics-a2-polished-to-amazement/).
