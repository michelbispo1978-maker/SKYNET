import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

if "velocidade-net" not in code:
    code = code.replace("consultar-memoria", "consultar-memoria|velocidade-net|rede-wifi|brilho:|historico")
    bloco = '''        "^velocidade-net" {
            $Synthesizer.SpeakAsync("Medindo velocidade da internet, aguarde.") | Out-Null
            $Ping = (Test-Connection -ComputerName "8.8.8.8" -Count 2 -ErrorAction SilentlyContinue | Measure-Object -Property ResponseTime -Average).Average
            $Sw = [System.Diagnostics.Stopwatch]::StartNew()
            try {
                $Tmp = "$env:TEMP\\skynet_speed.tmp"
                Invoke-WebRequest -Uri "https://ovh.net" -OutFile $Tmp -TimeoutSec 20
                $Sw.Stop()
                $Mbps = [math]::Round((10 * 8) / $Sw.Elapsed.TotalSeconds, 2)
                Remove-Item $Tmp -Force -ErrorAction SilentlyContinue
                return "=== VELOCIDADE DA INTERNET ===`nDownload: $Mbps Mbps`nPing (Google DNS): $([math]::Round($Ping,0)) ms"
            } catch {
                return "Falha ao testar download. Ping atual: $([math]::Round($Ping,0)) ms"
            }
        }
        "^rede-wifi" {
            $IpLocal = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notmatch "Loopback" -and $_.IPAddress -notmatch "^169\." } | Select-Object -First 1).IPAddress
            $IpPub = try { (Invoke-RestMethod -Uri "https://ipify.org" -TimeoutSec 5) } catch { "Indisponivel" }
            $Dispositivos = Get-NetNeighbor -AddressFamily IPv4 -State Reachable,Stale -ErrorAction SilentlyContinue | Select-Object -First 12 | ForEach-Object { "- $($_.IPAddress) [$($_.LinkLayerAddress)]" }
            return "=== REDE & DISPOSITIVOS ===`nIP Local: $IpLocal`nIP Publico: $IpPub`nDispositivos Detectados:`n" + ($Dispositivos -join "`n")
        }
        "^brilho:\\s*(\\d+)" {
            $Nivel = [int]$Matches[1]
            if ($Nivel -lt 0) { $Nivel = 0 }
            if ($Nivel -gt 100) { $Nivel = 100 }
            try {
                (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, $Nivel)
                return "Brilho da tela ajustado para $Nivel%."
            } catch {
                return "Monitor externo detectado: ajuste de brilho via WMI disponivel apenas em telas internas/notebooks."
            }
        }
        "^historico" {
            $LogFile = Get-ChildItem "C:\\SkynetPowerShell\\logs\\*.log" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
            if (-not $LogFile) { return "Nenhum registro de historico encontrado ainda." }
            $Linhas = Get-Content $LogFile.FullName -Tail 12
            return "=== HISTORICO RECENTE ($($LogFile.Name)) ===`n" + ($Linhas -join "`n")
        }
        "^consultar-memoria" {'''
    code = code.replace('        "^consultar-memoria" {', bloco, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[OK] Comandos velocidade-net, rede-wifi, brilho e historico instalados no Core!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado!")
