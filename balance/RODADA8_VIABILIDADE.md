# Rodada 8: tornar viáveis as habilidades pouco usadas (testes no nível 25)

Dados: `exp8_underused.json` (275 combinações classe-habilidade abaixo de 3% de escolha), `exp8_patched_r1/r2/r3.json` (alterações), `exp3_team_v1_r1/r2/r3/sel.json`, `exp8_result.md`, `exp8_selected.json`. Código: `exp8_list.py`, `exp8_round.py`, `exp8_sel.py`, `exp8_report.py`.
Condições: equipes de 5, mapa variável, progressão real (40 AP por batalha, conjunto secundário), 12.000 batalhas no nível 25 (4.000 no 10 e 6.000 no 45).

## 1. Ponto de partida
No pacote atual, **275 combinações classe-habilidade são escolhidas em menos de 3% das vezes em que estão disponíveis**: 194 têm efeito modelado, 81 não (efeito sem valor no simulador: roubos, morph, Cover, Dispel, Rasp, Lifebreak...). Das 194, **60 habilidades distintas têm alavanca simples** (MP maior que zero ou poder fixo de dano), 60 combinações não têm (MP 0 e poder vindo da arma: Aim, Blackout, Wild Swing, Swallowtail, Powerbreak...).

## 2. Buff em todas as 60, em 3 passos
Poder só nas de dano (não toquei no dano de suporte), MP em todas que gastam MP; cada passo só reforça quem continua abaixo de 3%.
| passo | poder / MP | habilidades com ≥ 3% de escolha | desvio entre classes (nível 25) | ações por batalha (25) |
|---|---|---|---|---|
| base | – | 0 de 60 | 8,4 pp | 63 |
| 1 | ×1,15 / ×0,8 | 9 | 9,4 | 56 (−11%) |
| 2 | ×1,30 / ×0,6 | 13 | 10,0 | 52 (−17%) |
| 3 | ×1,50 / ×0,4 | 12 | 10,9 | 47 (−25%) |
**Mesmo com +50% de poder e −60% de MP, só 12 de 60 passam de 3%**, e os efeitos colaterais são grandes: as batalhas encurtam até 25% e as classes se afastam (Black Mage +4 a +8, Alchemist +5,6; Gladiator −7,4, Dragoon −5,6, Paladin −4,6). Os buffs em magias compartilhadas (Fire, Fira, Firaga e família) chegam a muitas classes pelo conjunto secundário.

## 3. Por que o buff numérico não basta (classificação após o passo 3)
| grupo | n | exemplos |
|---|---|---|
| **A. responde** (≥ 3% de escolha) | 8 | Heavy Dust, Sliprain e Shining Air (Elementalist, poder 46), Earth Render (Defender), Blizzard (Illusionist), Sheep Count e Cuisine (Animist/Gunner) |
| **C. valor médio** (45–70% da melhor da classe) | 14 | Toad, Protect, Life, Far Fist, Silenshot, Last Breath, Nightmare, Ague, Air Render, Body Slam, a família Fira/Firaga do Juggler |
| **D. ainda fraca** (< 45%) | 38 | Slow, Reflect, Quarter, Demi, Stop e Quicken (Time Mage), Dispel e Barrier (Bishop), Rasp, Poison e Astra (Alchemist), Unspell (Ninja), Carbuncle, Whirlwind, Tremor, Water, Aero |
Duas causas:
1. **Reduzir MP quase não muda a escolha.** O MP raramente é o limite no simulador e pesa pouco no valor de cada ação; o valor de uma habilidade de status ou suporte vem do efeito, não do custo. Os 38 casos do grupo D são, na maioria, **status e suporte**, que valem 10–40% da melhor da classe e não respondem a número.
2. **Cada classe tem uma habilidade-assinatura que vale 2–5 vezes mais** (Haste no Time Mage 409, Charmshot 83% das ações do Gunner). Para uma habilidade secundária ser escolhida ela precisaria dobrar de valor.

## 4. Versão seletiva (25 habilidades, passo 1)
Só habilidades específicas de classe; excluí as magias compartilhadas (Fire, Thunder, Blizzard, Fira, Thundara, Blizzara, Firaga, Thundaga, Blizzaga), as curas e Protect/Shell.
| | desvio entre classes (25 / 45) | ações por batalha (25 / 45) | classes fora de ±5 pp (25) |
|---|---|---|---|
| base | 8,4 / 7,4 | 63 / 46 | 24 |
| passo 1 (todas) | 9,4 / 7,8 | 56 / 41 | 25 |
| **seletivo** | **8,6 / 8,6** | **61 / 44** | **24** |
O ritmo e o equilíbrio ficam praticamente como no pacote atual (−3% nas ações). Das 25, **5 passam de 3%** (Heavy Dust 4,9%, Holy do Bishop 4,2%, Shining Air 4,2%, Sliprain 3,8%, Silenshot 3,0%, Cuisine 3,0%), e 10 passam de 2%. Classes que mais mudam no nível 25: Warrior +4,8, Animist +4,7, White Monk +3,9; Gladiator −5,1, Black Mage (Moogle) −3,5. Com erro de ±1,5 por classe, só Gladiator e Warrior estão fora do ruído.

## 5. Conclusões
- **Funcionam com ajuste de número** (poder, às vezes MP): as habilidades de dano de classe (Elementalist, Defender, Bishop). Recomendo manter o passo 1 nelas.
- **Não funcionam só com número:** status e suporte do grupo D. Precisam de mudança estrutural: **área, efeito adicional, duração ou acerto** (o que já deu certo com o Haste em área), ou de valor no simulador (Dispel, Rasp, Unspell, Lifebreak, Cover aparecem como 0 porque o efeito não está modelado).
- **Não mexer** nas magias compartilhadas: cada alteração desloca muitas classes por causa do conjunto secundário.
- Critério "≥ 3% de escolha" é duro para uma IA que escolhe sempre o melhor valor: habilidades situacionais (Dispel, Silence contra conjuradores, Manastrike) só aparecem quando o contexto pede. O simulador precisa de contexto (alvo com buffs, alvo conjurador, vários inimigos juntos) para medi-las bem.

## 6. Próximos passos propostos
1. Adotar o passo 1 nas 25 habilidades seletivas (efeito comprovado em 6, neutro nas demais).
2. Para o grupo D, testar mudança estrutural uma por vez: área em Slow, Stop, Dispel e Barrier; efeito adicional em Expert Guard e Quicken; Demi e Quarter com efeito fixo maior.
3. Dar ao simulador as situações que valorizam Dispel, Silence e Manastrike antes de decidir se são fracas.
