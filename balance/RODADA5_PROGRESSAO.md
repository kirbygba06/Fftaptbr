# Rodada 5: progressão de habilidades revista (estoque da loja + AP acumulado) e ranking v3

Você tinha razão: eu ligava o kit do nível 10 a "AP ≤ 100". Isso não corresponde à progressão real, que depende de (1) a arma que ensina a habilidade estar no estoque da loja e (2) o AP acumulado nas batalhas. Refiz o modelo e o ranking.
Arquivos: `progression.py` (modelo), `RANKING_CLASSES_V3.md` (ranking completo), `exp3_team_p_*.json` (dados), `ranking2.py`.

## 1. Modelo novo
- **Estoque das armas** (`progression.py`): armas da sua lista de 10 batalhas (estoque 1) e de 20 batalhas (estoque 2). As não listadas: estoque inicial se custam ≤ 1.200 gil; senão estoque tardio (após 35 batalhas, que cobre lojas maiores e saque). Resultado: 37 habilidades no estoque inicial, 53 no de 10 batalhas, 40 no de 20 e 173 no tardio.
- **AP acumulado:** AP por batalha × batalhas jogadas até o nível (12 batalhas no nível 10, 40 no 25, 90 no 45). Aprende-se do mais barato ao mais caro entre as que o estoque libera.
- **Valor padrão:** 40 AP por batalha. No nível 10 isso dá 480 AP: uma unidade já tem de 1 a 4 habilidades, incluindo as de 200 AP. Exemplos no nível 10: Black Mage Fire, Thunder, Blizzard; Illusionist Prominence, Tempest, Freezeblink; Time Mage Haste e Slow (sem corte de 100 AP); Summoner Unicorn e Ifrit.
- **Mudança de conclusão já visível:** o Time Mage no nível 10 sai de −20 pp para −0/−4 pp (Haste existe cedo pelo Firewheel Rod).

## 2. Ranking v3 (pacote completo; 42 classes em `RANKING_CLASSES_V3.md`)
Desvio entre classes: original neste modelo 13,4 pp · R2 9,0 · **pacote 8,6** (7,4 no modelo antigo). Tiers S/A/B/C/D: original 10/10/4/6/12 → **pacote 2/10/18/9/3**.
**Topo:** Summoner +16,3 (S), White Monk +10,3 (S), White Mage (Hume) +6,0, Mog Knight +5,9, Soldier +5,7, White Mage (Viera) +5,6, Dragoon +4,8, Black Mage (Moogle) +4,6.
**Meio (tier B, 18 classes):** Illusionist +2,5 e +1,1, Assassin +2,5, Sage +1,8, Black Mage (Nu Mou, Hume) +1,7 e +1,6, Alchemist +1,1, Gunner +0,9, Fencer +0,6, Fighter, Gladiator, Elementalist, Templar (−0,7), Archer ×2, Animist, Time Mage (Nu Mou, −2,9).
**Fundo:** Time Mage (Moogle) −4,5, Gadgeteer −4,6, Sniper −5,0, Defender −6,5, Paladin −6,9, Blue Mage −9,7, Thief (Hume) −10,0, Thief (Moogle) −11,4, Morpher −13,8.

## 3. O que mudou em relação ao ranking anterior
- **Subiram:** Summoner (+8,6 → +16,3, kit completo cedo), Mog Knight (+1,2 → +5,9), Soldier, Juggler, Red Mage.
- **Caíram:** Bishop (+8,0 → −3,7), Defender (+3,7 → −6,5), Templar (+4,9 → −0,7), Paladin. No nível 10 Defender (−22), Paladin (−20) e Bishop (−16) ficam com 1 a 2 habilidades úteis e dependem do estoque tardio para o resto.
- **Illusionist:** continua em tier B (+2,5/+1,1) com orçamento ×0,8.
- **Classes avançadas no nível 10** (Sage, Alchemist, Hunter, Sniper, Morpher, Blue Mage): 0 habilidades de ação pelo estoque, e por isso aparecem mal no nível 10 (Sage −16, Alchemist −19). No jogo essas classes só existem depois de dominar habilidades das anteriores, então o nível 10 delas é pouco realista; **a média por classe subestima essas**.

## 4. Robustez à suposição de AP por batalha (pacote)
Correlação entre os postos com 20, 40 e 80 AP por batalha: 0,85 e 0,82. Mudam bastante: Soldier (#8 com 20 AP, #5 com 40, #28 com 80), Warrior (#11, #13, #31), Alchemist (#38, #20, #22), Assassin (#24, #15, #5), Fencer (#6, #22, #26). Summoner fica em 1º nas três.

## 5. O que eu preciso de você (entradas do modelo)
1. **Quantos AP por batalha as unidades ganham** (valor típico por batalha, normal e missão)? O resultado de Soldier, Warrior, Fencer e Assassin depende disso.
2. **Estoque inicial da loja** (antes das 10 batalhas): quais armas e habilidades? Eu assumi "preço ≤ 1.200".
3. **Quando as classes avançadas ficam disponíveis** (Sage, Alchemist, Hunter, Sniper): em qual nível/batalha costuma-se ter uma?
4. Quantas batalhas até o nível 10, 25 e 45 (assumi 12, 40, 90)?

## 6. Limites
O modelo ignora o desbloqueio de classes, a habilidade secundária e que o jogador escolhe o que aprender (aqui é "mais barato primeiro"). O estoque tardio concentra 173 habilidades por falta de dados.
