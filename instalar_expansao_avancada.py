import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

if "doutor-skynet" not in code:
    code = code.replace("vigiar-downloads", "vigiar-downloads|me-lembre:|acordar-pc:|doutor-skynet|olhar-foto:")
    bloco_avancado = '''        "^me-lembre:\\s*([^|]+)\\|\\s*(.+)" {
            $Quando = $Matches[1].Trim().ToLower()
            $AvisoTxt = $Matches[2].Trim()
            $Segundos = 60
            if ($Quando -match '^(\\d+)m$') {
                $Segundos = [int]$Matches[1] * 60
            } elseif ($Quando -match '^(\\d+)h$') {
                $Segundos = [int]$Matches[1] * 3600
            } elseif ($Quando -match '^(\\d{1,2}):(\\d{2})$') {
                $AlvoHora = (Get-Date).Date.AddHours([int]$Matches[1]).AddMinutes([int]$Matches[2])
                if ($AlvoHora -lt (Get-Date)) { $AlvoHora = $AlvoHora.AddDays(1) }
                $Segundos = [int]($AlvoHora - (Get-Date)).TotalSeconds
            }
            Start-Job -ScriptBlock {
                param($Sec, $Msg)
                Start-Sleep -Seconds $Sec
                Add-Type -AssemblyName System.Speech
                $S = New-Object System.Speech.Synthesis.SpeechSynthesizer
                $S.Speak("Lembrete Skynet: $Msg")
                if (Test-Path "C:\\SkynetPowerShell\\secrets.json") {
                    try {
                        $SecJson = Get-Content "C:\\SkynetPowerShell\\secrets.json" -Raw | ConvertFrom-Json
                        if ($SecJson.TELEGRAM_BOT_TOKEN -and $SecJson.TELEGRAM_CHAT_ID -notmatch "COLE_SEU") {
                            $B = @{ chat_id = $SecJson.TELEGRAM_CHAT_ID; text = "⏰ LEMBRETE SKYNET: $Msg" } | ConvertTo-Json -Compress
                            Invoke-RestMethod -Uri "https://telegram.org" -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($B)) -ContentType "application/json" | Out-Null
                        }
                    } catch {}
                }
            } -ArgumentList $Segundos, $AvisoTxt | Out-Null
            Falar-Skynet("Lembrete agendado.")
            return "=== LEMBRETE AGENDADO ===`nDisparo em: $Quando ($Segundos segundos)`nMensagem: $AvisoTxt`nNotificacao: Voz + Telegram"
        }
        "^acordar-pc:\\s*(.+)" {
            $MacStr = $Matches[1].Trim() -replace '[:-]', ''
            if ($MacStr.Length -ne 12) { return "MAC Address invalido. Use o formato AA:BB:CC:DD:EE:FF." }
            $MacBytes = 0..5 | ForEach-Object { [Convert]::ToByte($MacStr.Substring($_ * 2, 2), 16) }
            $Packet = (,0xFF * 6) + ($MacBytes * 16)
            $Udp = New-Object System.Net.Sockets.UdpClient
            $Udp.Connect([System.Net.IPAddress]::Broadcast, 9)
            [void]$Udp.Send($Packet, $Packet.Length)
            $Udp.Close()
            Falar-Skynet("Pacote Wake on LAN enviado.")
            return "Pacote magico Wake-on-LAN enviado para o MAC $($Matches[1].Trim())."
        }
        "^doutor-skynet$" {
            $Rel = @("=== DIAGNOSTICO E AUTO-CURA DOUTOR SKYNET ===")
            $Tasks = Get-ScheduledTask -TaskName "Skynet*" -ErrorAction SilentlyContinue
            foreach ($t in $Tasks) {
                if ($t.State -ne "Running" -and $t.TaskName -ne "SkynetWeeklyBackup") {
                    Start-ScheduledTask -TaskName $t.TaskName -ErrorAction SilentlyContinue
                    $Rel += "[CURADO] $($t.TaskName) estava $($t.State) -> Reiniciado!"
                } else {
                    $Rel += "[OK] $($t.TaskName): $($t.State)"
                }
            }
            $P5000 = try { (Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 3).StatusCode } catch { "OFFLINE" }
            $P11434 = try { (Invoke-RestMethod -Uri "http://127.0.0" -TimeoutSec 3).models.Count } catch { "OFFLINE" }
            $Rel += "Porta 5000 (Interface 66827): $P5000"
            $Rel += "Porta 11434 (Ollama Modelos): $P11434"
            Falar-Skynet("Auditoria concluida. Todos os sistemas verificados.")
            return ($Rel -join "`n")
        }
        "^olhar-foto:\\s*(.+)" {
            $ImgPath = $Matches[1].Trim().Trim('"')
            if (-not (Test-Path $ImgPath)) { return "Imagem nao encontrada: $ImgPath" }
            Falar-Skynet("Analisando imagem com visao multimodal.")
            $B64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($ImgPath))
            $PayloadVis = @{ model = "moondream"; prompt = "Descreva detalhadamente o que voce ve nesta imagem em portugues:"; images = @($B64); stream = $false } | ConvertTo-Json -Compress
            try {
                $RespVis = Invoke-RestMethod -Uri "http://127.0.0" -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($PayloadVis)) -ContentType "application/json" -TimeoutSec 120
                return "=== VISAO MULTIMODAL ===`n$($RespVis.response)"
            } catch {
                return "Modelo visual 'moondream' nao encontrado no Ollama. Rode no terminal: ollama pull moondream"
            }
        }
        "^vigiar-downloads$" {'''
    code = code.replace('        "^vigiar-downloads$" {', bloco_avancado, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[1/3] Agendador, Wake-on-LAN, Doutor Skynet e Visao Multimodal instalados!")

# Libera gatilhos no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"doutor-skynet"' not in p_txt:
        py_p.write_text(p_txt.replace('"vigiar-downloads",', '"vigiar-downloads", "me-lembre:", "acordar-pc:", "doutor-skynet", "olhar-foto:",'), encoding="utf-8")
        print("[2/3] Novos gatilhos liberados no /api/chat!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[3/3] Motores reiniciados e Interface 66827 preservada!")
