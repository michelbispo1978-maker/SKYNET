import pathlib, re, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

# 1. Adiciona atalhos compostos 'status-total' e 'limpar-tudo' + atualiza 'ajuda'
if "status-total" not in code:
    code = code.replace("win11-restaurar", "win11-restaurar|status-total|limpar-tudo")
    bloco_macros = r'''        "^status-total$" {
            $H = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
            $Doc = try { (Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $H -Body '{"entrada":"doutor-skynet"}' -TimeoutSec 20).resultado } catch { "" }
            $Rx  = try { (Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $H -Body '{"entrada":"raio-x"}' -TimeoutSec 20).resultado } catch { "" }
            return "$Doc`n`n$Rx"
        }
        "^limpar-tudo$" {
            $H = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
            $Fax = try { (Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $H -Body '{"entrada":"faxina-win11"}' -TimeoutSec 30).resultado } catch { "" }
            $Org = try { (Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $H -Body '{"entrada":"organizar-desktop"}' -TimeoutSec 20).resultado } catch { "" }
            [System.GC]::Collect()
            Falar-Skynet("Limpeza geral e organizacao concluidas.")
            return "$Fax`n$Org`nMemoria RAM liberada."
        }
        "^win11-restaurar$" {'''
    code = code.replace('        "^win11-restaurar$" {', bloco_macros, 1)

catalogo_mestre = r'''        "^ajuda$" {
            $Catalogo = @"
=== ARSENAL COMPLETO WINDOWS 11 + SKYNET ===

[MACROS & SISTEMA WIN 11 ENXUTO]
- status-total | limpar-tudo -> Boletim completo e faxina geral em 1 comando
- win11-essencial | win11-restaurar -> Deixa so o necessario rodando no Win 11
- startup-listar | startup-otimizar | startup-usar: [app] | startup-pausar: [app]
- doutor-skynet -> Auto-diagnostico e auto-cura de todas as portas e servicos
- eventos-erro -> Diagnostica ultimos erros criticos do Windows 11 com IA
- faxina-win11 | organizar-desktop -> Limpa caches SSD e arruma icones do Desktop

[CONTROLE DE JANELAS, HARDWARE & UI AUTOMATION]
- janela-ativa | focar: [app] | posicionar: [esquerda|direita|maximizar]
- clicar-texto: [botao] | digitar-na-tela: [texto] | abrir: [app/config]
- nova-area | desktop-esq | desktop-dir -> Areas de trabalho virtuais
- modo-turbo | volume: [0-100] | mudo | brilho: [0-100] | dispositivos
- matar-app: [nome] | servico: [start|stop|restart] [nome] | ps-admin: [cmd]
- acordar-pc: [MAC] | reiniciar-pc | desligar-pc

[INTELIGENCIA COGNITIVA, VISAO & ESPECIALISTAS]
- especialista: [codigo|juridico|saude|financas|professor] | [pergunta]
- analisar-tela: [pergunta] | olhar-foto: [imagem] | ver-tela | vigiar-tela
- ler-tudo: [arquivo] | aprender-pasta: [pasta] | plano: [objetivo]
- investigar: [tema] | pesquisar: [termo] | resumir-url: [link] | analisar-copia

[MEMORIA, AGENDADOR & NUVEM]
- me-lembre: [15m ou 18:30] | [aviso] -> Alarme falado + notificacao no Telegram
- lembrar: [fato] | consultar-memoria | gerar-senha | velocidade-net | rede-wifi
- sincronizar-github | reiniciar-colmeia | gerar-relatorio
"@
            return $Catalogo
        }'''

code = re.sub(
    r'        "\^ajuda\$"\s*\{.*?^\s*\}',
    lambda m: catalogo_mestre,
    code,
    count=1,
    flags=re.S | re.M
)
core_p.write_text(code, encoding="utf-8")

# 2. Libera 'status-total' e 'limpar-tudo' no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"status-total"' not in p_txt:
        py_p.write_text(p_txt.replace('"win11-restaurar",', '"win11-restaurar", "status-total", "limpar-tudo",'), encoding="utf-8")

# 3. Garante Interface 66827 ReadOnly, reinicia motores e faz backup final seguro no GitHub
html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
if html_p.exists():
    subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[OK] Arsenal consolidado e motores reiniciados!")

backup_py = ps_dir / "backup_final_seguro.py"
if backup_py.exists():
    subprocess.run([r"C:\Users\Administrador\AppData\Local\Programs\Python\Python313\python.exe", str(backup_py)])
