## 1. Efeito de cada classe na EQUIPE (5 contra 5, mapa variável)
Regressão logística: a equipe que tem a classe vence quantos pontos percentuais a mais do que com uma classe média no lugar. Barra de erro ≈ ±1,0 ponto.

- **Original**: desvio do efeito por classe 13.1 / 13.8 / 13.8 pp; classes com efeito > ±3 pp: 39 / 36 / 34; ações por batalha 85 / 68 / 70
- **R2 (classes+itens+Gunner)**: desvio do efeito por classe 9.1 / 9.1 / 7.4 pp; classes com efeito > ±3 pp: 27 / 32 / 29; ações por batalha 73 / 62 / 69
- **Original + pacote de correções**: desvio do efeito por classe 9.5 / 12.8 / 12.7 pp; classes com efeito > ±3 pp: 33 / 35 / 32; ações por batalha 90 / 65 / 67

| classe | Original 10/25/45 (pp) | R2 | Original + correções |
|---|---|---|---|
**Piores 12 (efeito médio no original)**
| Time Mage (Nu Mou) | -32 / -18 / -18 | -19 / -10 / -12 | -21 / -17 / -18 |
| Time Mage (Moogle) | -30 / -17 / -17 | -17 / -12 / -10 | -21 / -15 / -19 |
| Morpher (Nu Mou) | -14 / -16 / -19 | -5 / -14 / -15 | -15 / -20 / -21 |
| Thief (Moogle) | -10 / -16 / -17 | -2 / -12 / -10 | -12 / -18 / -20 |
| Blue Mage (Hume) | -7 / -15 / -18 | -1 / -10 / -10 | -10 / -14 / -18 |
| Illusionist (Hume) | -5 / -15 / -18 | +26 / +15 / +5 | +13 / +3 / -4 |
| Illusionist (Nu Mou) | -5 / -12 / -19 | +24 / +14 / +3 | +14 / +5 / -4 |
| Gadgeteer (Moogle) | -5 / -16 / -16 | +6 / -3 / -7 | -9 / -14 / -16 |
| Templar (Bangaa) | -5 / -13 / -14 | +9 / -4 / -6 | -4 / -11 / -12 |
| Bishop (Bangaa) | -29 / +0 / -4 | -16 / +10 / +3 | +1 / +5 / +1 |
| Summoner (Viera) | -29 / +0 / -2 | -20 / +10 / +8 | -2 / +3 / +2 |
| Thief (Hume) | -4 / -11 / -14 | +2 / -10 / -9 | -8 / -13 / -14 |

**Melhores 8**
| classe | Original | R2 | Original + correções |
|---|---|---|---|
| Defender (Bangaa) | +15 / +17 / +6 | +5 / +14 / +1 | +9 / +17 / +1 |
| Hunter (Hume) | +12 / +12 / +17 | -3 / +2 / +7 | +6 / +11 / +16 |
| White Mage (Hume) | +7 / +14 / +24 | -1 / +6 / +15 | +13 / +14 / +23 |
| Dragoon (Bangaa) | +14 / +24 / +8 | +5 / +17 / +3 | +8 / +23 / +7 |
| White Mage (Nu Mou) | +9 / +12 / +26 | -3 / +6 / +13 | +14 / +13 / +25 |
| White Mage (Viera) | +14 / +18 / +26 | +0 / +9 / +10 | +13 / +12 / +23 |
| Gunner (Moogle) | +22 / +17 / +23 | -0 / +5 / +12 | +13 / +13 / +18 |
| White Monk (Bangaa) | +10 / +37 / +18 | -1 / +18 / +11 | +4 / +33 / +17 |

