-- Script de rastreio para o mGBA (PC, versão 0.10 ou mais nova): Tools > Scripting > File > Load script.
-- NÃO foi testado por mim (sem emulador no ambiente). Objetivo: descobrir de onde o jogo lê o texto comprimido.
--
-- Como usar:
--  1) carregue um save state tirado ANTES de a caixa de diálogo abrir;
--  2) carregue este script (ele fica esperando);
--  3) avance até o diálogo aparecer; o script grava em 'ffta_trace.txt' (pasta do mGBA) os endereços de ROM lidos,
--     o PC da rotina que escreve o texto e os registradores.
local WATCH_LO, WATCH_HI = 0x02017680, 0x02017800   -- buffer do texto descomprimido (EWRAM 0x0201769C no save state; 0x1F734 era o offset no ARQUIVO .st0)
local out = io.open("ffta_trace.txt", "w")
local count = 0
local function dump(tag)
  local line = string.format("%s pc=%08X", tag, emu:readRegister("pc"))
  for r = 0, 12 do line = line .. string.format(" r%d=%08X", r, emu:readRegister("r" .. r)) end
  line = line .. string.format(" sp=%08X lr=%08X\n", emu:readRegister("sp"), emu:readRegister("lr"))
  out:write(line); out:flush()
end
for a = WATCH_LO, WATCH_HI - 1, 2 do
  emu:setWatchpoint(function()
    count = count + 1
    if count <= 4000 then dump(string.format("W[%08X]", a)) end
  end, a, C.WATCHPOINT_TYPE.WRITE)
end
console:log("ffta_trace: aguardando escritas em " .. string.format("%08X-%08X", WATCH_LO, WATCH_HI))
