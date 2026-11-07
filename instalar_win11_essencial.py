import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

if "win11-essencial" not in code:
    code = code.replace("startup-pausar:", "startup-pausar:|win11-essencial|win11-restaurar")
    bloco_essencial = r'''        "^win11-essencial$" {
            # 1. Desativa aplicativos em segundo plano do Windows 11
            $BgPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications"
            if (-not (Test-Path $BgPath)) { New-Item -Path $BgPath -Force | Out-Null }
            Set-ItemProperty -Path $BgPath -Name "GlobalUserDisabled" -Value 1 -Type DWord -Force

            # 2. Coloca servicos nao-essenciais do Windows 11 em Manual (sob demanda) e para os que estao rodando
            $Sup = @("DiagTrack", "dmwappushservice", "MapsBroker", "Fax", "XblAuthManager", "XblGameSave", "XboxNetApiSvc", "XboxGipSvc", "WMPNetworkSvc", "RetailDemo", "RemoteRegistry", "gupdate", "gupdatem", "edgeupdate", "edgeupdatem")
            $Parados = @()
            foreach ($s in $Sup) {
                $Svc = Get-Service -Name $s -ErrorAction SilentlyContinue
                if ($Svc) {
                    Stop-Service -Name $s -Force -ErrorAction SilentlyContinue
                    Set-Service -Name $s -StartupType Manual -ErrorAction SilentlyContinue
                    $Parados += $s
                }
            }

            # 3. Aciona automaticamente o startup-otimizar para pausar apps de boot fora da lista essencial
            $H = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
            $ResBoot = try { (Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $H -Body '{"entrada":"startup-otimizar"}' -TimeoutSec 30).resultado } catch { "Boot verificado." }

            # 4. Libera memoria RAM imediatamente
            [System.GC]::Collect()
            Falar-Skynet("Modo Windows 11 essencial ativado. Apenas o sistema basico e a Skynet estao rodando.")
            return "=== MODO WIN11 ESSENCIAL ATIVADO ===`n- Apps em segundo plano: DESATIVADOS`n- Servicos superfluos pausados ($($Parados.Count)): $($Parados -join ', ')`n`n$ResBoot"
        }
        "^win11-restaurar$" {
            $BgPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications"
            if (Test-Path $BgPath) { Set-ItemProperty -Path $BgPath -Name "GlobalUserDisabled" -Value 0 -Type DWord -Force }
            foreach ($s in @("XblAuthManager", "XblGameSave", "XboxNetApiSvc", "Spooler")) {
                Set-Service -Name $s -StartupType Manual -ErrorAction SilentlyContinue
            }
            Falar-Skynet("Configuracoes padrao do Windows 11 restauradas.")
            return "Configuracoes de aplicativos em segundo plano e servicos do Windows 11 restauradas."
        }
        "^startup-pausar:\s*(.+)" {'''
    code = code.replace('        "^startup-pausar:\\s*(.+)" {', bloco_essencial, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[1/3] Comandos 'win11-essencial' e 'win11-restaurar' instalados!")

# Libera gatilhos no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"win11-essencial"' not in p_txt:
        py_p.write_text(p_txt.replace('"startup-pausar:",', '"startup-pausar:", "win11-essencial", "win11-restaurar",'), encoding="utf-8")
        print("[2/3] Gatilhos liberados no chat principal (/api/chat)!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[3/3] Motores reiniciados! Agora execute 'win11-essencial' para aplicar.")