## 2. Habilidades menos usadas por classe (nível 45; escolhida = % das vezes em que estava disponível e foi a melhor opção; valor = valor esperado médio quando disponível, em % da melhor habilidade da classe)
| classe | habilidades menos escolhidas (escolhida%, valor%) |
|---|---|
| Alchemist | Rasp (0%, -1%); Poison (0%, 45%); Toad (2%, 60%) |
| Animist | Friend (0%, -1%); Catnip (0%, 13%); Sheep Count (2%, 73%) |
| Archer | Burial (0%, 0%); Blackout (0%, 34%); Aim: Legs (1%, 39%) |
| Assassin | Ague (0%, 14%); Aphonia (0%, 15%); Oblivion (0%, 23%) |
| Beastmaster | Bomb (0%, 0%); Bug (0%, 0%); Dragon (0%, 0%) |
| Bishop | Dispel (0%, 0%); Judge (0%, 0%); Barrier (0%, 24%) |
| Black Mage | Blizzard (1%, 61%); Thunder (1%, 61%); Fire (2%, 60%) |
| Defender | Drop Weapon (0%, 0%); Hibernate (0%, 0%); Meltdown (0%, 0%) |
| Dragoon | Lancet (0%, 0%); Wyrmtamer (0%, 0%); Wyrmkiller (0%, 58%) |
| Elementalist | Elementalshift (0%, 0%); Earth Heal (0%, 30%); Sliprain (1%, 56%) |
| Fencer | Featherblow (0%, 0%); Manastrike (0%, 0%); Swallowtail (1%, 63%) |
| Fighter | Beatdown (0%, 0%); Blitz (0%, 0%); Rush (1%, 63%) |
| Gadgeteer | Black Ingot (0%, -2%); Blue Screw (0%, -2%); Chroma Gem (0%, -2%) |
| Gladiator | Beatdown (0%, 0%); Blitz (0%, 0%); Rush (4%, 72%) |
| Gunner | Boltshot (0%, 22%); Fireshot (0%, 22%); Iceshot (0%, 22%) |
| Hunter | Addle (0%, 0%); Aim: Vitals (0%, 0%); Capture (0%, 0%) |
| Illusionist | Soil Evidence (3%, 85%); Deluge (3%, 85%); Wild Tornado (3%, 85%) |
| Juggler | Hurl (0%, 0%); Gil Toss (0%, 12%); Firebomb (6%, 62%) |
| Mog Knight | Mog Peek (0%, 0%); Mog Rush (0%, 0%); Mog Attack (6%, 77%) |
| Morpher | Bomb (0%, 0%); Bug (0%, 0%); Dragon (0%, 0%) |
| Ninja | Throw (0%, 0%); Unspell (0%, 0%); Oblivion (1%, 39%) |
| Paladin | Cover (0%, 0%); Drop Weapon (0%, 0%); Parley (0%, 0%) |
| Red Mage | Blizzard (5%, 90%); Barrier (5%, 76%); Thunder (6%, 90%) |
| Sage | Drain (0%, -1%); Blind (0%, 19%); Aero (1%, 38%) |
| Sniper | Aim: Armor (0%, 0%); Aim: Wallet (0%, 0%); Aim: Weapon (0%, 0%) |
| Soldier | Magicbreak (0%, 0%); Sensor (0%, 0%); Mindbreak (0%, 21%) |
| Summoner | Carbuncle (0%, 40%); Shiva (2%, 70%); Ramuh (3%, 70%) |
| Templar | Rasp (0%, -1%); Lifebreak (0%, 0%); Soul Sphere (0%, 0%) |
| Thief | Steal: Ability (0%, 0%); Steal: Access. (0%, 0%); Steal: Armor (0%, 0%) |
| Time Mage | Quarter (0%, 19%); Quicken (0%, 36%); Reflect (0%, 15%) |
| Warrior | Magicbreak (0%, 0%); Mindbreak (0%, 21%); Powerbreak (0%, 21%) |
| White Mage | Life (0%, 34%); Protect (1%, 51%); Shell (4%, 50%) |
| White Monk | Exorcise (0%, 0%); Holy Sign (0%, 0%); Whirlwind (0%, 40%) |

## 3. Testes de melhoria (5 contra 5, mapa variável; a classe sempre no time A; 2.000 batalhas por ponto)
Δ = diferença para o original da mesma classe e nível. Diferenças < 5 pontos não são conclusivas.

