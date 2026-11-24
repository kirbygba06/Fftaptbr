# Balanceamento conservador por dados de habilidade

Regras seguidas: só dados já existentes; nada de novas habilidades/classes/sistemas; nenhuma fórmula global alterada; sem ASM; patches modulares (1 byte por registro) e reversíveis (não aplicar o IPS).
Arquivos: `exp_cons_result.md` (uma habilidade por vez), `diag_classes.py`/`diag_classes_raw.json` (decomposição), `exp_pacotes_result.md` (pacotes, população inteira), `patches/*.ips`, simulador em `sim2.py`.

## 1. O que a ROM deixa editar, por habilidade
Registro de 28 bytes (`0x710E04 + 0x1C·id`): **MP** (+4), **AP** (+3), **poder** (+0xB), **alcance H/V** (+6/+7), **alvo** (+8), **área H/V** (+9/+0xA), **4 efeitos** (+0xC..+0xF, IDs), **flags** (+0x10), **IA**: condição, comportamento e prioridade (+0x18..+0x1A; valor alto = o inimigo usa menos).
**Precisão de status não é um campo da habilidade.** Vem do *tipo* do efeito (AType com Evade, SType com SRes, ou "se o efeito 1 acertar") e da fórmula global. Só dá para mudá-la trocando o ID do efeito, o que foge da estratégia conservadora. Logo, MP, poder, alcance, área e prioridade da IA são os botões reais.
| habilidade | AP | MP | alcance | efeitos (ID) | IA prioridade |
|---|---|---|---|---|---|
| Rockseal | 300 | 32 | 1 (V2) | Petrify (98) | 30 |
| Charmshot | 300 | 0 | arma | dano (63) + "se o 1 acertar: Charm" (140) | 80 |
| Cupid | 200 | 0 | arma | Charm (142) | 50 |
| Fire Veil | 200 | 4 | 4 | dano (63) + "se o 1 acertar: Confusion" (93) | 80 |
| Death Sickle | 300 | 0 | arma | Doom (170) | 30 |
| Checkmate | 300 | 0 | arma | Doom (170) | 30 |
Observação: a IA dos inimigos tem prioridade 30 (a mais "provável") em Doom e Petrify. É uma alavanca que só afeta o lado inimigo; não testei porque o simulador não tem a IA original.

## 2. Mudanças no simulador (IA do simulador separada da ROM)
- **Dados confirmados incorporados** (teste comunitário, nível 25): Stop 3 turnos, Silence 3, Slow 3, Haste 3, Doom 3 até o KO, Petrify permanente até curar; Charm e Sleep terminam ao receber dano. **Suposições mantidas como parâmetro**: duração natural de Charm/Sleep/Confusion, % do Poison, Blind, Berserk etc.
- **Precisão registrada pela comunidade** (Rockseal 60%, Charmshot 95%, Cupid 80%, Checkmate 60%, Death Sickle 60%) como **Modo B**; o **Modo A** usa a fórmula do guia. Resultado de consistência: no Modo A o simulador dá ~58% para Rockseal, Checkmate e Death Sickle, bem perto dos 60% medidos.
- Charm faz a vítima atacar o próprio time; imunidade a status (Ribbon/Immunity) em 0% / 10% / 25% das unidades nos níveis 10/25/45; **Expert Guard** (dano 0, acerto 100%, 2 turnos) com valor defensivo na IA; custo de oportunidade do MP.
- **Instrumentação**: taxa de vitória, uso por classe, status aplicado por uso, impacto médio por uso (PV causado/curado) e turnos negados (valor).
- **Separação**: `sim2.AI` e `sim2.P` são parâmetros do simulador; as mudanças de ROM entram só como `mods` (MP). Original e modificado rodam com a mesma IA.
- **"Inútil" não é "a IA não escolhe"**: usei **ablação** (retirar a habilidade do kit e medir o efeito), não frequência de escolha.
- **Ruído medido**: rodando o original com duas sementes, a diferença média por classe é **2,2–2,4 pontos** (p90 4–5). Diferença menor que ~±5 pontos numa classe **não é conclusiva**.

