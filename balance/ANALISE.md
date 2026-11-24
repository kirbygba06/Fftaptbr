# Como o balanceamento do FFTA funciona – análise com os números da ROM

Fontes: tabelas lidas da ROM (classes, itens, habilidades), conferidas com o Mechanics Guide (Terence) e o Ability FAQ (NeoBlitz).
"[ROM]" = lido direto da ROM; "[Guia]" = fórmula documentada pelo guia; "[Cálculo]" = conta minha; "[Hipótese]" = não verificado em jogo.

## 1. A fórmula central
[Guia] `Dano = (Att − Def/2) × Poder/100`, com Att = atributo da classe + bônus de equipamento (máx. 999).
Para ataques com arma, **Poder = o ATK da arma**. Ou seja, o ATK da arma entra duas vezes: soma no Att e multiplica o resultado.
Para magia, Poder é fixo da habilidade (Fire 30, Fira 40, Firaga 50, Flare 65…) e o Att é o Poder Mágico.

[Cálculo] Lutador nível 50 (ATK 547) contra Soldado (DEF 524 + 40 de armadura), ataque comum:
| ATK da arma | 17 | 30 | 45 | 60 |
|---|---|---|---|---|
| dano | 48 | 88 | 140 | 195 |

A arma decide quase todo o dano. [ROM] ATK de armas vai de 15 a 87 (Excalibur2 87, Ebon Blade 84, Masamune 100 79). A melhor arma vendida em loja é a Estreledge (77, 25.000 gil) e a Masamune (65, 25.000); o resto das lojas fica em ≤46.
Armadura: [ROM] o melhor DEF por slot é Armor 58, Clothing 42, Robe 32; somando todos os slots dá ~184. [Cálculo] +120 de DEF reduz o dano de uma arma 45 de 149 para 122 (−18%). Útil, mas bem menos decisivo que a arma.

## 2. Crescimento: todas as classes têm a mesma "forma"
[ROM] Em todas as classes humanoides o crescimento por nível é ~10% da base (ex.: Soldier ATK 88 / +8,8; Fighter 92 / +9,2). Atributos nível 50 ≈ 5,9× o nível 1. A diferença entre classes é só a base: no nível 50 o melhor/pior fica em 1,5–1,9× por atributo (ATK 571 Dragoon vs 333 Time Mage). Não há classes que "crescem diferente" (ex.: HP lento no início e forte no fim).
Exceção: **Velocidade**. Base ~100 e crescimento só +0,8 a +2,3 por nível (Assassin 125/2,3 → ~244 no nível 50; Sage 85/0,8 → ~128). A velocidade depende quase só da classe.
[ROM] Mov 3–4 e Jump 2–4 para quase todas as classes jogáveis; resistência a status = 50 para todas as classes jogáveis. Mobilidade e status não diferenciam classe nenhuma.

## 3. Economia de turnos (o verdadeiro "meta")
[Guia] A cada tick o contador soma a Velocidade; ao chegar em 1000 age. Custo do turno: 500 + 300 se mover + 200 se agir (1000 se mover e agir). Quem só espera paga 500 e volta em metade do tempo. Haste soma o dobro da velocidade; Slow soma metade; Quick dá turno imediato.
[Cálculo] Assassin (244) age ~1,9× mais que Sage (128). Haste (Time Mage, 200 AP, 24 MP) dobra isso. Como o dano por ação é parecido entre classes, **quem age mais bate mais**: Assassin, Ninja (229), Thief (204–209), Hunter/Sniper (≈200) são as classes de maior valor por número de ações. Monstros: Masterberry 165/1,9 (~266 no nível 50) e Tonberry 148 são os mais rápidos do jogo.

## 4. Magia: MP não é o limite, ações são
[ROM] MP no nível 50: Sage ~471, Alchemist ~462, Illusionist ~421; Fencer/Gunner ~62.
[Cálculo] Um mago de 470 MP lança ~19 Firaga (24 MP). Uma batalha dá poucas ações por unidade, então para mago o MP raramente trava [Hipótese: MP volta cheio a cada batalha]. Logo o que importa é dano por **ação**:
| Magia (MP) | Fire 6 | Fira 12 | Firaga 24 | Flare 36 | Totema 0 |
|---|---|---|---|---|---|
| dano (mago nível 50 vs alvo com RM 480) | 71 | 95 | 119 | 155 | 202 |
Os níveis baixos são muito mais eficientes em MP (Fire 5,0 poder/MP; Firaga 2,1), mas o tier alto ganha por ação e pela área (r1/v3). Resultado: se MP sobra, **Fire/Cure (100 AP) são redundantes** depois que se aprende o tier 3 (300 AP).
[ROM] Piores relações poder/MP: Tempest/Star Cross/Deluge/Soil Evidence/Wild Tornado (poder 17, 32 MP; 0,5 por MP), Meteor (50 poder, 40 MP), Madeen (52, 36), Angel Whisper (30, 24), Saint Cross (35, 24).