| variante | classe | nível 10 | nível 25 | nível 45 | ações/batalha (25) | MP gasto (25) | habilidades mais usadas (nível 45) |
|---|---|---|---|---|---|---|---|
| original | Illusionist/1 | 45% | 40% | 38% | 60 | 70 | [['Prominence', 30], ['Freezeblink', 27], ['Stardust', 25], ['Star Cross', 4]] |
| original | Illusionist/3 | 47% | 41% | 38% | 61 | 72 | [['Prominence', 29], ['Stardust', 27], ['Freezeblink', 26], ['Tempest', 4]] |
| original | Time Mage/3 | 29% | 38% | 38% | 66 | 64 | [['Haste', 68], ['Stop', 18], ['Fight', 10], ['Silence', 3]] |
| original | Time Mage/5 | 28% | 39% | 39% | 67 | 64 | [['Haste', 65], ['Stop', 18], ['Fight', 11], ['Silence', 2]] |
| original | Summoner/4 | 31% | 49% | 49% | 66 | 41 | [['Kirin', 37], ['Unicorn', 22], ['Madeen', 16], ['Phoenix', 8]] |
| original | Bishop/2 | 33% | 49% | 48% | 62 | 48 | [['Break', 75], ['Cura', 12], ['Fight', 5], ['Holy', 5]] |
| original | Templar/2 | 45% | 41% | 41% | 68 | 76 | [['Haste', 73], ['Fight', 14], ['Cheer', 9], ['Silence', 2]] |
| original | Sage/3 | 47% | 49% | 61% | 64 | 46 | [['Bio', 48], ['Raise', 34], ['Giga Flare', 8], ['Fight', 8]] |
| Phantasm poder 30 | Illusionist/1 | 56% (+11) | 47% (+7) | 43% (+5) | 57 | 67 | [['Prominence', 15], ['Tempest', 13], ['Freezeblink', 13], ['Deluge', 11]] |
| Phantasm poder 30 | Illusionist/3 | 56% (+9) | 49% (+7) | 46% (+8) | 56 | 69 | [['Prominence', 16], ['Freezeblink', 13], ['Tempest', 13], ['Star Cross', 13]] |
| Phantasm MP 24 | Illusionist/1 | 48% (+2) | 41% (+1) | 38% (+1) | 62 | 55 | [['Prominence', 30], ['Freezeblink', 27], ['Stardust', 27], ['Tempest', 3]] |
| Phantasm MP 24 | Illusionist/3 | 47% (-0) | 40% (-1) | 37% (-1) | 59 | 51 | [['Prominence', 30], ['Freezeblink', 26], ['Stardust', 26], ['Tempest', 4]] |
| Phantasm poder 30 e MP 24 | Illusionist/1 | 56% (+11) | 48% (+8) | 44% (+7) | 56 | 54 | [['Prominence', 16], ['Tempest', 13], ['Freezeblink', 12], ['Star Cross', 12]] |
| Phantasm poder 30 e MP 24 | Illusionist/3 | 57% (+10) | 49% (+8) | 44% (+6) | 56 | 51 | [['Prominence', 15], ['Tempest', 14], ['Freezeblink', 13], ['Star Cross', 13]] |
| Haste MP 16 | Time Mage/3 | 29% (+0) | 39% (+1) | 38% (-0) | 66 | 48 | [['Haste', 71], ['Stop', 19], ['Fight', 6], ['Silence', 2]] |
| Haste MP 16 | Time Mage/5 | 28% (+0) | 39% (+1) | 39% (-1) | 65 | 50 | [['Haste', 67], ['Stop', 17], ['Fight', 12], ['Silence', 2]] |
| Haste AP 100 | Time Mage/3 | 31% (+1) | 38% (+0) | 38% (+0) | 66 | 64 | [['Haste', 68], ['Stop', 18], ['Fight', 10], ['Silence', 3]] |
| Haste AP 100 | Time Mage/5 | 32% (+3) | 39% (+0) | 39% (+0) | 67 | 64 | [['Haste', 65], ['Stop', 18], ['Fight', 11], ['Silence', 2]] |
| Haste MP 16 e AP 100 | Time Mage/3 | 33% (+4) | 39% (+1) | 38% (-0) | 66 | 48 | [['Haste', 71], ['Stop', 19], ['Fight', 6], ['Silence', 2]] |
| Haste MP 16 e AP 100 | Time Mage/5 | 34% (+6) | 39% (+1) | 39% (-1) | 65 | 50 | [['Haste', 67], ['Stop', 17], ['Fight', 12], ['Silence', 2]] |
| Unicorn e Cura AP 100 | Summoner/4 | 48% (+16) | 49% (+0) | 49% (+0) | 66 | 41 | [['Kirin', 37], ['Unicorn', 22], ['Madeen', 16], ['Phoenix', 8]] |
| Unicorn e Cura AP 100 | Bishop/2 | 48% (+15) | 49% (+0) | 48% (+0) | 62 | 48 | [['Break', 75], ['Cura', 12], ['Fight', 5], ['Holy', 5]] |
| piso de velocidade (+10 base, +0,3 cresc.) | Illusionist/1 | 49% (+4) | 43% (+3) | 39% (+2) | 60 | 83 | [['Prominence', 29], ['Freezeblink', 28], ['Stardust', 26], ['Tempest', 4]] |
| piso de velocidade (+10 base, +0,3 cresc.) | Illusionist/3 | 51% (+4) | 45% (+4) | 39% (+1) | 60 | 84 | [['Prominence', 30], ['Freezeblink', 27], ['Stardust', 25], ['Tempest', 3]] |
| piso de velocidade (+10 base, +0,3 cresc.) | Summoner/4 | 30% (-1) | 52% (+4) | 50% (+1) | 67 | 50 | [['Kirin', 42], ['Unicorn', 21], ['Madeen', 16], ['Fight', 8]] |
| piso de velocidade (+10 base, +0,3 cresc.) | Bishop/2 | 31% (-2) | 55% (+6) | 52% (+4) | 60 | 57 | [['Break', 73], ['Cura', 12], ['Fight', 6], ['Holy', 5]] |
| piso de velocidade (+10 base, +0,3 cresc.) | Templar/2 | 50% (+5) | 45% (+3) | 42% (+1) | 67 | 79 | [['Haste', 70], ['Fight', 15], ['Cheer', 11], ['Silence', 3]] |
| piso de velocidade (+10 base, +0,3 cresc.) | Sage/3 | 53% (+6) | 51% (+2) | 65% (+5) | 62 | 51 | [['Bio', 51], ['Raise', 29], ['Giga Flare', 9], ['Fight', 8]] |
| pacote de correções | Illusionist/1 | 62% (+17) | 53% (+14) | 48% (+10) | 53 | 62 | [['Prominence', 15], ['Tempest', 14], ['Freezeblink', 13], ['Star Cross', 12]] |
| pacote de correções | Illusionist/3 | 63% (+16) | 54% (+13) | 48% (+10) | 53 | 60 | [['Prominence', 15], ['Freezeblink', 13], ['Tempest', 13], ['Star Cross', 13]] |
| pacote de correções | Time Mage/3 | 32% (+3) | 38% (-0) | 36% (-2) | 64 | 45 | [['Haste', 74], ['Stop', 18], ['Fight', 6], ['Silence', 2]] |
| pacote de correções | Time Mage/5 | 30% (+2) | 38% (-1) | 37% (-2) | 64 | 46 | [['Haste', 70], ['Stop', 18], ['Fight', 9], ['Silence', 2]] |
| pacote de correções | Summoner/4 | 50% (+19) | 53% (+4) | 51% (+2) | 64 | 49 | [['Kirin', 41], ['Unicorn', 21], ['Madeen', 16], ['Fight', 7]] |
| pacote de correções | Bishop/2 | 49% (+16) | 55% (+7) | 51% (+3) | 59 | 55 | [['Break', 74], ['Cura', 12], ['Fight', 6], ['Holy', 5]] |
| pacote de correções | Templar/2 | 46% (+1) | 41% (-0) | 41% (+0) | 65 | 64 | [['Haste', 81], ['Fight', 10], ['Cheer', 7], ['Silence', 2]] |
| pacote de correções | Sage/3 | 46% (-1) | 51% (+3) | 63% (+3) | 60 | 49 | [['Bio', 49], ['Raise', 31], ['Fight', 9], ['Giga Flare', 9]] |