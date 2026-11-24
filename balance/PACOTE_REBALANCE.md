# Pacote de rebalanceamento (atributos + itens + habilidades)

Resposta à crítica: o ajuste de MP do Gunner era só a camada de habilidades. O pacote completo tem três módulos independentes, cada um um IPS reversível (não aplicar = voltar ao original):
| módulo | patch | o que muda | registros |
|---|---|---|---|
| **Classes** | `bal10_classes.ips` | base e crescimento de HP/MP/ATK/DEF/PM/RM/Velocidade, Evade, de 42 classes jogáveis | 84 |
| **Itens** | `bal11_itens.ips` | armaduras, topo das armas de saque, preços, venda = metade | 180 |
| **Habilidades** | `bal01_tiros_de_status_mp6.ips` + `bal02_cupid_mp8.ips` | MP dos 5 tiros de status do Gunner (0→6) e de Cupid (0→8) | 6 |
Os IPS foram aplicados em memória sobre a ROM e relidos: **0 divergências** entre o valor pretendido e o gravado. Não se sobrepõem entre si nem à tradução.

## O que cada módulo faz
**Classes** (`f1_classes.csv`/`f1v4_*`): cada classe recebe uma *forma* por papel (guardião, atacante, ágil, mago, apoio) e um *orçamento* ajustado pelo simulador completo (habilidades + status) para a taxa de vitória ficar perto de 50%, com limite de ×0,8 a ×1,2 (identidade preservada). Velocidade e Evade comprimidos (mais rápida/mais lenta 1,87× → 1,47×). MP dos magos −30% de crescimento. ATK e PM de todos ×1,12 para compensar a lentidão causada pela armadura.
**Itens**: armadura convexa (peças fracas iguais, melhores ×3); topo de saque comprimido (87→68); preço crescente com o ATK dentro de cada tipo (22 armas de loja piores e mais caras → 0); venda = metade.
**Habilidades**: só onde o efeito passou do ruído (Gunner). Rockseal, Death Sickle, Checkmate, Charmshot isolado e Fire Veil isolado: sem mudança (ablação ≈ 0, ver `BALANCEAMENTO_CONSERVADOR.md`).

## Resultado (simulador completo, 4.000 batalhas por ponto, níveis 10/25/45)
| módulos | nível | faixa de vitória | desvio padrão | classes fora de 40–60% | ações/batalha |
|---|---|---|---|---|---|
| original | 10 / 25 / 45 | 21–69 / 28–77 / 29–74% | 0,120 / 0,119 / 0,109 | 19 / 17 / 19 | 56 / 47 / 60 |
| só habilidades | 10 / 25 / 45 | 21–66 / 27–74 / 29–72% | 0,117 / 0,110 / 0,110 | 15 / 16 / 19 | 56 / 47 / 60 |
| só classes e itens | 10 / 25 / 45 | 27–69 / 30–67 / 35–65% | 0,094 / 0,084 / 0,071 | 9 / 11 / 7 | 49 / 43 / 69 |
| **pacote completo** | 10 / 25 / 45 | 28–75 / 26–65 / 38–66% | **0,098 / 0,078 / 0,071** | **12 / 8 / 7** | 48 / 43 / 71 |
Comparação por classe em `exp_final_result.md`. Gunner 70% → 58%, Assassin 65 → 52, Ninja 64 → 52; Illusionist 35 → 55, Defender 38 → 51, Black Mage 42 → 55, Summoner 40 → 52.
**Robustez** (`robust_final_result.md`, níveis 25 e 45, 11 trocas de suposição: duração dos status ×0,5 e ×2, valor dos status na IA ×0,5 e ×1,5, fogo amigo 0 e 0,5, peso do alcance, imunidade dobrada, precisão registrada, times de 4): o desvio fica em **0,058–0,081** contra **0,095–0,122** do original, e as classes fora de 40–60% caem de **12–22 para 3–10** em todos os casos.

## Charm de 2 turnos
- **Efeito medido** (`exp_charm_raw.json`): Charm de 4 para 2 turnos tira **Archer** de 61→52% (nível 45) e 53→46% (nível 25), e quase não mexe no Gunner (72→73%), porque os tiros dele aplicam Charm só quando o dano acerta e Charm já termina ao receber dano. Pacote completo + Charm 2: desvio 0,098/0,080/0,071, praticamente igual.
- **Como implementar**: não achei a duração de Charm como dado. Habilidade só tem os 4 IDs de efeito, flags e poder (nenhum campo de duração); varredura da ROM por uma tabela de durações não achou nada. Está no código do jogo (aplicação de status). Esse é o caso em que ASM se justifica, mas exige localizar a rotina (rastrear com emulador ou desmontar o código de batalha) antes de mudar uma constante. Não tentei sem sua autorização.

## Pontos abertos e riscos
1. **Ritmo da batalha**: nível 10 14% mais rápido (48 vs 56), nível 25 9% mais rápido, **nível 45 18% mais lento (71 vs 60)**. A armadura alonga os combates tardios; ATK×1,12 compensou só em parte. Botões: `wdef` (peso da armadura) e `atk_scale`.
2. **Nível 10 ainda desigual** (σ 0,098, 12 classes fora de 40–60%), porque os kits mudam com os tiers de AP e um orçamento por classe não os acompanha.
3. **Fora da prova**: Thief, Beastmaster, Morpher, Blue Mage (kit não modelável; Thief/Morpher ficam em 45–46% e 40%); Time Mage 36% (utilidade Haste/Slow que o simulador mede mal); reações, JP/Combo/Totema, elementos, segundo conjunto de habilidades.
4. Inimigos humanos usam as mesmas tabelas; monstros não mudam. Contra monstros o jogador fica um pouco mais forte no começo e mais lento no fim.
5. Tudo em modelo; **precisa de jogo**: Gunner, Assassin e Ninja ainda parecem fortes? Illusionist/Black Mage ficaram úteis? Tela de equipamento com DEF maior: números cabem?

## Ordem sugerida de teste em jogo
1. `bal10_classes` sozinho. 2. + `bal11_itens`. 3. + `bal01` (Gunner). Se algo parecer errado, a etapa anterior mostra a causa.
