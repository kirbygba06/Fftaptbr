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
| Equipamento (parcial) | categorias de item não identificado (idx 686–715: Espada?, Armadura?…) e ~190 armas: espadas, facas, cajados, bastões, maças, arcos, lanças, instrumentos, garras, almas e armas de fogo (nomes 124–375; lendárias como Excalibur ficam) |
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
