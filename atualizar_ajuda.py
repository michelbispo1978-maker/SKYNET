import pathlib, re, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

novo_bloco_ajuda = '''        "^ajuda$" {
            $Catalogo = @"
=== CATALOGO COMPLETO SKYNET FUSAO TOTAL ===

[INTELIGENCIA COGNITIVA & VISAO]
- analisar-tela: [pergunta] -> Le o texto da tela (OCR) e responde com a IA
- aprender-pasta: [caminho] -> Indexa documentos/codigos para consulta (RAG)
- plano: [objetivo] -> Cria e executa sequencia autonoma de comandos
- ver-tela | vigiar-tela -> Captura print da tela e monitora alteracoes
- traduzir: [texto] -> Traduz PT/EN e narra o resultado em voz alta

[MEMORIA & PRODUTIVIDADE]
- lembrar: [fato] -> Salva informacao na memoria permanente da IA
- consultar-memoria -> Lista todas as anotacoes salvas
- gerar-senha -> Gera senha forte de 16 caracteres e copia (Ctrl+C)
- ler-area -> Le o conteudo atual da area de transferencia
- pesquisar: [termo] | resumir-url: [link] -> Busca e resume conteudo web
- historico -> Exibe os ultimos logs e comandos executados

[REDE & HARDWARE]
- velocidade-net -> Mede download (Mbps) e ping em tempo real
- rede-wifi -> Mostra IP local, IP publico e dispositivos na rede
- raio-x | saude-ssd | energia -> Diagnostico de CPU, RAM, SSD e Uptime
- brilho: [0-100] -> Ajusta o brilho da tela (notebooks/monitores WMI)

[OTIMIZACAO & CONTROLE DO PC]
- limpar-ram | otimizar-windows | destravar-pc -> Limpeza e fluidez
- modo-trabalho | modo-foco | minimizar-tudo -> Atalhos de ambiente
- vol-up | vol-down | vol-mute | midia-play | midia-next -> Audio/Midia
- bloquear-tela | desligar-monitor | suspender-pc | sirene -> Seguranca

[COLMEIA & NUVEM]
- sincronizar-github -> Salva a versao atual blindada no GitHub
- reiniciar-colmeia | gerar-relatorio -> Manutencao e relatorio geral
"@
            return $Catalogo
        }'''

if '"^ajuda$"' in code:
    code = re.sub(r'        "\^ajuda\$"\s*\{.*?^\s*\}', novo_bloco_ajuda, code, count=1, flags=re.S | re.M)
else:
    code = code.replace('        "^historico" {', novo_bloco_ajuda + '\n        "^historico" {', 1)

core_p.write_text(code, encoding="utf-8")
print("[OK] Catalogo completo atualizado no comando 'ajuda'!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado! Clique em ❓ Ajuda ou envie 'ajuda' no Telegram.")
