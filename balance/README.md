# FFTA – projeto de balanceamento e novas mecânicas

Projeto separado da tradução. Aqui ficam as ferramentas que leem os números da ROM **original** (AFXP) e a análise de balanceamento.
Defina `FFTA_ROM=/caminho/da/rom.gba` (ou edite `romlib.py`).

## Mapa de dados (descoberto por varredura; sem documentação externa)
| Dado | Endereço | Registro | Estado |
|---|---|---|---|
| Itens (375) | `0x6E0BC0` (índice 1..375) | 32 bytes | decodificado em parte |
| Tabela com nome/descrição por id (jobs/monstros, ids 2..) | `0x710E0C` | 28 bytes | campo `+12` = id do nome (`NAMES`), `+14` = descrição; demais campos **ainda não decodificados** |
| Nomes de itens/classes/monstros | `0x724C34` (ponteiros) | – | – |
| Nomes de habilidades/menu | `0x720D44` (ponteiros) | – | – |

### Registro de item (32 bytes)
`+0` poder (ATK/DEF, a confirmar) · `+1` res (a confirmar) · `+2..7` bônus de atributos · `+8` e `+24` subtipo · `+16` u16 nome (índice em `0x724C34`)
· `+18` u16 descrição · `+20` u16 preço de compra (0 = não vendido em loja) · `+22` u16 preço de venda · `+27` categoria de equipamento.

## Arquivos
- `romlib.py` leitura da ROM e decodificação de textos · `items.py` exporta `items.csv`
- `ANALISE.md` achados até agora
