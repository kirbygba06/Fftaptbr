# Segunda rodada: tabela de propostas (nenhum patch novo foi gerado)

Resultados completos: `exp2_result.md` (tabelas), `exp2_*.json` (dados brutos: vitória por classe, uso por habilidade, sucesso e turnos negados dos status, impacto por ação, MP por unidade, ações por batalha), `classes_foco_r2.md`. Código: `exp2.py`, `exp2_combo.py`, `combo.py`, `exp2_report.py`. Sementes iguais entre versões; 4.000 batalhas por ponto (1.500 nas ablações por habilidade). **Diferença menor que ~5 pontos em uma classe não é conclusiva** (ruído medido: 2,2–2,4 de média, p90 4–5).

## 0. Três correções no simulador (mudam conclusões anteriores)
1. *(rodada anterior)* O filtro de alvo ("só Undead/Dragon") foi corrigido.
2. **Novo:** habilidades de área centradas no próprio personagem (Wild Swing, Whirlwind, Tremor, Saint Cross, Swallowtail, Mow Down) eram valoradas como dano ao caster, ou seja, sempre negativas. Corrigido: agora são golpes corpo a corpo em área, com risco de acertar aliados (fogo amigo 25%).
3. **Consequência:** no motor corrigido o **Defender** sobe de 38% (modelo antigo) para **~61%** no original e o pacote de referência (R1) o leva a **~83%**, um excesso. Os números anteriores do Defender não valem. As demais classes mudaram ≤4 pontos.
**Referência R2 (reajuste do orçamento de classes no motor corrigido, ainda não gerado como patch):** σ 0,121/0,114/0,114 (original) → R1 0,099/0,090/0,083 → **R2 0,086/0,078/0,073** (níveis 10/25/45); classes fora de 40–60%: 16/19/22 → 11/9/9 → **9/10/9**; ações por batalha: 54/46/47 → 47/43/47 → 49/45/49. **O ritmo agora é semelhante ao original** (o desvio de +18% no nível 45 que medi antes era do motor antigo).

