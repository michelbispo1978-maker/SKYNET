import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

if "startup-listar" not in code:
    code = code.replace("faxina-win11", "faxina-win11|startup-listar|startup-otimizar|startup-usar:|startup-pausar:")
    bloco_startup = '''        "^startup-listar$" {
            $RegRun = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
            $RegApp = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run"
            $Itens = (Get-Item $RegRun -ErrorAction SilentlyContinue).Property
            if (-not $Itens) { return "Nenhum programa de usuario configurado na inicializacao." }
            $Lista = foreach ($Nome in $Itens) {
                $Bytes = (Get-ItemProperty -Path $RegApp -Name $Nome -ErrorAction SilentlyContinue).$Nome
                $Status = if ($Bytes -and $Bytes[0] -eq 3) { "[PAUSADO]" } else { "[ATIVO]" }
                "$Status $Nome"
            }
            return "=== INICIALIZACAO DO WINDOWS 11 ===`n" + ($Lista -join "`n")
        }
        "^startup-otimizar$" {
            $WlFile = "C:\\SkynetPowerShell\\database\\startup_whitelist.json"
            New-Item -ItemType Directory -Path "C:\\SkynetPowerShell\\database" -Force | Out-Null
            if (-not (Test-Path $WlFile)) {
                @("Skynet", "SecurityHealth", "WindowsDefender", "OneDrive", "Realtek", "Audio") | ConvertTo-Json | Set-Content $WlFile -Encoding UTF8
            }
            $Whitelist = @(Get-Content $WlFile -Raw | ConvertFrom-Json)
            $RegRun = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
            $RegApp = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run"
            if (-not (Test-Path $RegApp)) { New-Item -Path $RegApp -Force | Out-Null }
            $Itens = (Get-Item $RegRun -ErrorAction SilentlyContinue).Property
            $Pausados = @()
            $Mantidos = @()
            foreach ($Nome in $Itens) {
                $Permitido = $false
                foreach ($w in $Whitelist) { if ($Nome -match [regex]::Escape($w)) { $Permitido = $true; break } }
                if ($Permitido) {
                    Set-ItemProperty -Path $RegApp -Name $Nome -Value ([byte[]](2,0,0,0,0,0,0,0,0,0,0,0)) -Type Binary
                    $Mantidos += $Nome
                } else {
                    Set-ItemProperty -Path $RegApp -Name $Nome -Value ([byte[]](3,0,0,0,0,0,0,0,0,0,0,0)) -Type Binary
                    $Pausados += $Nome
                }
            }
            Falar-Skynet("Inicializacao otimizada. $($Pausados.Count) programas foram pausados e $($Mantidos.Count) mantidos ativos.")
            return "=== OTIMIZACAO DE BOOT CONCLUIDA ===`nMantidos Ativos ($($Mantidos.Count)): $($Mantidos -join ', ')`nColocados em Pausa ($($Pausados.Count)): $($Pausados -join ', ')"
        }
        "^startup-usar:\\s*(.+)" {
            $Alvo = $Matches.Trim()
            $WlFile = "C:\\SkynetPowerShell\\database\\startup_whitelist.json"
            New-Item -ItemType Directory -Path "C:\\SkynetPowerShell\\database" -Force | Out-Null
            $Wl = if (Test-Path $WlFile) { @(Get-Content $WlFile -Raw | ConvertFrom-Json) } else { @("Skynet", "SecurityHealth") }
            if ($Wl -notcontains $Alvo) { $Wl += $Alvo; $Wl | ConvertTo-Json | Set-Content $WlFile -Encoding UTF8 }
            $RegRun = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
            $RegApp = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run"
            $Reativados = @()
            foreach ($Nome in (Get-Item $RegRun -ErrorAction SilentlyContinue).Property) {
                if ($Nome -match [regex]::Escape($Alvo)) {
                    Set-ItemProperty -Path $RegApp -Name $Nome -Value ([byte[]](2,0,0,0,0,0,0,0,0,0,0,0)) -Type Binary
                    $Reativados += $Nome
                }
            }
            Falar-Skynet("$Alvo liberado na inicializacao.")
            return "Programa '$Alvo' adicionado a lista de uso. Reativados no boot: $($Reativados -join ', ')"
        }
        "^startup-pausar:\\s*(.+)" {
            $Alvo = $Matches.Trim()
            $RegRun = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
            $RegApp = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run"
            if (-not (Test-Path $RegApp)) { New-Item -Path $RegApp -Force | Out-Null }
            $Pausados = @()
            foreach ($Nome in (Get-Item $RegRun -ErrorAction SilentlyContinue).Property) {
                if ($Nome -match [regex]::Escape($Alvo)) {
                    Set-ItemProperty -Path $RegApp -Name $Nome -Value ([byte[]](3,0,0,0,0,0,0,0,0,0,0,0)) -Type Binary
                    $Pausados += $Nome
                }
            }
            Falar-Skynet("$Alvo colocado em pausa.")
            return "Pausados na inicializacao: $($Pausados -join ', ')"
        }
        "^faxina-win11$" {'''
    code = code.replace('        "^faxina-win11$" {', bloco_startup, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[1/3] Controlador de Inicializacao instalado no Core 8080!")

# Libera gatilhos no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"startup-listar"' not in p_txt:
        py_p.write_text(p_txt.replace('"faxina-win11",', '"faxina-win11", "startup-listar", "startup-otimizar", "startup-usar:", "startup-pausar:",'), encoding="utf-8")
        print("[2/3] Gatilhos liberados no chat principal (/api/chat)!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[3/3] Motores reiniciados e Interface 66827 preservada!")
