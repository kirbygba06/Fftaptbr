# Análise de balanceamento – status

## Verificado nos números da ROM
1. **Itens: 375**, dos quais **225 têm preço de compra 0** (só aparecem como saque/recompensa; não existem em loja).
2. **Preço de venda ≠ metade da compra em 10 itens**: Estreledge, Tiptaptwo, Masamune, Princess Rod, Hunt Bow, Seventh Heaven,
   Temple Cloth, Bracers, Star Armlet e Elixir valem 15.000–40.000 na compra mas **vendem por 500**.
   (Elixir: compra 20.000, venda 500.) Itens comuns vendem por metade do preço.
3. **Preço não acompanha poder**: dentro de uma mesma família o campo de poder (`+0`) sobe de forma irregular
   (ex.: Espadas 17, 25, 30, 35 e depois 39, 36, 18…), e os itens mais caros nem sempre são os mais fortes.
   Itens baratos de início de família aparecem com valores altos (Jack Knife 77 por 200 gil), o que pode ser outro campo
   (a confirmar antes de concluir "quebrado").
4. **Itens de recuperação**: Potion 50, Hi-Potion 200, X-Potion 700, Ether e Elixir só em loot/preço absurdo (Elixir 20.000).

## Ainda não decodificado (próximos passos)
- Classes: HP/MP/atributos base e crescimento, equipamento permitido, conjuntos de habilidades (tabela de 28 bytes em `0x710E0C` é a candidata; campos de crescimento ainda por identificar).
- Habilidades: poder, custo de MP, AP para aprender, alcance, elemento, status, fórmula.
- Curvas de EXP/AP, drop de monstros, dificuldade das missões, leis/juízes.
- Fórmulas de dano no código ARM/THUMB.