## 1. Tabela de propostas
Legenda: **[D]** dados, **[A]** ASM. Fase 0 = jogar antes de alterar mais. Fase 1 = habilidades/magias. Fase 2 = hooks.
| # | proposta | patch | evidência medida | esforço | risco | decisão |
|---|---|---|---|---|---|---|
| 1 | Classes: orçamento reajustado (R2), mantendo a forma por papel | `bal20_classes` [D] | σ 0,114 → 0,078 (nível 25); Defender 83% → ~60% | baixo (já calculado) | modelo; Thief, Morpher e Blue Mage sem prova | **Fase 0** (jogar R2 em vez de R1) |
| 2 | Itens: armadura convexa, topo das armas de saque comprimido (87→68), preço crescente com ATK, venda = metade | `bal21_itens` [D] | 22 armas piores e mais caras → 0; ritmo de batalha ≈ original no motor corrigido | baixo | escudos e acessórios continuam fracos (não resolvido) | **Fase 0** (igual a bal11) |
| 3 | Tiros de status do Gunner 6 MP (variante 10 MP para teste) | `bal22_habilidades` [D] | Gunner 70% → 57%; 10 MP: −17 (nível 25) e −8 (nível 45) | baixo | com 10 MP vira artilharia comum (só 39% das ações com status) | **Fase 0**; testar 6 e 10 |
| 4 | Cupid 8 MP | `bal22_habilidades` [D] | Archer −2 a −5, dentro do ruído | baixo | efeito pequeno | opcional |
| 5 | Magias: Tier 2 = 46 poder/14 MP; Tier 3 = 68 poder/30 MP | `bal23_magias` [D] | Black Mage (Hume): tier 2 +10 (nível 25); tier 3 +7 (nível 45); σ 0,114 → 0,108; MP por unidade igual (63) | baixo | só 2 classes mudam; Cure/Cura/Curaga não testadas | **Fase 1** |
| 6 | AP 100/200/400 e finais 600–990 | `bal23_magias` [D] | **sem evidência**: o AP só define quando o tier existe e a progressão de AP não está modelada | baixo | muda o ritmo de progressão | adiar |
| 7 | Whirlwind: poder 25 → 35–40 | `bal22_habilidades` [D] | valor esperado por ação = Fight (34 vs 34 no nível 25; 48 vs 57 no 45) | baixo | pouco | **Fase 1** |
| 8 | Powerbreak e Mindbreak: trocar o efeito por um debuff mais forte (−30% DEF/RES) ou somar um 2º efeito | `bal22_habilidades` [D: IDs de efeito] | valor esperado 7–14 contra 31–54 do Fight (~25%); uso forçado derruba a vitória em 15–18 pontos | baixo | muda a identidade das "breaks"; precisa de teste em jogo | **Fase 1** (uma por vez) |
| 9 | Expert Guard: somar efeito defensivo (2º efeito) | `bal22_habilidades` [D] | tirar a habilidade **melhora** o Defender em +6 (nível 45), mesmo ela sendo usada em 38% das ações: o efeito não compensa a ação | baixo | Defender ainda sobrestimado (ver Mow Down) | **Fase 1**, depois do Defender estabilizar |
| 10 | Tremor, Wild Swing, Saint Cross, Swallowtail | – | **não são inúteis**: valor esperado 1,1–1,6× o do Fight; baixa frequência por haver opção melhor; ablação ≈ 0 (redundância) | – | – | **não alterar** |
| 11 | Magicbreak, Holy Sign, Manastrike, Dispel, Rasp, Carbuncle, Barrier | – | o simulador não modela o efeito (valor 0) ou o benefício; Barrier e Water/Aero têm valor 1,5× o do Fight mas o Bishop prefere Break (82%) | – | alto sem teste | **não alterar** até haver modelo |
| 12 | Combo: `(10 + 4·JP)/10` → `(10 + 2·JP)/10` | `bal24_jp_combo` [A] | **rotina localizada e verificada em `0x134122`**: 1 halfword (`lsls r0,r0,#2` → `#1`, bytes `80 00` → `40 00`). No modelo (JP inicial 5): ações por batalha −33% → −17%, multiplicador do golpe final 1,9× → 1,5× | muito baixo | **não sei quanto JP as unidades têm em jogo**; σ quase não muda (~0,10) | **Fase 2**, depois de medir JP |
| 13 | Teto de JP útil 5 | `bal24_jp_combo` [A] | modelo: com K=2 + teto, ações por batalha −20%, multiplicador 1,5×; K=4 + teto 1,9× | médio: precisa de trampolim em área livre próxima | caverna segura não identificada | adiar; K=2 sozinho já reduz |
| 14 | Hunting 10 → 3 JP | `bal24_jp_combo` | rotina do JP **não localizada**. Hipótese: o 4º slot de efeito do Hunting vale 10 (dado) e o código usa isso (o guia diz que esse efeito nunca roda). **No modelo Hunting é usado em 1,5% das ações: sem efeito** | baixo [D] se a hipótese estiver certa; senão [A] alto | hipótese não confirmada | testar em jogo (mudar o slot 4 para 3) |
| 15 | Totema 85 → 65 | `bal23_magias` [**D, não ASM**] | os 5 Totemas têm poder 85 na tabela (Mateus, Adrammelech, Ultima, Exodus, Famfrit). **Não está no simulador**; depende de JP | baixo | JP desconhecido | adiar junto com o item 12 |
| 16 | Charm de 2 turnos | `bal26_status` [A] | Archer 61% → 52% (nível 45), Gunner 72% → 73%. **Duração não está em tabela**; rotina não localizada | alto (achar a rotina por rastreio) | médio | **precisa da sua autorização** |
| 17 | Haste ×1,5 | – | Time Mage **cai** (40% → 35% no nível 45); σ 0,114 → 0,116: sem ganho | – | – | **não recomendo** |
| 18 | Double Sword segundo golpe 65% | `bal25_turnos` [A] | Ninja 68% → 63% (borderline); σ igual | médio | pouco ganho | só se o Ninja continuar forte no jogo |
| 19 | Doublecast, Quicken | – | Doublecast: 0 pontos de efeito; sem Quicken o Time Mage cai 3–6 | – | – | **não alterar** |
| 20 | Mais compressão de velocidade | `bal20_classes` [D] | σ 0,090 → 0,085/0,084; Assassin 62% → 58–59%: dentro do ruído | baixo | descaracteriza classes rápidas | **não recomendo** |
| 21 | Rockseal, Death Sickle, Checkmate, Charmshot, Fire Veil | – | ablações ≈ 0 (rodada anterior) | – | – | **não alterar** |