## 5. JP, Combos e Totema: onde o jogo quebra
[Guia] JP se ganha seguindo as leis recomendadas e derrubando unidades. JP é gasto em Combo e Totema.
- **Combo**: ignora Reações, nunca erra o golpe final e, se algum aliado encadear, `Multiplicador = [(100% + soma dos combos) × (10 + 4·JP)/10]`.
  [Cálculo] 5 JP = ×3; 10 JP = ×5 (já com 1 aliado); máximo documentado 860%. "Mesmo o chain mais fraco com 10 JP multiplica por 5; 5 JP equivale a qualquer Ultima" (guia).
- **Totema**: poder 85 em **todos os inimigos**, alcance infinito, 100% de acerto, sem MP [ROM]. Dano ~202 no exemplo, contra 119 de um Firaga, e acerta todo o mapa.
- **Hunting**: matar com Hunting dá **10 JP em vez de 1** [Guia, marcado como possível bug]. Dá 10 JP direto, o suficiente para Combo ×5 ou Totema.
Conclusão: a economia de JP é o poder real do jogo e é desligada das classes; o resto é detalhe. Tudo depende de lei + JP, não de habilidade.

## 6. AP e progressão de habilidades
[ROM] O custo de AP só tem 100 / 200 / 300 (e 999 para as sete capstones). [Guia]: 300 AP ×142, 200 AP ×137, 100 AP ×79, 999 AP ×7, 400 AP ×1.
O custo não reflete o poder: Fire e Cure custam 100, o tier 3 custa 300 sem importar o ganho.
Maior custo de classe: Hunter e Sage 3.499 AP; Beastmaster 3.300; menor: Blue Mage 1.100 (aprende por Learning, não por AP) e Gunner 1.800.
As capstones (999 AP): Double Sword (Ninja), Ultima Shot (Hunter), Ultima Sword (Gladiator), Ultima Blow (Sage), Doublecast (Red Mage), Ultima Masher (Assassin), Ultima Charge (Mog Knight).
- **Double Sword**: ataques comuns batem duas vezes [Guia]. **Doublecast**: duas magias por turno. Ambas dobram ações por turno por 999 AP, sem MP extra.

## 7. Itens
[ROM] 376 registros; 252 armas, 102 delas compráveis; **225 de 375 itens não existem em loja** (só saque/recompensa). Almas (Morpher) 0 compráveis.
- Preço de compra e venda: normal = venda 50%. **10 itens caros vendem por 500**: Elixir (compra 20.000), Hunt Bow (40.000), Temple Cloth (30.000), Tiptaptwo (27.000), Masamune e Estreledge (25.000), Seventh Heaven (23.000), Princess Rod (20.000), Bracers e Star Armlet (15.000).
- **22 armas de loja são piores e mais caras** que outra arma do mesmo tipo e alcance (ex.: Paraiba Blade 33 ATK a 22.000 vs Sun Blade 37 a 3.000; Tiptaptwo 35 a 27.000 vs Khukuri 37 a 5.000; Ogun Blade 42 a 15.000 vs Icebrand 42 a 8.000). Muitas existem para ensinar uma habilidade, não pelo ATK.
- Preço não acompanha ATK: bucket 30–39 ATK custa em média 6.700 e vai até 40.000; 40–49 média 10.900.
- Escudos dão ≤10 de DEF (+15 Evade no máximo); Anéis/acessórios ≤4 de DEF; Ribbon/Cachusha 2: a maior parte dos slots de equipamento é pouco relevante em números.

## 8. Resumo do que é inútil e do que é quebrado
**Quebrado / dominante**
1. JP → Combo ×3 a ×5 e Totema; Hunting dando 10 JP.
2. Turnos: Haste, Quicken, Velocidade alta fixa por classe (Assassin/Ninja/Thief) e Double Sword/Doublecast (999 AP).
3. Poder da arma elevado ao quadrado (ATK soma e multiplica): armas de saque 70–87 contra 17–46 de loja fazem a diferença de 2–4× dano.
4. Totema: dano em todo o mapa, 100% de acerto, sem custo de MP.
**Inútil / quase irrelevante**
1. Tiers baixos de magia depois do tier 3 (se MP sobra); status resist (50 fixo), Mov/Jump quase iguais, crescimento sem identidade.
2. 22 armas de loja dominadas; 10 itens que não vale vender; Elixir a 20.000.
3. Equipamentos de DEF/RES pequenos (escudo, anel, ribbon) e armadura frente à arma.
4. Ability kits com AP chato (100/200/300) sem relação com o poder.
**Observação**: tudo aqui é número e fórmula. O que o balanceamento "sente" em jogo (dificuldade das missões, IA, drops) ainda não foi medido.
