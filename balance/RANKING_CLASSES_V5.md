# Ranking v5: conjunto secundário realista, 16 batalhas no nível 10, 40 AP por batalha

**Modelo:** loja inicial real (24 armas) + listas de 10 e 20 batalhas; classes só existem após dominar os pré-requisitos (por raça); 40 AP por batalha; **16 batalhas no nível 10** (você chega às 20 entre o 10 e o 15), 40 no 25 e 90 no 45. **Conjunto secundário:** até o nível 15 é o de pré-requisito; depois é escolhido o mais útil entre as classes que a unidade pode usar (valor esperado medido das 3 melhores habilidades), com **preferência forte por não misturar físico e mágico** (peso 0,4 no tipo diferente; White Mage é exceção por ser suporte).
**Mistura físico×mágico:** com o peso 0,4, 18 das 84 escolhas de secundário (classe × nível 25/45) misturam os tipos (ex.: Fighter, Paladin, Mog Knight, Juggler com Black Mage); a coluna "sem mistura" refaz a simulação proibindo isso quando há alternativa.

**Pacote avaliado:** R2 (classes e itens) + Gunner 6 MP + Cupid 8 MP + Phantasm 30 + Unicorn e Cura a 100 AP + Haste em área + Paladin (Nurse 45, Saint Cross 45/18, Holy Blade 24) + Elementalist (4 habilidades a 40) + magias tier 2 e 3 + First Aid 40 + Illusionist ×0,8 + orçamento +8% em Assassin, Fencer, Soldier, Mog Knight, Juggler, Red Mage.
Efeito na equipe (5 contra 5, mapa variável, 12.000 batalhas por nível, erro ≈ ±1): pontos percentuais que a equipe vence a mais por ter a classe; média só dos níveis em que a classe existe. Tier: S ≥ +10, A +3 a +10, B −3 a +3, C −10 a −3, D < −10.

Desvio entre classes: original 12.4 pp · R2 8.7 · **pacote 8.7** · só pré-requisito como secundário 9.0 · sem secundário 8.3.

