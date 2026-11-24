# Ranking v3: progressão de habilidades por estoque da loja e AP acumulado

**Modelo:** a habilidade só existe se a arma que a ensina estiver no estoque (inicial; após 10 batalhas; após 20; depois) e se o AP acumulado (40 AP por batalha, 12 batalhas no nível 10, 40 no 25, 90 no 45) cobrir o custo; aprende-se do mais barato ao mais caro. **Não há mais corte "AP ≤ 100 no nível 10".** Estoque das armas: lista que você mandou (10 e 20 batalhas); armas não listadas contam como estoque inicial se custam ≤ 1.200 e como estoque tardio (após 35 batalhas) nas demais.
**Pacote avaliado:** R2 (classes e itens) + Gunner 6 MP + Cupid 8 MP + Phantasm 30 + Unicorn e Cura a 100 AP + Haste em área + Paladin (Nurse 45, Saint Cross 45/18 MP, Holy Blade 24 MP) + Elementalist (4 habilidades a 40) + magias tier 2 e 3 + First Aid 40 + Illusionist ×0,8 + orçamento +8% em Assassin, Fencer, Soldier, Mog Knight, Juggler, Red Mage.
Efeito na equipe (5 contra 5, mapa variável, 12.000 batalhas por nível, erro ≈ ±1): pontos percentuais que a equipe vence a mais por ter a classe. Tier: S ≥ +10, A +3 a +10, B −3 a +3, C −10 a −3, D < −10.

Desvio entre classes: original (neste modelo) 13.4 pp · R2 9.0 · **pacote 8.6** · (pacote no modelo antigo de AP: 7.4).

