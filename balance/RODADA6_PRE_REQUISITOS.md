# Rodada 6: progressão com loja real, pré-requisitos de classe e 40 AP por batalha

Ranking completo: `RANKING_CLASSES_V4.md`. Dados: `exp3_team_q_*.json`, `exp6_diag.json`. Código: `progression.py` (função `plan`), `exp6_teams.py`, `exp6_diag.py`, `ranking3.py`.

## 1. Modelo
- **Loja inicial:** as 24 armas da base que você enviou. Armas das listas de 10 e 20 batalhas liberam depois; as demais só depois de ~35 batalhas.
- **AP:** 40 por batalha; 12 batalhas até o nível 10, 40 até o 25, 90 até o 45 (suposição ainda aberta).
- **Pré-requisitos por raça** (tabelas que você enviou). Para existir como classe, a unidade precisa dominar as A-abilities exigidas, recursivamente (Assassin exige Elementalist, que exige Fencer e White Mage; e Sniper, que exige Archer). Esse AP sai do **mesmo orçamento**; o que sobra compra as habilidades da própria classe, das mais baratas às mais caras.
- **Conjunto secundário:** as habilidades dominadas como pré-requisito ficam disponíveis em batalha (na classe de pré-requisito com mais habilidades).
- **Disponibilidade:** no nível 10 não existem, por falta de AP: Illusionist ×2 (1.200 AP de pré-requisito), Alchemist (1.200), Morpher (1.000), Sage (900), Assassin (800), Summoner (700), Time Mage ×2 (700). A partir do nível 25 existem todas. Essas classes não entram nas lutas do nível 10.

## 2. Resultado (efeito na equipe, 5 contra 5, mapa variável, 12.000 batalhas por nível)
Desvio entre classes: original 12,8 pp · R2 9,4 · pacote 9,7. Tiers S/A/B/C/D: original 10/8/7/4/13 → **pacote 5/6/17/11/3**. Com 50% mais batalhas por nível a correlação de postos é 0,90.
**Topo:** Templar +18,2, Time Mage (Nu Mou) +13,3, Blue Mage +13,2, Time Mage (Moogle) +11,0, Alchemist +10,8, White Monk +8,9, Sage +7,0, Summoner +6,7, Mog Knight +6,2, Assassin +5,7.
**Fundo:** Morpher −18,9, Thief (Moogle) −13,7, Thief (Hume) −11,8, Paladin −9,0, Gadgeteer −8,5, Ninja −8,1, Beastmaster −6,1.

## 3. A suposição que decide o topo: o conjunto secundário
Retirando-a (coluna "sem conjunto secundário" do ranking):
| classe | com secundário | sem |
|---|---|---|
| Templar | +18,2 | +1,1 |
| Blue Mage | +13,2 | −8,3 |
| Time Mage (Nu Mou / Moogle) | +13,3 / +11,0 | −3,3 / −3,9 |
| Alchemist | +10,8 | −4,4 |
| White Monk | +8,9 | +10,4 |
| Summoner | +6,7 | +9,0 |
Diagnóstico estratificado (`exp6_diag.json`): o pico de **Templar no nível 10 (81%)** e de **Blue Mage (75%)** desaparece sem o secundário (53% e 51%). No Templar vêm de Air Render e Whirlwind, herdados de White Monk (Air Render: poder 45, alcance 3, 0 MP). O **Time Mage no nível 25–45 (65%/59%)** cai para 47/45% sem as magias de Black Mage. **Haste em área** pesa menos: Templar e Time Mage +4 a +6.
**Conclusão:** em classes avançadas, o poder depende do que o jogador carrega como secundário. O simulador usa todas as habilidades dominadas, sem escolha do jogador, e **isso superestima** quem tem um bom pré-requisito. O ranking sem secundário é o piso; o com secundário é o teto.

## 4. Pontos para decidir
1. **Como você escolhe o conjunto secundário?** Sempre o de pré-requisito, ou outro (ex.: White Mage para curar)? Isso define qual dos dois rankings se aproxima do jogo.
2. **Haste em área** só deve entrar com a classe que o ensina estável; o efeito em Templar e Time Mage é de +4 a +6.
3. Batalhas por nível ainda são suposição (12, 40, 90).
4. **Classes sem kit modelado** (Thief, Morpher, Gadgeteer, Blue Mage, Beastmaster): posição não é evidência.