## 3. Resultados por habilidade (ablação e passos de MP; `exp_cons_result.md`)
| habilidade | ablação (sem ela) | MP graduais | leitura |
|---|---|---|---|
| Rockseal (Assassin) | −1,5 e +0,9 (nível 45), ruído | não testado (já 32 MP, mantido) | **sem efeito mensurável isolado**; o Assassin tem Nightmare, Shadowbind etc. no lugar |
| Charmshot (Gunner) | +2,0 (!) | MP 4/8/12: +3,6/+0,8/+1,8 | **sem efeito**: Confushot, Stopshot e Silenshot substituem |
| Cupid (Archer) | −9 a −17 (nível 25), −6 a −11 (45) | MP 4/8/12: −0,3/−1,7/−3,9 (nível 25) | é a ferramenta central do Archer; MP 8 muda pouco |
| Fire Veil (Ninja) | −13 (25), −7 (45) | MP 8/12/16: −5/−7/−8 (nível 25); ±2 (45) | só importa no nível 25; as outras Veils substituem |
| Death Sickle (Sniper) | −1 | MP 8/12/16: ruído | **sem efeito**; 22–25% das ações da classe |
| Checkmate (Fencer) | −1 | MP 8/12/16: ruído | **sem efeito**; sem status o Fencer ganha mais (64% vs 59%) |

## 4. O que explica de fato as classes que mais vencem (`diag_classes.py`)
Taxa de vitória (nível 25 / 45) retirando um componente por vez:
| classe | completo | só Fight | sem status | velocidade média |
|---|---|---|---|---|
| Assassin | 60 / 72 | 54 / 50 | 54 / 50 | 50 / 62 |
| Gunner | 71 / 75 | 35 / 39 | 37 / 41 | 75 / 78 |
| Archer (Hume) | 57 / 59 | 42 / 47 | 50 / 57 | 53 / 61 |
| Ninja | 75 / 67 | 43 / 41 | 43 / 41 | 65 / 56 |
| Sniper | 62 / 60 | 54 / 49 | 52 / 52 | 60 / 54 |
| Fencer | 59 / 55 | 47 / 43 | 64 / 57 | 53 / 52 |
Leitura: o **Gunner é quase só kit** (35–39% sem os tiros, 71–75% com). **Assassin** = velocidade (+10) + família de status (+22 no nível 45). **Ninja** = família de Veils (+26–32). **Fencer não depende do status** (o Doom do kit atrapalha na simulação). Portanto o ajuste certo é por **família**, não por uma habilidade.

## 5. Pacotes testados (população inteira, níveis 10/25/45; `exp_pacotes_result.md`)
Taxa de vitória (variação vs original), efeitos acima do ruído em negrito:
| classe | nível | só tiros MP 6 (F) | Cupid 8 + tiros 6 (E) | tiros MP 10 (D) |
|---|---|---|---|---|
| Gunner | 25 | **62% (−9)** | **60% (−12)** | **55% (−17)** |
| Gunner | 45 | 70% (−4) | 70% (−5) | **67% (−8)** |
| demais classes | | dentro do ruído | dentro do ruído | dentro do ruído |
**Identidade do Gunner (nível 45, % das ações: dano / dano+status):** original 1 / 99; tiros MP 6 = 44 / 56; MP 10 = 61 / 39. Com MP 6 o Gunner continua sendo a classe dos tiros de status. Com MP 10 passa a ser mais artilharia comum.
**Equilíbrio global não muda**: desvio 0,113 → 0,106 no melhor pacote; faixa 28–75% → 31–67%. Custos de MP em poucas habilidades **não resolvem o desequilíbrio geral**, que vem de muitas classes (ver `F1_v2.md`: ajuste de atributos reduz o desvio a ~0,064).

## 6. Recomendação conservadora
1. **Rockseal: não mexer** (60% medido, 32 MP, ablação ≈ 0).
2. **Death Sickle e Checkmate: não mexer** (sem efeito mensurável; Fencer e Sniper estão em ~55–60%). Alterar MP aqui só mudaria a identidade sem ganho de equilíbrio.
3. **Charmshot/Cupid/Fire Veil individualmente: não mexer**: o MP isolado é indistinguível do ruído (Charmshot, Fire Veil) ou muda só o Archer em 2–5 pontos (Cupid).
4. **Único ajuste com efeito comprovado: tiros de status do Gunner a 6 MP** (`patches/bal01_tiros_de_status_mp6.ips`). Passo seguinte, se o jogo ainda estiver forte: `bal01b_..._mp10.ips`. Opcional e de efeito pequeno: `bal02_cupid_mp8.ips`.
Cada IPS escreve 1 byte por habilidade, não tem sobreposição com a tradução e se reverte deixando de aplicá-lo.

## 7. Limites
Reações, JP/Combo/Totema, elementos, segundo conjunto de habilidades e IA real de chefes não estão no simulador. Kit de Thief, Beastmaster, Morpher e Blue Mage não é modelável. Poison % e duração natural de Confusion/Sleep/Charm continuam suposições (o resultado do Gunner depende pouco delas: os tiros de status aplicam por dependência do dano).
**Para confirmar em jogo (Gunner)**: com `bal01_...mp6`, o Gunner ainda domina batalhas de nível 25? E fica sem MP cedo demais (MP base 8, +1,1 por nível: ~35 MP no nível 25 = 5–6 tiros)?