## 2. Classes que você pediu para recuperar (taxa de vitória 10/25/45)
| classe | original | R1 (bal10 atual) | R2 | observação |
|---|---|---|---|---|
| Defender (Bangaa) | 60/61/62 | 85/84/80 | 51/63/61 | forte pelo Mow Down (ataque em área, 0 MP), **não pela proteção**; Cover não modelado |
| White Monk | 55/65/55 | 46/58/53 | 47/58/54 | Whirlwind abaixo do Fight (item 7) |
| Bishop | 23/51/49 | 33/60/54 | 34/60/52 | usa Break (Petrify) em 82% das ações; é o que o define |
| Templar | 45/41/37 | 54/46/40 | 65/47/43 | Rasp não modelado |
| Dragoon | 63/71/53 | 53/62/50 | 52/64/50 | preservado |
| Fencer | 70/57/51 | 54/46/47 | 57/50/50 | Manastrike não modelado; Swallowtail valor 1,4× o do Fight |
| Alchemist | 41/39/47 | 44/39/58 | 46/47/61 | habilidades situacionais não modeladas |
| Morpher, Blue Mage, Gadgeteer | 35/35/33, 48/37/37, 42/39/36 | 42/33/32, 51/42/38, 59/49/45 | 43/38/37, 51/43/35, 58/48/41 | **sem forma confiável de testar**: não alterar |
| Gunner | 67/68/74 | 50/58/64 | 50/54/65 | itens 3 e 4 |

## 3. Ordem de execução que proponho
1. **Fase 0, só jogar**: `bal20_classes` (R2), `bal21_itens` e `bal22` (Gunner 6 MP). Comparar a sensação com a previsão do simulador antes de qualquer outra coisa.
2. **Fase 1**: itens 5, 7, 8, 9, um por vez, cada um com seu CSV, ablação e reversão.
3. **Fase 2 (depois de medir JP em jogo)**: item 12 (1 halfword), depois 14 e 15.
4. **Charm (item 16)** só com sua autorização para rastrear a rotina.

## 4. O que não consegui fazer e por quê
- **JP real**: o modelo varre estoques de JP (0, 3, 5, 10) porque o jogo não tem isso no que eu li. Preciso saber quanto JP uma unidade costuma ter no meio de uma batalha.
- **Fórmula de Combo**: confirmei a de dano (`JP·4+10`, divisor 1.000, bônus da cadeia em %). A **tabela de Poder/Alcance/Hit% dos combos não foi achada** em dados simples da ROM.
- **Identidade do Defender**: não há métrica de "proteção" (Cover, Expert Guard, dano evitado ao aliado) no simulador. Sem ela não deveria tocar nas ferramentas dele.
- **Gadgeteer (aleatoriedade), Morpher (almas) e Blue Mage (aprendizado)**: não modelados.

## 5. Reversão
Cada patch será de bytes gravados em registros de tabela (ou 1 halfword no código). Reverter = não aplicar o IPS. Para os de ASM, o IPS guarda o original no relatório do patch.
