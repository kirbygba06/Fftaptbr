# FFTA – proposta de rebalanceamento e mecânicas novas

Base: `ANALISE.md`. Números exatos em `proposta_classes.csv`, `proposta_itens.csv`, `proposta_magias.csv` (gerados por `proposta.py`, não alteram a ROM).
Legenda de esforço: **[D]** só dados (edita tabela, sem código) · **[H]** hook de código pequeno (achar a rotina e trocar uma constante/fórmula) · **[N]** código novo.

## 0. Objetivos de design
1. **Cada classe com identidade** (hoje todas crescem ~10% da base: só mudam as bases).
2. **Ações valem mais que MP** – nenhuma classe domina por agir o dobro.
3. **JP/Totema/Combo como decisão**, não botão de vitória.
4. **Equipamento relevante em todas as faixas**: arma não deve dar 2–4× dano; armadura deve pesar.
5. **Progressão (AP) ligada ao poder** das habilidades.
6. Manter o ritmo do jogo (não virar outro jogo); mudanças medidas e reversíveis.

## 1. Fase A – só números **[D]**
### 1.1 Papéis de classe e crescimento (`proposta_classes.csv`)
Cada uma das 42 classes jogáveis recebe um papel e multiplicadores sobre o crescimento (bases ficam):
| Papel | Classes | HP | MP | ATK | DEF | PM | RM | Mov/Jmp | Res. status |
|---|---|---|---|---|---|---|---|---|---|
| Guardião | Soldier, Paladin, Templar, Defender, Warrior, Mog Knight, Gadgeteer | ×1,12 | ×0,9 | ×0,98 | ×1,12 | ×0,92 | ×1,05 | 3/2 | 65 |
| Atacante | Fighter, Dragoon, Gladiator, Sniper, Hunter, Archer, Gunner | ×0,98 | ×0,9 | ×1,10 | ×0,95 | ×0,90 | ×0,95 | 4/3 | 50 |
| Ágil | Thief, Ninja, Assassin, Fencer, White Monk, Juggler | ×0,92 | ×0,95 | ×1,02 | ×0,92 | ×0,98 | ×0,96 | 5/4 | 35 |
| Mago | Black/Red Mage, Illusionist, Elementalist, Summoner, Alchemist, Sage | ×0,92 | ×1,0 | ×0,88 | ×0,92 | ×1,12 | ×1,10 | 3/2 | 45 |
| Apoio | White/Time Mage, Bishop, Animist, Beastmaster, Morpher, Blue Mage | ×1,0 | ×1,0 | ×0,92 | ×1,0 | ×1,05 | ×1,12 | 4/2 | 60 |
Efeito no nível 50 (máx/mín entre classes): HP 1,81→2,16 · ATK 1,71→2,02 · DEF 1,55→1,78 · PM 1,82→2,15. Classes passam a ter forças e fraquezas reais.
Mov/Jump e resistência a status deixam de ser iguais: ágeis andam 5, guardiões 3; ágeis resistem pouco a status e guardiões muito.

### 1.2 Velocidade comprimida
Base ← 100 + 0,7·(base−100); crescimento ← 1,2 + 0,5·(cresc−1,2). Spread no nível 50 de **1,91× para 1,47×** (Assassin ~244 → ~209; Sage ~128 → ~144). Rápido continua rápido, sem ter o dobro de turnos.

### 1.3 Armas (`proposta_itens.csv`)
- ATK comprimido: `novo = 30 + (ATK−15)·0,55` (15–87 vira 30–70). Dano de um ataque comum (lutador nível 50): arma mais fraca 47→87, mais forte 306→224. A arma continua importante mas o teto (4×) cai para ~2,6×.
- Preço pelo ATK: `300·(ATK/36)^6` arredondado a 50. Isso elimina as 22 armas "dominadas" (Paraiba Blade 22.000→550; Tiptaptwo 27.000→650; Estreledge 25.000→9.450; Masamune 25.000→5.250).
- Venda = 50% do preço para todos (corrige os 10 itens que vendiam por 500).
Obs.: armas existem também para ensinar habilidades; esse vínculo (`+0x1D`) não muda.

### 1.4 Armaduras
DEF ×1,7 e RES ×1,5 em todos os slots de equipamento defensivo (limite 255). Um conjunto completo passa de ~184 para ~310 de DEF (≈−30% de dano físico recebido, hoje −18%). Escudos e acessórios continuam pequenos: ver ideias de efeitos em 3.

