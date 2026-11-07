import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

if '"^ajuda"' not in code:
    code = code.replace("vigiar-tela", "vigiar-tela|ajuda")
    bloco = '''        "^ajuda" {
            $Synthesizer.SpeakAsync("Exibindo catalogo completo de comandos da Skynet.") | Out-Null
            return @"
=== ARSENAL COMPLETO SKYNET ===
[SISTEMA & HARDWARE]
- raio-x : GPU, espaco em disco e top processos RAM
- saude-ssd : Saude fisica, temperatura e desgaste dos discos
- limpar-ram : Libera memoria RAM ociosa
- otimizar-windows : Limpa DNS, pasta TEMP e alivia RAM
- destravar-pc : Encerra janelas congeladas (Nao Respondendo)
- servicos / reiniciar-servico: [nome] : Controla servicos Windows
- sirene / bip : Emite alerta sonoro nos alto-falantes

[VISAO, WEB & ARQUIVOS]
- ver-tela [pergunta] : Analisa o que esta na tela com IA
- vigiar-tela : Verifica erros criticos na tela
- pesquisar: [tema] : Pesquisa na web e resume por voz
- resumir-url: [link] : Le e resume qualquer pagina web
- achar-arquivo [nome] / ler-doc [caminho] : Busca e resume arquivos
- ler-area : Resume o texto copiado no Ctrl+C

[AUTOMACAO, VOZ & CLOUD]
- lembrar: [fato] : Salva na memoria permanente
- agendar: [HH:mm] [aviso] : Despertador inteligente por voz
- digitar: [pedido] : Gera e digita texto onde o cursor estiver
- criar-script: [objetivo] : Forja ferramenta .ps1 sob demanda
- executar-python: [pedido] : Roda codigo Python em sandbox
- modo-trabalho / modo-foco : Macros de produtividade
- midia-play / midia-next / vol-up / vol-down / vol-mute
- minimizar-tudo / desligar-monitor / bloquear-tela / suspender-pc
- relatorio-geral / gerar-relatorio : Balanco e exportacao CSV
- sincronizar-github / reiniciar-colmeia
"@
        }
        "^vigiar-tela" {'''
    code = code.replace('        "^vigiar-tela" {', bloco, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[OK] Comando 'ajuda' instalado no skynet_core.ps1!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core reiniciado com catalogo de ajuda ativo!")
