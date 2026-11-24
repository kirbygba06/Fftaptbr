# FFTA – tradução PT-BR (slot inglês)

Patch IPS para a ROM **europeia** de Final Fantasy Tactics Advance (`AFXP`, 16 MB, multi-idioma).
A tradução entra no **slot do inglês**: escolha *English* na tela de idioma.

- `patches/FFTA_ptBR_slot_ingles.ips` – o patch (aplica sobre a ROM AFXP limpa **ou** sobre a que já tem os patches do italiano)
- `tools/build_patch.py` – regenera o patch (`python3 tools/build_patch.py ROM.gba`)
- `reference/` – patch de menus/status feito antes no slot italiano (fonte das traduções reaproveitadas)

## O que está traduzido
| Área | Detalhe |
|---|---|
| Menus de comando / sistema / loja / missões | mesmos textos do patch italiano v2, agora nos índices do inglês (tabela `0x720D44`) |
| Tela e menu de status | índices 717–765 (Pot./Res. Mágica, Velocidade, Sem prêmio, Cores, Tipo cursor, Padrão, Rápido…) + `Trocar Itens`, `Lento` |
| Conjuntos de habilidades | 45 nomes (idx 95–139), com "de" onde cabe (Banco de Monstros, Tormenta de Areia, Téc. de Batalha): Combate, Magia Branca/Negra/Azul/Vermelha/Temporal, Ferraria, Téc. Monge, Oração, Canção… |
| Monstros, chefes e papéis de NPC | 50 nomes (tabela de nomes, idx 2–122): Flan de Gelo, Formigaleão, Zumbi, Olho Flutuante, Wyrm de Fogo, Chefe Borzoi, Líder de Turma, Enfermeira… (nomes próprios como Ahriman, Coeurl, Tonberry, Malboro ficam) |
| Habilidades individuais | ~430 nomes (idx 140–574, incluindo os Combos): Roubar, Mirar: Pernas, Presa Venenosa, Foice Mortal, Golpe Ultima, Vida|Plena… (146, 178 e 207 têm códigos de controle e ficaram em inglês) |
| Equipamento (parcial) | categorias de item não identificado (idx 686–715: Espada?, Armadura?…) e ~310 armas, equipamentos e itens: espadas, facas, cajados, bastões, maças, arcos, lanças, instrumentos, garras, almas, armas de fogo, escudos, elmos, chapéus, armaduras, mantos, botas, acessórios e itens de uso (nomes 124–498; lendárias como Excalibur ficam) |
| Classes | 44 nomes (tabela `0x724C34`): Soldado, Lutador, Ladrão, Mago Branco/Negro/Azul/Vermelho/Temporal, Arqueiro, Paladino, Templário, Caçador, Bispo, Guerreiro, Esgrimista, Monge Branco, Domador, Alquimista, Sábio, Invocador… |

Monstros, itens, habilidades e diálogos **não** foram tocados.

## ã e õ de verdade
A fonte da ROM não tem `ã`/`õ` (o patch italiano usava `â`/`ô` no lugar). Este patch desenha glifos reais de `ã` e `õ`
sobre os glifos `ä` e `ö` (`0x4954DC + 27*128` e `+ 40*128`). Efeito colateral: **o slot alemão perde ä/ö**.
Texto novo vai em `0xFE5000` (livre; o patch italiano usa `0xFE4000–0xFE4587`).

## Formato de texto (descoberto)
- Fonte `0x4954DC`: glifos 16x16 de 128 bytes (tiles TL,BL,TR,BR, 4bpp valores 0–3); largura em `0x4F885B + código`.
- String `01`: `01` + códigos + `00`, código = glifo+1 (A=B1, a=CB, 0–9=A7–B0, `.`=E5, `,`=ED, `!`=EC, `?`=EB, FF=quebra).
- String `80`: pares `80 xx` (xx = glifo), espaço = `40 73`.
- Acentos (código 01): à19 á1A â1B ã1C é1E ê1F í22 ó27 ô28 õ29 ú2B ç30.