### 1.5 Magias (`proposta_magias.csv`)
Fire/Thunder/Blizzard 30/6 MP (igual), tier 2 passa de 40/12 para **50/14**, tier 3 de 50/24 para **80/30**. Cure 40/6, Cura 65/14, Curaga 95/28. Isso faz o tier 3 valer o AP (300) e o MP; hoje o ganho de 30→50 de poder custa 4× o MP.
Junto, para MP voltar a importar: **crescimento de MP de classes mágicas ×0,75** (Sage ~471 → ~350 no nível 50) – pendente de aplicar no CSV.

### 1.6 AP e Totema
- AP: 100 / 200 / **400** (tier 3), capstones 600–990. Hoje 100/200/300 sem relação com o poder.
- Totema: poder 85 → **65** (continua forte; passa a não ser a melhor opção sempre).

## 2. Fase B – pequenos hooks de código **[H]**
Cada item exige primeiro achar a rotina (ver seção 5, "como achar").
1. **JP em Combo**: `(10 + 4·JP)/10` → `(10 + 2·JP)/10` e teto de JP útil em 5 (×2 em vez de ×3 a ×5).
2. **Hunting**: matar dá **3 JP** em vez de 10 (o guia chama de provável bug).
3. **Double Sword**: segundo golpe a **60%** do dano (o guia: "ataques comuns batem duas vezes").
4. **Haste**: soma ×1,5 da velocidade em vez de ×2.
5. **Flanqueamento**: o jogo já calcula frente/lado/costas para evade. Acrescentar dano ×1,25 pelas costas, ×1,12 pelo lado. Cria valor de posicionamento sem código novo de sistema.
6. **Recuperação de MP**: +4% do MP máximo no início do turno de cada unidade (combina com 1.5).
7. **Custo de turno**: ação 200 → 250 (ritmo ligeiramente mais lento, menos "ações por turno" de classes rápidas).

## 3. Fase C – mecânicas novas
### 3.1 Sem código novo: recombinar efeitos **[D]**
O guia lista 207 efeitos reutilizáveis; cada habilidade tem 4 slots de efeito e flags. A ROM tem 453 registros de habilidade, vários vazios/ignorados (ids `-`) e ~125 só de monstros/sistema. Dá para criar habilidades novas **só com tabela**:
- **Golpe Duplo** (Fighter): dano 1× + Delay no alvo (efeito 0x1C) · **Cortina** (Illusionist): Shell+Protect na área · **Punhal Venenoso** (Thief): dano + Poison · **Marca de Caça** (Hunter): Weakness/Defense Down no alvo · **Bênção Rápida** (White Mage): Regen+Haste curto.
Limite: o nome/descrição são texto (nós controlamos a tradução); animação reaproveita as existentes.

### 3.2 Traços raciais **[D]**
Via tabela de classes e resistências elementais (campo `+0x12`): Hume equilibrado; Bangaa +HP/+ATK, −Vel; Nu Mou +MP/+PM, fraco a físico; Viera +Vel/+Evade, fraca a Dark; Moogle +RM, fraco a Wind.

### 3.3 Equipamentos com identidade **[D]**
Os efeitos de equipamento (`+0x1A..0x1C`) já têm resistência, absorção e anulação elemental, anulação de status, auto-Reraise/Reflect. Redistribuir: cada acessório/escudo com 1 efeito claro (ex.: "Anel do Gelo": anula Ice; "Escudo Espelho": Auto-Reflect), em vez de bônus pequenos de DEF.

### 3.4 Novas classes **[D+]**
Há 115 slots de classe na ROM, ~42 usados por jogadores. Uma classe nova = registro de classe + kit de habilidades (3.1) + requisitos; reaproveita sprite de outra (paleta/nome próprios). Ex.: **Duelista** (Fencer + Soldier), **Cantor de Guerra** (buffs de grupo). Risco: tela de troca de classe e requisito exigem checar tabelas auxiliares.

### 3.5 Sistemas novos **[N]**
Só se as fases A–C.1 deixarem espaço de design:
- **Ponto de Vantagem por lei**: JP perde peso e passa a dar 1 efeito situacional por batalha.
- **Reação de grupo** (ex.: "Cobertura": aliado adjacente absorve parte do dano).
- **Fadiga/Quebra de guarda** (variável por unidade, fica na RAM da batalha, não no save).
Exigem código novo e espaço (seção 4). Não recomendado antes de provar o pipeline de hooks.

