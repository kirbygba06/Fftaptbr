# FFTA – projeto de balanceamento e novas mecânicas

Projeto separado da tradução. Lê os números da ROM **original** (AFXP) e analisa o balanceamento.
`FFTA_ROM=/caminho/rom.gba python3 romdata.py` (ou edite `ROM_PATH` em `romlib.py`).

## Mapa de dados (conferido: bate 100% com os guias para Soldier, Cure, Fire, preços etc.)
| Dado | Endereço (ROM AFXP) | Registro |
|---|---|---|
| Classes/monstros (115, id 0 vazio) | `0x6E5498` | 0x34 bytes |
| Itens/equipamentos (376) | `0x6E0BD0` | 0x20 bytes |
| Habilidades (id 1..0x1C4) | `0x710E04` (+0x1C·id) | 0x1C bytes |

(Os endereços do Data Crystal são da ROM USA; na AFXP estão deslocados. Estrutura dos campos: `fontes/dc_*.txt`.)

### Classe (0x34)
`+0` id do nome · `+4` raça · `+0x16` resistência a status · `+0x17` HP base · `+0x18` MP · `+0x19` Velocidade ·
`+0x1A` 3 bytes: ATK (12 bits) e DEF (12 bits) · `+0x1D` 3 bytes: Poder Mágico e Res. Mágica ·
`+0x20..0x26` crescimento ×10 (HP, MP, Vel, ATK, DEF, PM, RM) · `+0x28` Mov · `+0x29` Jump · `+0x2A` Evade ·
`+0x12` u32 elementos (3 bits cada: 0 fraco, 1 normal, 2 anula, 3 absorve, 4 resiste) · `+0x2D` índice de equipamento permitido.

### Item (0x20)
`+0` nome · `+2` descrição · `+4` compra · `+6` venda · `+8` tipo · `+9` elemento · `+0xA` alcance · `+0xB` onde equipa ·
`+0x10` ATK · `+0x11` DEF · `+0x12` Poder · `+0x13` Res · `+0x14` Vel · `+0x15` Evade · `+0x16` Mov · `+0x17` Jump ·
`+0x1A..0x1C` efeitos (resistências, imunidades...) · `+0x1D` habilidade que ensina.

### Habilidade (0x1C)
`+0` nome (índice no menu +1) · `+2` elemento · `+3` AP÷10 · `+4` MP · `+5` exige arma · `+6/7` alcance H/V · `+8` alvo ·
`+9/0xA` área H/V · `+0xB` poder · `+0xC..0xF` 4 efeitos · `+0x10` flags u32 · `+0x14` animação · `+0x16` descrição · `+0x18..0x1A` IA.

## Arquivos
- `romlib.py`, `romdata.py` leitura da ROM → `jobs.csv`, `items.csv`, `abilities.csv`
- `parse_abilities.py` (efeitos de cada habilidade, do Mechanics Guide) → `abilities.json`
- `parse_faq.py` (habilidades por classe, item que ensina, AP) → `class_abilities.json`
- `parse_growth.py` → `growth.json`
- `fontes/` guias usados (Mechanics Guide v0.95 de Terence Fergusson; Ability FAQ de NeoBlitz; páginas do Data Crystal)
- `ANALISE.md` análise de balanceamento

**Tudo acima é editável por IPS no lugar** (mesmos tamanhos de tabela), sem gastar espaço livre da ROM.
