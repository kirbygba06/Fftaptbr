# Rodada 3: equipes de 5, mapa variável, efeito por equipe e melhoria das classes fracas

Dados: `exp3_result.md` (tabelas), `abilidades_uso_5v5.csv` (todas as habilidades de todas as classes), `exp3_team_*.json`, `exp3_fix_raw.json`, `exp3_tm_raw.json`, `exp3_haste.json`, `exp3_haste_area.json`. Código: `exp3.py`, `exp3_fix.py`, `exp3_tm.py`, `exp3_haste*.py`, `exp3_report.py`.

## 1. O que mudou no simulador
- **5 contra 5** (era 3 contra 3).
- **Mapa variável (conservador):** distância inicial entre as frentes sorteada de 4 a 7 casas em 75% das lutas e de 10 a 13 em 25% ("mapas grandes às vezes"). Quem não alcança o alvo (Mov + alcance < distância) gasta o turno andando; a distância cai conforme as unidades avançam. Habilidades de cura e buff não dependem da distância.
- **Efeito por equipe:** regressão logística sobre 12.000 batalhas por nível, com a presença de cada classe nos dois times. O número é "quantos pontos percentuais a equipe que tem a classe vence a mais do que com uma classe média no lugar" (erro ≈ ±1 ponto). Usa cada batalha para as 10 classes envolvidas, então é bem mais preciso que o duelo individual.
- **Habilidades menos usadas:** valor esperado médio de cada habilidade quando disponível (mesmo as não escolhidas), % das vezes em que foi a melhor opção, e valor relativo à melhor da classe. Nada é chamado de inútil só por não ser escolhido.
- **Haste:** medi o ganho realizado por Haste (turnos extras do aliado) contra o que a IA do simulador estima.

## 2. Efeito de cada classe na equipe (níveis 10 / 25 / 45, em pontos percentuais)
| | desvio entre classes | classes com efeito > ±3 pp | ações por batalha |
|---|---|---|---|
| Original | 13,1 / 13,8 / 13,8 | 39 / 36 / 34 | 85 / 68 / 70 |
| R2 (classes+itens+Gunner) | 9,1 / 9,1 / 7,4 | 27 / 32 / 29 | 73 / 62 / 69 |
| Original + pacote de correções (seção 4) | 9,5 / 12,8 / 12,7 | 33 / 35 / 32 | 90 / 65 / 67 |
**As piores para a equipe (original):** Time Mage (−32/−18/−18 e −30/−17/−17), Morpher (−14/−16/−19), Thief Moogle (−10/−16/−17), Blue Mage (−7/−15/−18), Illusionist (−5/−15/−18), Gadgeteer, Templar (−5/−13/−14), e no nível 10 Bishop e Summoner (−29).
**As melhores:** White Monk (+10/+37/+18), White Mage nas três raças (+7 a +26), Gunner (+22/+17/+23), Dragoon (+14/+24/+8), Defender (+15/+17/+6), Hunter (+12/+12/+17).
Com 5 unidades e mapa variável o jogo fica **mais** desigual por equipe do que o duelo 3×3 sugeria (13 pp de desvio): curandeiros e controladores de status brilham, quem depende de chegar perto sofre nos mapas grandes. O R2 reduz o desvio para 7–9 pp, mas **inverte** o Illusionist (+26/+15/+5) porque foi ajustado por atributos para compensar o kit.

## 3. Habilidades menos usadas
Das 266 combinações classe-habilidade medidas no nível 45, **137 (52%) são escolhidas em menos de 2% das vezes em que estão disponíveis**. A maioria é redundante ou não modelada. Só 8 têm valor ≥60% do da melhor habilidade da classe e mesmo assim são ignoradas: Fire/Thunder/Blizzard do Black Mage (tier 1 superado), Toad (Alchemist), Sheep Count (Animist), Nightmare (Assassin), Swallowtail (Fencer), Rush (Fighter).
Nas classes fracas:
- **Time Mage**: Quicken, Slow, Reflect, Quarter, Demi, Silence (0,2 a 2% cada; valor 15–39% do melhor). **Haste concentra 65–78% das escolhas**.
- **Illusionist**: antes, só 3 das 8 Phantasm eram usadas (Prominence, Freezeblink, Stardust); as demais (Tempest, Deluge, Soil Evidence, Wild Tornado, Star Cross) têm poder 17 por 32 MP.
- **Templar**: Astra, Warcry, Silence, e **Rasp, Soul Sphere e Lifebreak sem efeito modelado**. O Haste é escolhido em 91% das vezes disponíveis.
- **Summoner**: Carbuncle (0,5%, valor 40%), Ramuh e Shiva (70% do valor, 2–3%).
- **Bishop**: Dispel, Judge (sem efeito modelado), Barrier, Aero, Water (valor ≈25% do Break).

