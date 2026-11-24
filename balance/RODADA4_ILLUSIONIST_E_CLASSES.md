# Rodada 4: Illusionist corrigido, melhorias nas classes 16–38 e novo ranking

Dados: `exp4_ill_raw.json`, `exp4_classes_raw.json`, `exp4_result.md`, `exp3_team_final2.json` e `exp3_team_final3.json`, `RANKING_CLASSES_V2.md`. Código: `exp4_ill.py`, `exp4_classes.py`, `exp4_teams.py`, `ranking.py`.

## 1. Illusionist (prioridade)
O R2 tinha dado ao Illusionist orçamento ×1,26 para compensar o Phantasm fraco. Com o Phantasm a poder 30, isso o levava a +29 pp na equipe. Calibrei o orçamento dentro do pacote final (5 contra 5, mapa variável, 2.500 batalhas por ponto):
| orçamento (k) | vitória nível 10 / 25 / 45 | média |
|---|---|---|
| ×1,26 (R2) | 83 / 71 / 65% | 73% |
| ×1,14 | 71 / 64 / 57% | 64% |
| **×1,00 (escolhido)** | **58 / 53 / 46%** | **53%** |
| ×0,88 | 41 / 43 / 40% | 41% |
Efeito na equipe (regressão, 12.000 batalhas por nível), Illusionist: original −5/−14/−19 · pacote anterior +46/+24/+17 · **recalibrado +10/+5/−3** (com as melhorias das outras classes, +7/+3/−3). Passa de "pior da lista" para forte no início e comum no fim, sem esmagar. Sem inflar atributos: o ganho vem do Phantasm (poder 30).

## 2. Melhorias nas classes 16–38 (estratificado, 2.000 batalhas por ponto; conclusivo = |Δ médio| ≥ 4 com o mesmo sinal em 2 níveis)
| mudança (só dado) | classe | Δ (10/25/45) | conclusivo |
|---|---|---|---|
| Paladin: Nurse 30 → 45 | Paladin | +8 / +2 / +3 | **sim** (+4,3) |
| Paladin: Saint Cross 45 e MP 18; Holy Blade MP 24 | Paladin | +0/+0/+5; +0/+0/+4 | não isoladas; juntas com Nurse: **+4,7** |
| Elementalist: Fire Whip, Shining Air, Heavy Dust, Sliprain 30 → 40 | Elementalist | +6 / +5 / +2 | **sim** (+4,4) |
| Magias Tier 2 e 3 (46/14, 68/30) | Black Mage ×3 | +0 / +1 a +4 / +6 a +7 | só no nível 45 |
| First Aid 25 → 40 | Soldier, Warrior | +5 / +1 / 0 e +5 / −2 / +1 | só no nível 10 |
| Orçamento +8% | Red Mage | +8 / +3 / +5 | **sim** (+5,2) |
| Orçamento +8% | Assassin, Fencer, Soldier, Mog Knight | +3,8, +3,5, +3,2, +2,6 | não conclusivo (sinal certo) |
| Powerbreak/Mindbreak com debuff duplo | Soldier, Warrior | −1 / −1 | **não** (piora o nível 25) |
| Mog Aid 35 → 50; Dagger 42 e Firebomb 45 (Juggler); Frogsong MP 12 (Animist) | Mog Knight, Juggler, Animist | +0,4; +1,5; +1,9 | não |
| Cupid MP 0 / 4 (Archer) | Archer | ±0,3 | não: **Cupid a 8 MP não prejudica** |
| Stop em área (Time Mage) | Time Mage | 0 | não |
**Escolhido para o pacote:** Paladin (3 mudanças), Elementalist (4 habilidades), magias tier 2 e 3, First Aid 40, e orçamento +8% em Assassin, Fencer, Soldier, Mog Knight, Juggler, Red Mage. **Descartado:** debuff duplo, Mog Aid, Juggler, Cupid, Stop em área, Frogsong.

## 3. Resultado (ranking completo em `RANKING_CLASSES_V2.md`)
| | desvio entre classes | tiers S/A/B/C/D |
|---|---|---|
| original | 13,6 pp | 11 / 8 / 3 / 9 / 11 |
| pacote anterior (com Illusionist inflado) | 9,9 pp | 2 / 10 / 14 / 14 / 2 |
| **esta versão** | **7,4 pp** | **0 / 11 / 21 / 8 / 2** |
## 4. O que continua aberto
- **Time Mage** (−8 e −9; −20 no nível 10): sem habilidade no começo. Haste a 100 AP deu +3 a +6 no nível 10, não está no pacote.
- **Thief, Morpher, Blue Mage, Gadgeteer, Beastmaster:** kit não modelado; as posições deles não são evidência.
- **Ninja, Sniper, Animist (−3,3 a −3,8):** sem mudança proposta ainda.
- Dependências já conhecidas: Haste em área precisa de confirmação em jogo (se atinge inimigos).
