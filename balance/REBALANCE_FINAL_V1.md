# Rebalance FINAL v1 — FFTA (GBA), somente dados

Patches em `final_v1/` (como aplicar: `final_v1/LEIA-ME.md`). Nenhuma rotina do jogo foi alterada: só valores das tabelas de classes, itens e habilidades, e IDs de efeito que o jogo já usa em outras habilidades.

## 1. O que muda

### bal20 — classes (42 classes)
- Base: ajuste de orçamento por classe (F1 k5) com ATK/PM ×1,12 (acompanha a compressão das armas raras).
- Velocidade comprimida em torno de 100 (×0,7 da distância). Evade comprimido em torno de 50 (×0,6). Exemplo: Assassin vai de Vel 125 para 118 e de Evade 65 para 59.
- Ajustes desta versão:
  - Templar ×0,90 (era S por causa do Haste).
  - Time Mage ×0,85 (o pacote anterior dava +50% de PM e crescimento 16).
  - Alchemist ×0,92.
  - Paladin ×1,10.
  - Fencer ×1,12.
  - Archer, Ninja e Sniper ×1,08.
  - Fighter e Defender ×1,05.
  - Illusionist ×0,85 (com o Phantasm mais forte).
- Classes cujo kit o simulador não modela (Blue Mage, Thief, Morpher, Beastmaster, Gadgeteer) recebem só o ajuste global, sem orçamento próprio. Não há base para mexer nelas.

### bal21 — itens (176 itens)
- Armas de saque acima de 45 de ATK são comprimidas (45 + 0,55 do excesso). Exemplos: Excalibur2 87→68, Ebon Blade 84→66.
- Armaduras do topo ficam até ×3 em DEF/RES (curva convexa). As fracas quase não mudam.
- Escudos ganham Evade ×2.
- Preços crescentes com o ATK dentro de cada tipo, para que não haja arma dominada.

### bal22 — habilidades (47 habilidades)
| Grupo | Mudança |
|---|---|
| Rodada 8 (fracas → viáveis) | Earth Render 39, Far Fist 40, Air Render 52, Body Slam 52, Tremor 34, Whirlwind 29, Holy 57/26 MP, Water e Aero 39/10, Chocobo Rush 52/10, White Flame 19 MP, Cuisine 26, Sheep Count 6, Nightmare 14, Ague 10, Carbuncle 10, Tail Wag 6, Quicken 19 |
| Área raio 1 (Rodada 9) | Toad (MP 36 mantido), Provoke, Downsize, Ague, Oblivion, Heavy Dust, Sliprain, Shining Air (40 de poder, 10 MP), Cuisine, Quicken |
| Paladin | Nurse 45, Saint Cross 45/18 MP, Holy Blade 24 MP |
| Outras | First Aid 40, Fire Whip 40, Phantasm (8 invocações do Illusionist) 30, Unicorn e Cura 100 AP |
| Tiros de status (Gunner) e Cupid | 4 MP e 8 MP (eram gratuitos) |
| Assassin | Rockseal 32→40 MP; Last Breath fica no original (32) |
| Haste | Mantido como no original: alvo único, 24 MP. A área em Haste foi testada e descartada |

### bal23 — magias (identidade do trio)
| Elemento | Papel | Poder (t1/t2/t3) | MP | Efeito novo |
|---|---|---|---|---|
| Fogo | dano bruto | 33 / 51 / 75 | 6 / 14 / 30 | — |
| Gelo | controle | 24 / 37 / 54 | 6 / 14 / 30 | Slow se o dano acertar (ID 103, o mesmo do Sliprain) |
| Raio | ritmo | 27 / 41 / 61 | 6 / 14 / 30 | atrasa o turno se o dano acertar (ID 27, o mesmo do Hand Slap) |

Original: 30/40/50 com 6/12/24 MP para os três. Os tiers 2 e 3 já tinham ficado mais fortes e mais caros nas rodadas anteriores.

