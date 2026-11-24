# Rodada 10 — identidade para Fire / Blizzard / Thunder (Black Mage)

Na ROM os três elementos são idênticos nos três níveis (poder 30/40/50, MP 6/12/24, alcance 4, área r1; o efeito é só o dano, `fx=[63,1,1,1]`). Só o elemento muda, e ele só importa contra fraquezas. O jogo já tem efeito secundário dependente do dano (Fire Whip, Sliprain, Heavy Dust), então dá para diferenciar só com dados.

Pesquisa (fóruns e devlogs de design, não autoridade): diferenciar por função (dano, controle, custo, alcance), não só por elemento; "mesmo dano, custo diferente" é queixa comum; versões de alvo único e de área ajudam o equilíbrio.

Base: área seletiva da Rodada 9 (5v5, progressão real, 12000 batalhas no nível 25, 4000 no 45).

| Variante | O que muda | σ entre classes (25/45) |
|---|---|---|
| e0 | controle, sem mudança | 8,2 / 7,1 |
| e1 | Fogo +10% dano; Gelo −5% e Slow dependente; Raio −25% MP | 9,1 / 7,4 |
| e3 | Fogo +20% dano; Gelo −15% e Slow dependente; Raio igual | 8,6 / 7,6 |
| e5 | e3 + Raio em área maior (r2) nos tiers 1 e 2, com poder −10% | 8,7 / 8,1 |

Uso das magias do Black Mage (nível 25): no controle, Thundaga aparecia em 67% (empate numérico entre idênticas). Com e3: Blizzara 25,7%, Blizzard 11,5%, Firaga 12,5%, Thundaga 38,9%.

## Conclusões
- A diferenciação funciona: Fogo, Gelo e Raio passam a ser escolhas diferentes.
- O Slow vale mais que +20% de dano; ele puxa o uso do Gelo. Se for adotado, reduzir o dano do Gelo mais, ou limitar o Slow aos tiers 1–2.
- Efeito colateral: Red Mage/Viera +6 a +8 pp, porque usa Blizzard. Black Mage −3,6 (inconclusivo, <5 pp). Compensar no Red Mage antes de adotar.
- Raio em área r2 e MP menor quase não mudam o uso; Raio precisa de outra identidade.
- Próximo teste de dados: Raio com "Delay Unit" dependente do dano (já existe, Earth Veil); o simulador precisa modelar atraso de turno.
- Fora de dados (exige ASM/expansão, não testado): reação em cadeia entre elementos (Fogo seguido de Gelo no mesmo alvo = bônus), Raio que ignora altura/atinge em linha.