## 4. Testes de melhoria (estratificado, 5 contra 5, mapa variável, 2.000 batalhas por ponto; Δ vs original; < 5 pontos não é conclusivo)
| mudança (só dado) | classe | nível 10 | 25 | 45 | leitura |
|---|---|---|---|---|---|
| **Phantasm: poder 17–20 → 30** | Illusionist (Hume / Nu Mou) | +11 / +9 | +7 / +7 | +5 / +8 | conclusivo; reativa 5 habilidades que ninguém usava (uso passa de 3 → 6–8 Phantasm com 12–16% cada) |
| Phantasm: MP 32 → 24 | Illusionist | +2 / 0 | +1 / −1 | +1 / −1 | **sem efeito**: o problema é poder, não custo |
| Phantasm poder 30 e MP 24 | Illusionist | +11 / +10 | +8 / +8 | +7 / +6 | MP não soma |
| **Unicorn e Cura a 100 AP** | Summoner / Bishop | **+16 / +15** | 0 / 0 | 0 / 0 | conclusivo e só no início, sem tocar nos níveis altos |
| Piso de velocidade (+10 base, +0,3 cresc.) nas 5 classes lentas | Illusionist, Templar, Sage, Bishop, Summoner | +4 a +6 | +2 a +6 | +1 a +5 | no limite do ruído; só se quiser |
| Haste MP 16 / AP 100 / ambos | Time Mage | 0 a +6 (só nível 10 com AP 100) | 0 a +1 | −1 a 0 | **não resolve** |
| Stop MP 16; Demi 16 e Quarter 6; +15% HP/DEF; combinação | Time Mage | 0 a +1 | −0 a +4 | −2 a +2 | **não resolve**: o problema do Time Mage não é custo nem bulk |
| **Haste em área (raio 1)** | Time Mage (Nu Mou / Moogle), Templar | 0 | +8 / +6, +6 | +4 / +9, +5 | **conclusivo** (benefício coletivo, como você pediu) |
| Haste em área (raio 1) e dura 4 | idem | 0 | +8 / +8, +10 | +7 / +11, +7 | |
| Haste em área (raio 2) | idem | 0 | +9 / +12, +12 | +9 / +14, +10 | mais forte; verificar se não ultrapassa |
| **Pacote (Phantasm 30/24, Haste 16/AP100, Unicorn/Cura AP100, piso de velocidade)** | Illusionist | +17 / +16 | +14 / +13 | +10 / +10 | |
| | Summoner / Bishop | +19 / +16 | +4 / +7 | +2 / +3 | |
| | Time Mage, Templar, Sage | 0 a +3 | −1 a +3 | −2 a +3 | **não melhoram** (falta o Haste em área) |
No nível de equipe, o pacote leva o **Illusionist** de −5/−15/−18 para +13/+3/−4 pp, e Bishop e Summoner do nível 10 de −29 para −2/+1.
**Valor realizado do Haste**: a IA do simulador estima ~260 por cast; o ganho realizado (turnos extras) é **57 no nível 25 e 123 no 45**. A IA superestima o Haste 2–4 vezes e por isso o Time Mage fica 65–78% das ações nele. Trocar quanto a IA valoriza Haste (×0,5, ×0,25) ou removê-lo **não muda a vitória do Time Mage (37–42%)**: o Haste, como está, é neutro. É o motivo da melhora com área: o ganho passa a multiplicar por 2 a 3 aliados.

## 5. O que recomendo (Fase 1, uma por vez, cada uma com CSV e reversão)
1. **Phantasm poder 17–20 → 30** (8 registros): Illusionist +5 a +11, uso das habilidades diversificado.
2. **Unicorn e Cura a 100 AP** (2 registros): corrige o início do Summoner e do Bishop.
3. **Haste em área raio 1** (1 registro): Time Mage +4 a +9, Templar +5 a +6. **Risco:** o simulador só acerta aliados; no jogo a área "Default" pode hastear inimigos adjacentes. Testar em jogo antes de aprovar.
4. Piso de velocidade: opcional.
**Não resolvidos:** Time Mage no nível 10 (30%, sem habilidade), Templar (Rasp, Soul Sphere, Lifebreak sem modelo), Morpher, Thief, Blue Mage, Gadgeteer (kits não modelados).
**Não mexer:** MP de Phantasm, Haste, Stop e Demi (sem efeito medido).

## 6. Limites
- O mapa é uma distância única entre as frentes, sem altura, obstáculos nem flanqueamento.
- Os melhores números por equipe dependem de a IA do simulador escolher bem; a medição de Haste mostra que ela erra um pouco.
- Nada foi jogado. Haste em área precisa de confirmação de que a área não atinge inimigos.
