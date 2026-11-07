import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

if "traduzir:" not in code:
    code = code.replace("vigiar-tela", "vigiar-tela|traduzir:|gerar-senha|energia|consultar-memoria")
    bloco = '''        "^traduzir:\\s*(.+)" {
            $TxtTrad = $Matches.Trim()
            $Payload = @{ model = "skynet:final"; prompt = "Traduza o texto abaixo para portugues (se ja estiver em portugues, traduza para ingles) de forma natural, entregando apenas a traducao:`n$TxtTrad"; stream = $false } | ConvertTo-Json
            $RespTrad = Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $Payload -ContentType "application/json" -TimeoutSec 60
            $Synthesizer.SpeakAsync($RespTrad.response) | Out-Null
            return "Traducao:`n$($RespTrad.response)"
        }
        "^gerar-senha" {
            $Chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%&*"
            $Senha = -join (1..16 | ForEach-Object { $Chars[(Get-Random -Maximum $Chars.Length)] })
            Set-Clipboard -Value $Senha
            $Synthesizer.SpeakAsync("Senha forte gerada e copiada para a area de transferencia.") | Out-Null
            return "Senha Segura (16 caracteres - ja copiada no Ctrl+C):`n$Senha"
        }
        "^energia" {
            $Os = Get-CimInstance Win32_OperatingSystem
            $Up = (Get-Date) - $Os.LastBootUpTime
            $Bat = Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue
            $BatInfo = if ($Bat) { "Bateria: $($Bat.EstimatedChargeRemaining)% (Status: $($Bat.BatteryStatus))" } else { "Alimentacao: Conectado direto na tomada (Desktop)" }
            return "=== ENERGIA & UPTIME ===`nTempo Ligado: $($Up.Days)d $($Up.Hours)h $($Up.Minutes)m`n$BatInfo"
        }
        "^consultar-memoria" {
            $MemFile = "C:\\SkynetPowerShell\\database\\memoria_mestre.json"
            if (-not (Test-Path $MemFile)) { return "Nenhuma memoria salva ainda. Use 'lembrar: [fato]'." }
            $Mems = @(Get-Content $MemFile -Raw | ConvertFrom-Json) | ForEach-Object { "[$($_.data)] $($_.nota)" }
            return "=== MEMORIA PERMANENTE ($($Mems.Count)) ===`n" + ($Mems -join "`n")
        }
        "^vigiar-tela" {'''
    code = code.replace('        "^vigiar-tela" {', bloco, 1)

    # Injeta a memoria permanente automaticamente no prompt da IA Local
    mem_hook = '''$Model = if ($InputData.modelo) { $InputData.modelo } else { "skynet:final" }
                                $MemContext = ""
                                if (Test-Path "C:\\SkynetPowerShell\\database\\memoria_mestre.json") {
                                    $Notas = @(Get-Content "C:\\SkynetPowerShell\\database\\memoria_mestre.json" -Raw | ConvertFrom-Json) | Select-Object -Last 8 | ForEach-Object { "- " + $_.nota }
                                    if ($Notas) { $MemContext = "Contexto salvo na memoria do usuario:`n" + ($Notas -join "`n") + "`n`nPergunta atual: " }
                                }
                                $OllamaPayload = @{ model = $Model; prompt = ($MemContext + $RawText); stream = $false } | ConvertTo-Json'''
    old_ollama = '''$Model = if ($InputData.modelo) { $InputData.modelo } else { "skynet:final" }
                                $OllamaPayload = @{ model = $Model; prompt = $RawText; stream = $false } | ConvertTo-Json'''
    code = code.replace(old_ollama, mem_hook, 1)

    core_p.write_text(code, encoding="utf-8")
    print("[OK] Tradutor, Gerador de Senhas, Energia e Memoria Contextual instalados!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core reiniciado com inteligencia contextual!")