| # | classe | tier | pacote (10/25/45) | média | 1º nível em que existe (AP de pré-requisito) | secundário 10 / 25 / 45 | habilidades de ação 10/25/45 | original | R2 | só pré-req. como secundário (posto) | sem secundário (posto) | sem mistura físico×mágico (posto) | confiança |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Blue Mage (Hume) | S | +27 / +14 / +11 | **+17.4** | 10 (200 AP) | White Mage / Black Mage / Black Mage | 1 / 5 / 9 | +3.6 | +16.5 | +10.1 (#5) | -8.8 (#38) | +17.3 (#1) | baixa (kit não modelado) |
| 2 | Templar (Bangaa) | S | +30 / +15 / +4 | **+16.4** | 10 (300 AP) | White Monk / White Monk / White Monk | 4 / 9 / 15 | +0.6 | +15.8 | +13.9 (#1) | +0.4 (#21) | +17.0 (#2) | média (Rasp, Soul Sphere, Lifebreak sem valor) |
| 3 | Time Mage (Nu Mou) | S | n/d / +16 / +12 | **+14.1** | 25 (700 AP) | – / Black Mage / Black Mage | – / 9 / 16 | -15.4 | +10.4 | +13.3 (#2) | -3.3 (#32) | +14.4 (#3) | alta |
| 4 | Time Mage (Moogle) | S | n/d / +14 / +9 | **+11.7** | 25 (700 AP) | – / Black Mage / Black Mage | – / 9 / 16 | -17.0 | +3.9 | +11.0 (#3) | -3.9 (#34) | +11.7 (#4) | alta |
| 5 | Alchemist (Nu Mou) | A | n/d / +10 / +9 | **+9.7** | 25 (1200 AP) | – / Black Mage / Black Mage | – / 8 / 13 | -7.0 | +7.6 | +10.8 (#4) | -4.4 (#35) | +9.0 (#5) | alta |
| 6 | White Mage (Hume) | A | -2 / +6 / +15 | **+6.2** | 10 (0 AP) | – / Soldier / Black Mage | 3 / 8 / 16 | +11.6 | +5.5 | +7.1 (#6) | +7.1 (#4) | +5.6 (#7) | alta |
| 7 | Sage (Nu Mou) | A | n/d / +10 / +2 | **+6.1** | 25 (900 AP) | – / White Mage / Black Mage | – / 7 / 11 | +10.6 | +4.3 | +7.0 (#7) | +1.5 (#18) | +7.0 (#6) | alta |
| 8 | Summoner (Viera) | A | n/d / +5 / +6 | **+5.1** | 25 (600 AP) | – / Elementalist / Elementalist | – / 7 / 14 | -4.8 | +8.0 | +6.7 (#9) | +9.0 (#1) | +5.2 (#8) | alta |
| 9 | Warrior (Bangaa) | A | +6 / -1 / +9 | **+4.6** | 10 (0 AP) | – / White Monk / White Monk | 3 / 8 / 14 | +3.3 | +6.5 | -1.0 (#26) | +4.8 (#10) | +4.1 (#10) | alta |
| 10 | White Mage (Nu Mou) | A | -4 / +5 / +13 | **+4.5** | 10 (0 AP) | – / Black Mage / Black Mage | 3 / 8 / 16 | +10.8 | +2.5 | +4.0 (#14) | +4.6 (#11) | +4.0 (#11) | alta |
| 11 | Elementalist (Viera) | A | +3 / +1 / +7 | **+4.0** | 10 (200 AP) | Fencer / White Mage / White Mage | 3 / 8 / 17 | +11.9 | +4.4 | +1.0 (#21) | +2.5 (#16) | +4.2 (#9) | alta |
| 12 | Black Mage (Moogle) | A | +8 / +9 / -5 | **+3.6** | 10 (0 AP) | – / Animist / Animist | 4 / 9 / 16 | -9.9 | -2.4 | +5.2 (#12) | +8.7 (#2) | +3.0 (#14) | alta |
| 13 | Juggler (Moogle) | B | +16 / +3 / -10 | **+2.7** | 10 (300 AP) | Thief / Black Mage / Black Mage | 4 / 8 / 16 | +12.2 | -0.0 | +3.5 (#15) | +3.8 (#13) | +3.2 (#13) | alta |
| 14 | Red Mage (Viera) | B | +6 / -1 / +2 | **+2.4** | 10 (100 AP) | Fencer / White Mage / White Mage | 4 / 7 / 13 | +5.5 | -1.6 | -0.8 (#25) | +3.4 (#14) | +2.5 (#15) | alta |
| 15 | Black Mage (Hume) | B | +6 / +2 / -2 | **+2.2** | 10 (0 AP) | – / White Mage / White Mage | 4 / 9 / 16 | -5.0 | +0.8 | +3.4 (#16) | +6.0 (#5) | +2.5 (#16) | alta |
| 16 | White Mage (Viera) | B | -6 / +4 / +8 | **+2.1** | 10 (0 AP) | – / Archer / Archer | 3 / 8 / 15 | +12.1 | +2.8 | +4.9 (#13) | +5.5 (#7) | +1.1 (#19) | alta |
| 17 | Dragoon (Bangaa) | B | +1 / +6 / -1 | **+2.0** | 10 (300 AP) | Warrior / Warrior / White Monk | 4 / 8 / 14 | +14.7 | +4.4 | +2.9 (#17) | +4.5 (#12) | +1.7 (#17) | média |
| 18 | White Monk (Bangaa) | B | +4 / +8 / -6 | **+1.9** | 10 (0 AP) | – / Warrior / Warrior | 3 / 8 / 16 | +18.5 | +5.2 | +6.8 (#8) | +8.7 (#3) | +1.4 (#18) | alta |
| 19 | Gladiator (Bangaa) | B | -4 / +4 / +4 | **+1.7** | 10 (300 AP) | Warrior / Warrior / White Monk | 4 / 9 / 12 | +8.7 | +1.9 | +0.6 (#22) | +1.7 (#17) | +1.0 (#20) | média |
| 20 | Black Mage (Nu Mou) | B | +3 / +3 / -2 | **+1.4** | 10 (0 AP) | – / White Mage / White Mage | 4 / 9 / 16 | -5.5 | -0.5 | +1.7 (#18) | +5.0 (#9) | +0.8 (#21) | alta |
| 21 | Mog Knight (Moogle) | B | +11 / -11 / +1 | **+0.2** | 10 (100 AP) | Animist / Black Mage / Black Mage | 3 / 8 / 12 | -5.5 | -2.0 | +5.4 (#11) | +5.1 (#8) | +3.8 (#12) | média |
| 22 | Assassin (Viera) | B | n/d / -3 / +3 | **-0.2** | 25 (800 AP) | – / White Mage / Elementalist | – / 5 / 10 | +18.7 | -2.0 | +5.7 (#10) | +0.9 (#20) | +0.4 (#22) | alta |
| 23 | Hunter (Hume) | B | -1 / -7 / +8 | **-0.2** | 10 (300 AP) | Archer / White Mage / Black Mage | 2 / 7 / 11 | +12.1 | +1.1 | +1.3 (#19) | +2.7 (#15) | -0.6 (#23) | média |
| 24 | Bishop (Bangaa) | B | +0 / +3 / -7 | **-1.3** | 10 (300 AP) | White Monk / White Monk / White Monk | 3 / 8 / 15 | -10.7 | +0.9 | +1.3 (#20) | -2.2 (#29) | -2.5 (#25) | alta |
| 25 | Soldier (Hume) | B | +6 / -6 / -7 | **-2.5** | 10 (0 AP) | – / White Mage / Archer | 3 / 8 / 14 | -5.7 | -6.2 | +0.2 (#23) | +5.6 (#6) | -1.3 (#24) | alta |
| 26 | Illusionist (Hume) | C | n/d / -3 / -4 | **-3.2** | 25 (1200 AP) | – / Black Mage / Black Mage | – / 8 / 15 | -16.0 | +8.4 | -3.1 (#28) | -1.8 (#28) | -4.1 (#28) | alta |
| 27 | Fencer (Viera) | C | -2 / -4 / -4 | **-3.3** | 10 (0 AP) | – / White Mage / Archer | 1 / 8 / 15 | +1.8 | -6.1 | -3.1 (#29) | -0.9 (#23) | -3.6 (#27) | alta |
| 28 | Animist (Moogle) | C | -5 / +2 / -9 | **-4.1** | 10 (0 AP) | – / Black Mage / Black Mage | 3 / 9 / 17 | +6.3 | -3.5 | -1.9 (#27) | -1.2 (#24) | -4.4 (#29) | alta |
| 29 | Illusionist (Nu Mou) | C | n/d / -4 / -5 | **-4.4** | 25 (1200 AP) | – / Black Mage / Black Mage | – / 8 / 15 | -16.0 | +5.6 | -3.5 (#30) | -0.8 (#22) | -5.8 (#35) | alta |
| 30 | Defender (Bangaa) | C | -16 / +5 / -2 | **-4.6** | 10 (300 AP) | Warrior / Warrior / White Monk | 3 / 9 / 15 | -1.8 | -3.7 | -5.2 (#33) | -3.2 (#31) | -4.5 (#30) | média |
| 31 | Fighter (Hume) | C | -5 / +3 / -12 | **-4.6** | 10 (300 AP) | Soldier / Black Mage / Archer | 4 / 8 / 14 | +2.0 | -2.7 | -0.5 (#24) | +1.5 (#19) | -4.7 (#31) | média |
| 32 | Archer (Hume) | C | -9 / -8 / +2 | **-5.0** | 10 (0 AP) | – / White Mage / White Mage | 3 / 8 / 15 | +0.4 | -3.8 | -4.8 (#32) | -3.1 (#30) | -5.0 (#33) | alta |
| 33 | Archer (Viera) | C | -7 / -11 / +3 | **-5.0** | 10 (0 AP) | – / Fencer / White Mage | 3 / 8 / 15 | +3.4 | -2.6 | -5.5 (#34) | -1.7 (#27) | -5.7 (#34) | alta |
| 34 | Ninja (Hume) | C | -11 / -1 / -4 | **-5.2** | 10 (300 AP) | Thief / Soldier / White Mage | 4 / 7 / 10 | +9.6 | -4.5 | -5.8 (#35) | -1.6 (#26) | -5.9 (#36) | alta |
| 35 | Beastmaster (Nu Mou) | C | +2 / -13 / -7 | **-5.7** | 10 (0 AP) | – / Black Mage / Black Mage | 3 / 8 / 18 | -13.5 | -6.4 | -6.1 (#36) | -3.4 (#33) | -6.0 (#37) | baixa (kit não modelado) |
| 36 | Gadgeteer (Moogle) | C | -4 / -15 / +1 | **-6.0** | 10 (300 AP) | Thief / Black Mage / Black Mage | 3 / 7 / 16 | -14.8 | -6.0 | -8.8 (#38) | -5.2 (#37) | -4.9 (#32) | baixa (kit não modelado) |
| 37 | Gunner (Moogle) | C | -12 / -8 / -1 | **-6.8** | 10 (100 AP) | Animist / Animist / Black Mage | 3 / 10 / 17 | +5.6 | -3.3 | -3.8 (#31) | -1.3 (#25) | -6.9 (#38) | alta |
| 38 | Sniper (Viera) | C | -5 / -8 / -8 | **-6.9** | 10 (300 AP) | Archer / Fencer / Archer | 2 / 6 / 15 | +3.9 | -5.2 | -6.3 (#37) | -5.0 (#36) | -8.3 (#39) | média |
| 39 | Thief (Moogle) | C | -11 / -8 / -3 | **-7.2** | 10 (0 AP) | – / Animist / Black Mage | 3 / 9 / 17 | -12.1 | -5.6 | -14.4 (#41) | -11.0 (#41) | -3.4 (#26) | baixa (kit não modelado) |
| 40 | Thief (Hume) | C | -7 / -6 / -15 | **-9.4** | 10 (0 AP) | – / White Mage / Archer | 3 / 9 / 16 | -11.5 | -7.3 | -11.9 (#39) | -10.3 (#40) | -8.6 (#40) | baixa (kit não modelado) |
| 41 | Morpher (Nu Mou) | D | n/d / -20 / -3 | **-11.4** | 25 (1000 AP) | – / Black Mage / Black Mage | – / 3 / 14 | -21.5 | -13.3 | -18.9 (#42) | -16.5 (#42) | -12.7 (#41) | baixa (kit não modelado) |
| 42 | Paladin (Hume) | D | -18 / -11 / -13 | **-14.1** | 10 (300 AP) | Soldier / Black Mage / Archer | 3 / 8 / 14 | -17.1 | -16.7 | -12.6 (#40) | -9.9 (#39) | -13.8 (#42) | média |

Tiers S/A/B/C/D: original 10/9/5/7/11 · pacote 4/8/13/15/2.
Correlação de postos: com secundário escolhido × só pré-requisito 0.91; × sem secundário 0.49; × sem mistura físico×mágico 0.97.