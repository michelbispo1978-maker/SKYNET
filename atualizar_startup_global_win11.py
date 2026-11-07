import pathlib, re, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

novo_bloco = r'''        "^startup-listar$" {
            $Caminhos = @(
                @{ Nome = "Usuario (HKCU)"; Run = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"; App = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run" },
                @{ Nome = "Sistema Global (HKLM)"; Run = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"; App = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run" }
            )
            $Saida = @("=== INICIALIZACAO GLOBAL DO WINDOWS 11 ===")
            foreach ($c in $Caminhos) {
                $Saida += "`n[$($c.Nome)]"
                $Itens = (Get-Item $c.Run -ErrorAction SilentlyContinue).Property
                if (-not $Itens) { $Saida += "- Nenhum item"; continue }
                foreach ($Nome in $Itens) {
                    $Bytes = (Get-ItemProperty -Path $c.App -Name $Nome -ErrorAction SilentlyContinue).$Nome
                    $Status = if ($Bytes -and $Bytes[0] -eq 3) { "[PAUSADO]" } else { "[ATIVO]" }
                    $Saida += "$Status $Nome"
                }
            }
            return ($Saida -join "`n")
        }
        "^startup-otimizar$" {
            $WlFile = "C:\SkynetPowerShell\database\startup_whitelist.json"
            New-Item -ItemType Directory -Path "C:\SkynetPowerShell\database" -Force | Out-Null
            if (-not (Test-Path $WlFile)) {
                @("Skynet", "SecurityHealth", "WindowsDefender", "Realtek", "Audio", "RtkAudUService", "igfx", "NvBackend") | ConvertTo-Json | Set-Content $WlFile -Encoding UTF8
            }
            $Whitelist = @(Get-Content $WlFile -Raw | ConvertFrom-Json)
            $Caminhos = @(
                @{ Run = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"; App = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run" },
                @{ Run = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"; App = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run" }
            )
            $Pausados = @(); $Mantidos = @()
            foreach ($c in $Caminhos) {
                if (-not (Test-Path $c.App)) { New-Item -Path $c.App -Force | Out-Null }
                $Itens = (Get-Item $c.Run -ErrorAction SilentlyContinue).Property
                foreach ($Nome in $Itens) {
                    $Permitido = $false
                    foreach ($w in $Whitelist) { if ($Nome -match [regex]::Escape($w)) { $Permitido = $true; break } }
                    if ($Permitido) {
                        Set-ItemProperty -Path $c.App -Name $Nome -Value ([byte[]](2,0,0,0,0,0,0,0,0,0,0,0)) -Type Binary -ErrorAction SilentlyContinue
                        $Mantidos += $Nome
                    } else {
                        Set-ItemProperty -Path $c.App -Name $Nome -Value ([byte[]](3,0,0,0,0,0,0,0,0,0,0,0)) -Type Binary -ErrorAction SilentlyContinue
                        $Pausados += $Nome
                    }
                }
            }
            $SvcsPausados = @()
            foreach ($sName in @("gupdate", "gupdatem", "edgeupdate", "edgeupdatem", "AdobeARMservice", "MozillaMaintenance")) {
                $S = Get-Service -Name $sName -ErrorAction SilentlyContinue
                if ($S -and $S.StartType -eq "Automatic") {
                    Stop-Service -Name $sName -Force -ErrorAction SilentlyContinue
                    Set-Service -Name $sName -StartupType Manual -ErrorAction SilentlyContinue
                    $SvcsPausados += $sName
                }
            }
            Falar-Skynet("Otimizacao global do Windows 11 concluida. $($Pausados.Count) aplicativos pausados no boot.")
            return "=== OTIMIZACAO GLOBAL WINDOWS 11 ===`nMantidos Ativos ($($Mantidos.Count)): $($Mantidos -join ', ')`nApps Pausados ($($Pausados.Count)): $($Pausados -join ', ')`nServicos em Manual ($($SvcsPausados.Count)): $($SvcsPausados -join ', ')"
        }'''

code = re.sub(
    r'        "\^startup-listar\$"\s*\{.*?        "\^startup-usar:',
    lambda m: novo_bloco + '\n        "^startup-usar:',
    code,
    count=1,
    flags=re.S
)
core_p.write_text(code, encoding="utf-8")
print("[1/2] Controle Global HKCU + HKLM + Servicos aplicado com sucesso!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[2/2] Motor Core 8080 reiniciado sem erros!")