| # | classe | tier | pacote (10/25/45) | média | no modelo antigo (AP ≤ corte) | original neste modelo | R2 neste modelo | habilidades no nível 10 | confiança |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Summoner (Viera) | S | +31 / +10 / +8 | **+16.3** | +8.6 | +4.4 | +17.8 | 2 | alta |
| 2 | White Monk (Bangaa) | S | +15 / +10 / +7 | **+10.3** | +5.5 | +25.0 | +11.9 | 2 | alta |
| 3 | White Mage (Hume) | A | -2 / +7 / +13 | **+6.0** | +7.5 | +14.9 | +6.3 | 2 | alta |
| 4 | Mog Knight (Moogle) | A | +15 / -4 / +7 | **+5.9** | +1.2 | -2.7 | +2.1 | 2 | média |
| 5 | Soldier (Hume) | A | +14 / +2 / +0 | **+5.7** | +2.9 | -2.7 | -1.1 | 2 | alta |
| 6 | White Mage (Viera) | A | -5 / +6 / +16 | **+5.6** | +5.5 | +16.4 | +5.6 | 2 | alta |
| 7 | Dragoon (Bangaa) | A | +3 / +11 / +1 | **+4.8** | +5.3 | +12.0 | +5.5 | 2 | média |
| 8 | Black Mage (Moogle) | A | +3 / +8 / +3 | **+4.6** | +3.2 | -8.2 | +1.9 | 3 | alta |
| 9 | White Mage (Nu Mou) | A | -5 / +3 / +14 | **+4.0** | +4.8 | +14.4 | +4.7 | 2 | alta |
| 10 | Juggler (Moogle) | A | +19 / +1 / -8 | **+4.0** | -2.3 | +13.4 | +1.7 | 2 | alta |
| 11 | Red Mage (Viera) | A | +14 / +1 / -3 | **+3.9** | -0.3 | +5.2 | +0.5 | 2 | alta |
| 12 | Hunter (Hume) | A | -2 / -1 / +13 | **+3.3** | +1.0 | +12.6 | +3.6 | 0 | média |
| 13 | Warrior (Bangaa) | B | +16 / +2 / -9 | **+2.8** | +1.4 | -1.9 | +2.1 | 2 | alta |
| 14 | Illusionist (Hume) | B | +12 / -1 / -4 | **+2.5** | +1.4 | -14.7 | +12.1 | 3 | alta |
| 15 | Assassin (Viera) | B | -6 / +3 / +11 | **+2.5** | -1.2 | +15.5 | -0.0 | 1 | alta |
| 16 | Sage (Nu Mou) | B | -16 / +11 / +10 | **+1.8** | -0.5 | +6.0 | +3.1 | 0 | alta |
| 17 | Black Mage (Nu Mou) | B | -3 / +8 / +0 | **+1.7** | +0.6 | -7.0 | -1.7 | 3 | alta |
| 18 | Black Mage (Hume) | B | -2 / +5 / +2 | **+1.6** | +1.7 | -6.1 | -0.9 | 3 | alta |
| 19 | Illusionist (Nu Mou) | B | +8 / -1 / -4 | **+1.1** | +2.5 | -12.8 | +10.5 | 3 | alta |
| 20 | Alchemist (Nu Mou) | B | -19 / +12 / +10 | **+1.1** | -1.9 | -6.2 | +1.7 | 0 | alta |
| 21 | Gunner (Moogle) | B | -1 / -4 / +8 | **+0.9** | +2.1 | +15.3 | +1.5 | 1 | alta |
| 22 | Fencer (Viera) | B | +5 / -3 / -0 | **+0.6** | +2.6 | +5.6 | -2.6 | 1 | alta |
| 23 | Fighter (Hume) | B | -4 / +7 / -2 | **+0.2** | +3.5 | +4.7 | +1.5 | 2 | média |
| 24 | Gladiator (Bangaa) | B | -4 / +1 / +3 | **-0.0** | +1.6 | +5.6 | +4.3 | 2 | média |
| 25 | Elementalist (Viera) | B | +0 / +2 / -4 | **-0.4** | +1.8 | +2.3 | -1.0 | 1 | alta |
| 26 | Templar (Bangaa) | B | +0 / -1 / -1 | **-0.7** | +4.9 | -13.7 | -5.8 | 2 | média (Rasp, Soul Sphere, Lifebreak sem valor) |
| 27 | Archer (Viera) | B | +1 / -7 / +2 | **-1.2** | +0.0 | +8.3 | -0.4 | 2 | alta |
| 28 | Archer (Hume) | B | -3 / -5 / +4 | **-1.6** | -1.1 | +4.0 | -1.9 | 2 | alta |
| 29 | Animist (Moogle) | B | -6 / +5 / -4 | **-1.7** | -3.8 | +9.8 | -0.0 | 2 | alta |
| 30 | Time Mage (Nu Mou) | B | -0 / -3 / -5 | **-2.9** | -9.0 | -17.4 | -11.1 | 2 | alta |
| 31 | Beastmaster (Nu Mou) | C | +6 / -7 / -8 | **-3.1** | -1.7 | -7.6 | -2.2 | 2 | baixa (kit não modelado) |
| 32 | Ninja (Hume) | C | -5 / +0 / -6 | **-3.5** | -3.3 | +12.4 | -0.7 | 2 | alta |
| 33 | Bishop (Bangaa) | C | -16 / +4 / +1 | **-3.7** | +8.0 | -10.2 | -2.8 | 1 | alta |
| 34 | Time Mage (Moogle) | C | -4 / -5 / -5 | **-4.5** | -8.3 | -18.2 | -10.8 | 2 | alta |
| 35 | Gadgeteer (Moogle) | C | +3 / -8 / -8 | **-4.6** | -4.7 | -13.0 | -3.1 | 2 | baixa (kit não modelado) |
| 36 | Sniper (Viera) | C | -2 / -6 / -7 | **-5.0** | -3.7 | +7.0 | -3.8 | 0 | média |
| 37 | Defender (Bangaa) | C | -22 / +2 / +0 | **-6.5** | +3.7 | -3.1 | -3.3 | 2 | média |
| 38 | Paladin (Hume) | C | -20 / -1 / -0 | **-6.9** | -0.1 | -10.9 | -9.7 | 2 | média |
| 39 | Blue Mage (Hume) | C | -1 / -15 / -13 | **-9.7** | -7.4 | -13.3 | -7.8 | 0 | baixa (kit não modelado) |
| 40 | Thief (Hume) | D | -2 / -17 / -11 | **-10.0** | -8.4 | -12.7 | -7.5 | 2 | baixa (kit não modelado) |
| 41 | Thief (Moogle) | D | -6 / -14 / -14 | **-11.4** | -11.1 | -14.4 | -8.5 | 2 | baixa (kit não modelado) |
| 42 | Morpher (Nu Mou) | D | -8 / -18 / -16 | **-13.8** | -12.3 | -18.1 | -11.7 | 0 | baixa (kit não modelado) |

Tiers S/A/B/C/D: original 10/10/4/6/12 · pacote 2/10/18/9/3 · pacote no modelo antigo 0/11/21/8/2.