## 4. Espaço na ROM e aumento de tamanho
**Situação real (ROM original, 16 MB):**
- Livre contínuo: `0xD97728–0xFE0000` = **2,4 MB** (`0xFF`). Nossa tradução usa `0xF00000–0xFF5F20` (~1 MB). **Sobram ~1,4 MB** em `0xD97728–0xEFFFFF` que o patch ainda nem toca, mais ~40 KB no fim.
- Os 4 outros idiomas (alemão, francês, espanhol, italiano) são texto inutilizado no slot inglês. Dá para reaproveitar **vários MB** (não medi; o patch italiano já sobrescreve parte).
- Dados de classes/itens/habilidades são editáveis no lugar: **fase A não gasta espaço**.

**Expandir para 32 MB?** Tecnicamente possível, mas hoje desnecessário. Pontos:
1. O espaço de endereços do GBA vai a 32 MB (`0x08000000–0x09FFFFFF`); emuladores (mGBA, RetroArch) aceitam. Pokémon hacks usam 32 MB. Cartucho real exigiria flash de 32 MB.
2. **IPS não alcança além de 16 MB** (offset de 3 bytes). Precisaria de patch BPS/UPS (RetroArch aplica `.bps`; não sei se o My Boy! aplica – testar) ou entregar a ROM já expandida.
3. Código GBA usa ponteiros de 32 bits; chamadas `bl` de THUMB alcançam ±4 MB, então o código novo longe do original precisa de pequenos trampolins (`ldr`/`bx`). Normal, mas é mais trabalho.
4. **Risco desconhecido**: se o jogo valida ponteiros com `(p >> 24) == 8` ou usa só 24 bits de offset em alguma tabela, endereços ≥ `0x09000000` quebram. Teste: pôr uma string em `0x09xxxxxx`, apontar um texto para ela e ver se aparece.
5. O save é **Flash 64 KB** (`FLASH512_V130`); não depende do tamanho da ROM. O limite real para mecânicas novas é o **save**, não a ROM: estado novo que persista (ex.: pontos de classe) precisa caber nos bytes livres das estruturas existentes.
**Recomendação**: usar os ~1,4 MB livres + idiomas reaproveitados; ficar em 16 MB e IPS. Expandir só se código novo + gráficos exigirem, depois de passar o teste do item 4.

## 5. Como fazer (pipeline e pontos de entrada)
- Ferramentas disponíveis aqui: `clang`/`llvm-mc` (THUMB/ARM), `capstone` e `keystone` via pip. Falta um emulador estável (o mGBA headless falhou); testes ficam com você, com variantes A/B/C como na tradução.
- **Achar rotinas**: o código referencia as tabelas por ponteiro literal. Já achados na ROM: tabela de classes referenciada em `0xCBEF0, 0xCC6E0, 0xCC73C, 0xCCE94, 0x133B7C…`; itens em `0x2C4D8, 0x39064, 0x392AC…`; habilidades em `0x24540, 0x248C4, 0x26B9C, 0x27E88…`. As constantes de dano do guia (307/256, 358/256, 384/256) provavelmente são `mul/lsr` no código de batalha; localizar pelas referências acima.
- **Hello hook**: primeiro prova mínima (trocar uma constante, ex.: Hunting 10→3 JP) e ver no jogo. Só depois seguir.
- Entrega: gerar IPS separado `FFTA_balance.ips` aplicado sobre o patch de tradução (nunca juntos no mesmo arquivo).

## 6. Roadmap
| Fase | Conteúdo | Esforço | Risco |
|---|---|---|---|
| F1 | 1.1–1.6 aplicadas por IPS (script gera os bytes) | baixo | baixo (reversível) |
| F2 | Hello hook + hooks 2.1–2.4 | médio | médio |
| F3 | Flanqueamento, MP regen, custo de turno | médio | médio |
| F4 | Habilidades novas por recombinação, traços raciais, acessórios | médio | baixo |
| F5 | Classe nova, sistemas [N], expansão se precisar | alto | alto |

## 7. Decisões que dependem de você
1. **Intensidade**: rebalance leve (só F1) ou profundo (F1–F4)?
2. **Dificuldade**: manter o jogo como está de desafio ou mais difícil? (Aqui o jogador é nerfado em JP/Totema/armas de saque.)
3. **Jogar com variantes**: posso gerar F1 em 3 variantes (A só classes, B só itens/armas, C só magias) para você testar e apontar o que sentiu.
4. **Texto novo**: habilidades/classes novas precisam de nome PT-BR; posso traduzir direto.