## Não verificado
Sem emulador no ambiente: os glifos foram conferidos renderizando a fonte da ROM, **não** no jogo.
Nomes longos (`Mago Vermelho`, `Cavaleiro Negro`, `Engenhoqueiro`) podem estourar caixas pequenas; teste.

## Convenção de magias em níveis
Fire/Fira/Firaga → `Fogo`/`Fogo+`/`Fogo++`; Thunder/Thundara/Thundaga → `Trovão`/`Trovão+`/`Trovão++`;
Blizzard/Blizzara/Blizzaga → `Gelo`/`Gelo+`/`Gelo++`; Cure/Cura/Curaga → `Cura`/`Cura+`/`Cura++`.
Elementos (nomes 646–650): Fogo, Gelo, Raio, Sagrado, Vento.

## Segunda passada (`tools/extra_translations.py`)
Magias, invocações, troféus, medalhas, minérios, materiais, comidas, itens de missão e as categorias de
habilidade da tabela de nomes (idx 499–645). Ficam como estão só nomes próprios sem tradução
(Ifrit, Shiva, Ramuh, Kirin, Adrammelech, Mateus, Famfrit, Ahriman, Coeurl, Tonberry, Masamune…),
entradas com códigos de controle e as `Dummy`.

## Diálogos / textos de ajuda (`tools/dialogue.py`, `tools/dialogue_translations.py`)
Textos longos ficam em **bancos** no inglês: `0x4FA000–0x54E000` (~2.700 strings em ~22 bancos) e mais uma região em
`0xBB1000–0xC04000`. Formato do banco: tabela de offsets u16 (relativos ao banco, termina em `FFFF`) + strings
`[cabeçalho 2 bytes][pares 80 xx | controles 40 xx][sufixo 40 61 40 63 00]`. `40 73`=espaço, `40 6E`=quebra de linha,
`40 70`=quebra de página, `81 08`=`&`, `80 FE`=hífen. Uma parte das strings é **comprimida** (códigos 40–7F misturados) e ainda
não foi decodificada: só as simples são traduzidas.
Para não quebrar referências internas, o banco original é copiado inteiro para `0xF00000+`, as traduções são anexadas no fim,
e só a tabela de offsets e o ponteiro no código (ex.: `0x16FC4`) mudam.
Traduzidos até agora (~930 textos em 16 bancos): ajuda dos comandos (`0x527704`), combos (`0x534264`), efeitos curtos (`0x521A20`), descrições de habilidade (`0x529514`), penalidades de lei (`0x54382C`), falas de loja/taverna/banco de monstros (`0x4F9744`), comandos de classe (`0x531998`), descrições de classes/monstros (`0x540368`), objetivos, mensagens de sistema, locais e opções (`tools/dialogue_misc.py`). As notícias e dicas do jornal (`0x513A8C`, 57 artigos, `tools/dialogue_news.py`) são reescritas pelo código: o texto é quebrado em linhas de até 156 px e em páginas de 7 linhas. Faltam só os textos comprimidos.

## Textos comprimidos (tentativa de decodificação, sem sucesso)
Strings "comprimidas" (ex.: `0x51EBE0`, trechos de `0x51F3E0`, `0x4FE5D4`, `0x534D9C`) começam com `00 00 00 xx yy` e depois misturam
pares `80 xx` (letras literais, só no começo: `Ramsen Ar…`) com pares cujo primeiro byte é `40/42/44/46/48/88/90/98`.
O fim da string aparece como `42 61 40 63 20` (em vez de `40 61 40 63 00`), ou seja, o primeiro byte de cada par carrega
bits extras. Testes feitos e descartados: LZ77 do BIOS (nenhum bloco `0x10` vira texto) e leitura dos pares como índices de glifo
(`(b0&0x1f)<<8|b1` cai em kana/kanji sem sentido). A rotina que desenha texto de menu (`0x12E900`, `0x12E9C8`) monta
unidades de 2 bytes `(b0<<8|b1)&máscara`, mas o decodificador dos textos longos ainda não foi achado. Sem emulador/depurador para
rastrear a leitura desses bytes, continuo sem poder decodificá-los com segurança.

