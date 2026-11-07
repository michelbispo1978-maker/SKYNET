import pathlib, subprocess

auto_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_autonomia.ps1")
code = auto_p.read_text(encoding="utf-8")

if "Sentinela-WiFi" not in code:
    bloco = '''        # Sentinela de Intrusos Wi-Fi + Modo Noturno (23h-07h)
        $HoraInt = [int](Get-Date -Format "HH")
        $ModoNoturno = ($HoraInt -ge 23 -or $HoraInt -lt 7)
        $MacFile = "C:\\SkynetPowerShell\\database\\macs_conhecidos.json"
        $Conhecidos = if (Test-Path $MacFile) { @(Get-Content $MacFile -Raw | ConvertFrom-Json) } else { @() }
        $Ativos = Get-NetNeighbor -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.State -in @("Reachable","Stale") -and $_.LinkLayerAddress -and $_.IPAddress -notmatch "^(224\\.|239\\.|255\\.|127\\.)" }
        $Novos = @()
        foreach ($Dev in $Ativos) {
            $Mac = $Dev.LinkLayerAddress.ToUpper()
            if ($Conhecidos -notcontains $Mac) {
                $Conhecidos += $Mac
                $Novos += "$($Dev.IPAddress) ($Mac)"
            }
        }
        if ($Novos.Count -gt 0) {
            $Conhecidos | ConvertTo-Json | Set-Content -Path $MacFile -Encoding UTF8
            $Lista = $Novos -join ", "
            Registrar-Evento "Sentinela-WiFi" "Novo dispositivo na rede: $Lista"
            if (-not $ModoNoturno) {
                $Voz.SpeakAsync("Alerta de rede: $($Novos.Count) novo dispositivo conectado ao Wi-Fi.") | Out-Null
            }
        }
    } catch {}'''
    code = code.replace('    } catch {}', bloco, 1)
    auto_p.write_text(code, encoding="utf-8")
    print("[OK] Sentinela de Intrusos Wi-Fi instalado!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetAutonomyImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetAutonomyImortal'"])
print("[CONCLUIDO] Guardiao Autonomo reiniciado e vigiando a rede!")