No nível 25, o Black Mage passa a usar Firaga 42%, Blizzara 24%, Thundaga 22% e Blizzard 6,5%. Antes, Thundaga ficava com 67% só por empate. No nível 45, Blizzaga lidera com 26%.

## 2. Resultado (5v5, mapa variável, progressão real; efeito da classe na equipe em pp)
| Versão | nível 10: σ / máx | nível 25: σ / máx | nível 45: σ / máx |
|---|---|---|---|
| Pacote anterior + R8 + área (F0) | 10,5 / +34 | 8,8 / +17 | 7,6 / +14 |
| **Final v1 (F3)** | **8,5 / +19** | **8,3 / +14** | **6,5 / +12** |

Ablação (nível 25, contra F0):
- Haste de volta ao original: σ 9,0 → 8,3.
- Ajustes de orçamento: Fighter +8,5, Paladin +5,5, Illusionist +6 a +8, Time Mage −13, Templar −10.
- Trio: Black Mage −5 a +5 (inconclusivo); Red Mage voltou ao centro sem o +8%.

Robustez:
- Outra semente: correlação 0,98 entre as duas rodadas, diferença média de 1,2 pp por classe.
- Secundário só de pré-requisito: σ 8,8 no nível 25. O ranking muda nas classes que dependem do secundário (Blue Mage, Thief/Moogle, Paladin), como já se sabia.

Ranking final (média dos níveis):
- Topo: Blue Mage +11 (kit não modelado, baixa confiança) e Templar +8. Depois Elementalist, Warrior, Black Mage/Moogle, White Monk e White Mage, entre +6 e +7.
- Fundo:
  - Paladin −10, ainda fraco no simulador.
  - Thief, Morpher, Gadgeteer e Beastmaster: kits não modelados, então o número não é confiável.

## 3. Avaliação da análise externa (o que entrou e o que não)
| Proposta | Decisão |
|---|---|
| Assassin OP (Move/Jump/Evade, Rockseal, Last Breath) | Parcial. Velocidade e Evade já comprimidos, Rockseal +8 MP, Last Breath sem desconto. Move e Jump ficam iguais: com o pacote, a Assassin ficou no centro (−0,1). Precisão não é campo da habilidade (exige ASM) |
| Dragonheart uma vez por batalha | Não: exige ASM |
| Sage sem escudo, Giga Flare mais fraco | Não. O Sage está no centro (+4), e a tabela de equipamento não foi confirmada nesta ROM |
| Doublecast com MP dobrado | Não: exige ASM |
| Summoner com menos dano | Não. Ele está em +4; a força dele vem do Unicorn e do Fire Whip |
| Morpher (teto de atributos) | Não: exige ASM |
| Night / sono mais curto | Não. A duração de status é global, não por habilidade |
| Ultima Shot / Holy Blade / Concentrate / Double Sword | Holy Blade fica mais barato (o Paladin é a pior classe). Os outros exigem ASM ou não se justificam: Hunter está em +1 |
| Prioridade Fighter, Ninja, Archer, White Mage | Sim, por orçamento (White Mage já está bem) |
| Templar com menos ataque | Sim (×0,90 e Haste original) |
| Defender melhor | Sim (+5%) |
| Bishop mais rápido | Indireto: a compressão de Velocidade leva o Bishop de 88 para 92 |
| Beastmaster com controle mais longo | Não: duração global / ASM |

## 4. Limitações conhecidas
- O simulador não modela roubo, transformação, Blue Magic, os efeitos aleatórios do Gadgeteer nem Doublecast. Para essas classes, vale o que você observar jogando.
- O simulador quase não sente falta de MP. Custos (Rockseal 40, tiros 4) pesam mais no jogo real.
- O Haste continua a melhor escolha do Templar e do Time Mage (cerca de 65% das ações), como no jogo original.
- As descrições das magias no jogo não mencionam o Slow e o atraso novos.
- Fórmula do Combo, duração do Charm, Dragonheart e Doublecast ficam fora (exigem ASM).