### Pista nova (save state `.st0` do usuário)
Em `GBASTATE` (gzip), o diálogo "Aww, man! Why do I get stuck on the weak team?…" aparece **em texto simples** (pares `80 xx`) num buffer da
RAM (offset `0x1F734` do estado) — ou seja, o jogo descomprime para texto normal; a string correspondente **não** existe em texto simples na ROM.
Falta parear esse texto com a string comprimida da ROM. `tools/mgba_trace.lua` (não testado) registra o PC e os registradores quando o jogo escreve nesse buffer.

### Layout do save state `.st0` (gzip, `GBASTATE`) — descoberto
`0x00–0x97` cabeçalho (registradores r0–r12, sp, lr, pc, cpsr em big-endian a partir de `0x1C`), **IWRAM** em `0x98` (32 KB),
**EWRAM** em `0x8098` (256 KB), **VRAM** em `0x48098`. O diálogo descomprimido ("Aww, man!…") está em EWRAM `0x0201769C`.
Tentei retomar o jogo com o Unicorn (CPU ARM/Thumb em Python, `pip install unicorn`) a partir do estado, mas o jogo cai em código
dependente de estado de hardware que não está no save state; sem um emulador completo não consegui capturar a leitura da string comprimida.

### Limite de nomes (bug na loja)
Teste em jogo: na loja, o nome "Botas de Batalha" (16 letras, ~87 px) apareceu em branco. Como hipótese, os campos de nome têm limite de caracteres/largura
(inglês: até 15 letras e ~83 px em itens; classes até 12 letras). `tools/safe_names.py` reduz todos os nomes acima disso (ex.: `Botas Batalha`,
`Espada Prata`, `Cav. Negro`). Se a hipótese se confirmar, dá para voltar a nomes mais longos só onde o jogo aceita.

### Compressão dos textos longos — DECIFRADA (rotina da ROM em `0x54A0`, achada com mGBA + GDB)
Strings cujo cabeçalho (u16) tem o **bit 1 ligado** são comprimidas: depois do cabeçalho vêm 4 bytes (tamanho, big-endian) e um fluxo de opcodes
(LZ com literais, cópias, zeros e 0xFF). `tools/ffta_lz.py` implementa o descompressor; o resultado é o mesmo formato `80 xx`/`40 xx` dos textos simples.
Para traduzir, o gerador descomprime, troca o texto e grava a string **sem compressão** com o cabeçalho com o bit 1 desligado (`hdr & ~2`).
`tools/textbanks.py` lê os bancos (inclui os 78 bancos de história em `0xBB0748–0xC0B000`: ~8.400 entradas, ~1.960 comprimidas). Traduzido até agora com este método:
descrições de lojas/tavernas (`0x51EBE0`) e regras de batalha (`0x51F3E0`).
Como rodar o mGBA do AppImage aqui: extrair (`--appimage-extract`), `libEGL.so.1` falsa (stub em C), Xvfb, `mgba-qt -g` (GDB na porta 2345) e teclas via XTEST (`python-xlib`).

### Diálogos de história (`tools/story.py`, `tools/story_translations.py`, `tools/dump_story.py`)
O jogo acha o banco de uma cena em `P + tabela[k+1]`, com `P = 0x08BB064C` para o inglês (tabela de u32 no início de P; entrada 0 = fim).
O gerador copia o banco para `0xF40000+`, anexa as strings traduzidas (sem compressão, cabeçalho `& ~2`) e troca só o offset da tabela.
Confirmado no jogo (mGBA): o buffer de texto da primeira cena mostrou "Ah, cara! Por que sempre caio no time fraco?…".
Escala do trabalho: ~2.160 falas (~200 mil caracteres) nos bancos 0–52; traduzido até agora: bancos 0 a 16 (prólogo até o jagd, Nono, Clã Ox e Shara/Ritz).
`python3 tools/dump_story.py ROM.gba [banco]` exporta o inglês em marcação (`/` = quebra, `¶` = página, `{40 25 00}` = variável).
