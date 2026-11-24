# Rodada 7: conjunto secundário realista e 16 batalhas no nível 10

Ranking completo: `RANKING_CLASSES_V5.md`. Dados: `exp3_team_q2_*.json`. Código: `progression.py` (`plan`, escolha do secundário), `ability_ev.json` (valor esperado medido de cada habilidade), `ranking4.py`.

## 1. Mudanças no modelo (a partir do que você informou)
- **Batalhas:** 16 no nível 10 (você chega às 20 entre o 10 e o 15), 40 no 25 e 90 no 45; 40 AP por batalha.
- **Secundário no início = pré-requisito** (até o nível 15). **Depois:** o mais útil. Para cada unidade, o simulador avalia as classes que ela pode usar (iniciais e as da sua cadeia de pré-requisitos), conta o que ela consegue aprender com o AP que sobra do kit próprio e escolhe o conjunto cujas 3 melhores habilidades têm maior valor esperado (medido em simulações anteriores, `ability_ev.json`). **Preferência por não misturar físico e mágico:** o tipo diferente vale 0,4 do valor; White Mage é exceção (suporte).
- Classes indisponíveis no nível 10 por falta de AP (Illusionist ×2, Alchemist, Morpher, Sage, Assassin, Summoner, Time Mage ×2) continuam fora das lutas desse nível.

## 2. Resultado (efeito na equipe, 5 contra 5, mapa variável, 12.000 batalhas por nível, erro ≈ ±1)
Desvio entre classes: original 12,4 pp · R2 8,7 · **pacote 8,7**. Tiers S/A/B/C/D: original 10/9/5/7/11 → **pacote 4/8/13/15/2**.
**Topo:** Blue Mage +17,4, Templar +16,4, Time Mage (Nu Mou) +14,1, Time Mage (Moogle) +11,7, Alchemist +9,7, White Mage (Hume) +6,2, Sage +6,1, Summoner +5,1, Warrior +4,6, White Mage (Nu Mou) +4,5, Elementalist +4,0, Black Mage (Moogle) +3,6.
**Fundo:** Paladin −14,1, Morpher −11,4, Thief (Hume) −9,4, Thief (Moogle) −7,2, Sniper −6,9, Gunner −6,8, Gadgeteer −6,0, Beastmaster −5,7, Ninja −5,2, Archer ×2 −5,0, Defender −4,6, Fighter −4,6.

## 3. Robustez
| variação do modelo | correlação de postos com o ranking principal |
|---|---|
| secundário só o de pré-requisito | 0,91 |
| **proibir** mistura físico×mágico quando há alternativa | **0,97** |
| sem nenhum secundário | **0,49** |
- Como o secundário é escolhido (com ou sem mistura) **quase não muda o ranking**. Com o peso 0,4, 18 das 84 escolhas misturam tipos (Fighter, Paladin, Mog Knight, Juggler e Hunter com Black Mage; Bishop e White Mage com conjuntos físicos); proibir isso move poucas classes (Mog Knight #21 → #12; Thief Moogle #39 → #26).
- **Ter ou não um secundário muda muito:** sem secundário, Blue Mage cai de +17,4 para −8,8 (#38), Templar de +16,4 para +0,4, Time Mage de +14,1/+11,7 para −3,3/−3,9, Alchemist de +9,7 para −4,4. O topo é, em boa parte, um efeito do secundário. Como você confirmou que o secundário é usado de verdade, o ranking com secundário é o que vale.

## 4. O que isso diz
- **Classes avançadas com pré-requisito** (Templar, Time Mage, Alchemist, Sage, Summoner, Blue Mage) herdam um conjunto forte (Whirlwind e Air Render de White Monk; magias de Black Mage) e por isso lideram. É o desenho do jogo, não só do simulador, mas o tamanho do efeito pode estar exagerado porque o simulador usa o secundário o tempo todo e de forma ideal.
- **Paladin é a pior classe com kit modelado** (−14,1; −18 e −11 nos níveis 10 e 25). Melhorias anteriores (Nurse 45, Saint Cross, Holy Blade) não bastam neste modelo. Candidato à próxima rodada.
- **Gunner, Archer, Ninja, Sniper, Fighter** ficam em C: os ajustes anteriores já os tiraram do topo e o novo modelo os deixa abaixo.
- **Thief, Morpher, Gadgeteer, Blue Mage, Beastmaster:** sem kit modelado; posição não é evidência. Blue Mage no topo é só o secundário (Black Mage), não a classe.

## 5. Limites
Batalhas por nível ainda são estimativa; o secundário é escolhido pelo mesmo valor esperado da IA do simulador; o desbloqueio de classes é por menor custo e a unidade já tem todas as habilidades baratas.
