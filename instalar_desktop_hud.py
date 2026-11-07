import pathlib, subprocess, winreg

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Cria o Mini-HUD Flutuante Transparente para a Área de Trabalho (CPU/RAM + Botão Rápido)
hud_ps = ps_dir / "skynet_hud.ps1"
hud_ps.write_text('''Add-Type -AssemblyName System.Windows.Forms, System.Drawing

$Form = New-Object System.Windows.Forms.Form
$Form.Text = "SKYNET HUD"
$Form.Size = New-Object System.Drawing.Size(270, 58)
$Form.FormBorderStyle = "None"
$Form.TopMost = $true
$Form.BackColor = [System.Drawing.Color]::FromArgb(12, 22, 38)
$Form.Opacity = 0.88
$Form.StartPosition = "Manual"
$Screen = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$Form.Location = New-Object System.Drawing.Point(($Screen.Width - 285), 15)

# Permite arrastar o HUD para qualquer canto da tela
$dragging = $false; $dragCursor = [System.Drawing.Point]::Empty; $dragForm = [System.Drawing.Point]::Empty
$Form.Add_MouseDown({ $script:dragging = $true; $script:dragCursor = [System.Windows.Forms.Cursor]::Position; $script:dragForm = $Form.Location })
$Form.Add_MouseMove({ if ($script:dragging) { $dif = [System.Drawing.Point]::Subtract([System.Windows.Forms.Cursor]::Position, [System.Drawing.Size]$script:dragCursor); $Form.Location = [System.Drawing.Point]::Add($script:dragForm, [System.Drawing.Size]$dif) } })
$Form.Add_MouseUp({ $script:dragging = $false })

$Lbl = New-Object System.Windows.Forms.Label
$Lbl.ForeColor = [System.Drawing.Color]::FromArgb(0, 240, 255)
$Lbl.Font = New-Object System.Drawing.Font("Consolas", 8.5, [System.Drawing.FontStyle]::Bold)
$Lbl.Location = New-Object System.Drawing.Point(10, 8)
$Lbl.Size = New-Object System.Drawing.Size(175, 42)
$Lbl.Text = "SKYNET ONLINE`nCarregando telemetria..."
$Form.Controls.Add($Lbl)

$Btn = New-Object System.Windows.Forms.Button
$Btn.Text = "⚡ CMD"
$Btn.FlatStyle = "Flat"
$Btn.BackColor = [System.Drawing.Color]::FromArgb(0, 131, 143)
$Btn.ForeColor = [System.Drawing.Color]::White
$Btn.Font = New-Object System.Drawing.Font("Segoe UI", 8, [System.Drawing.FontStyle]::Bold)
$Btn.Location = New-Object System.Drawing.Point(190, 13)
$Btn.Size = New-Object System.Drawing.Size(68, 30)
$Btn.Add_Click({ Start-Process "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\\SkynetPowerShell\\skynet_win_bridge.ps1 -Modo prompt" })
$Form.Controls.Add($Btn)

$Timer = New-Object System.Windows.Forms.Timer
$Timer.Interval = 3000
$Timer.Add_Tick({
    try {
        $Os = Get-CimInstance Win32_OperatingSystem
        $RamPct = [math]::Round((($Os.TotalVisibleMemorySize - $Os.FreePhysicalMemory) / $Os.TotalVisibleMemorySize) * 100, 0)
        $CpuPct = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
        $Lbl.Text = "SKYNET HUD [ONLINE]`nCPU: $CpuPct% | RAM: $RamPct%"
    } catch {}
})
$Timer.Start()
[System.Windows.Forms.Application]::Run($Form)
''', encoding="utf-8")

# Inicia o HUD agora e coloca na inicialização do Windows
startup_hud = pathlib.Path.home() / r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\SKYNET_HUD.bat"
startup_hud.write_text('@echo off\nstart "" powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\\SkynetPowerShell\\skynet_hud.ps1"\n', encoding="utf-8")
subprocess.Popen(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", str(hud_ps)])
print("[1/3] Mini-HUD Flutuante ativado na Area de Trabalho!")

# 2. Adiciona comando 'organizar-desktop' no skynet_core.ps1
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")
if "organizar-desktop" not in code:
    code = code.replace("desligar-pc", "desligar-pc|organizar-desktop")
    bloco_desk = '''        "^organizar-desktop$" {
            $Desk = [Environment]::GetFolderPath("Desktop")
            $Mapa = @{
                "Documentos"   = @(".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".csv")
                "Imagens"      = @(".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")
                "Instaladores" = @(".exe", ".msi", ".zip", ".rar", ".7z")
            }
            $Movidos = 0
            Get-ChildItem -Path $Desk -File | Where-Object { $_.Extension -notin @(".lnk", ".url", ".ini") } | ForEach-Object {
                $DestPasta = "Outros"
                foreach ($k in $Mapa.Keys) { if ($Mapa[$k] -contains $_.Extension.ToLower()) { $DestPasta = $k; break } }
                $AlvoDir = Join-Path $Desk "Organizados_$DestPasta"
                New-Item -ItemType Directory -Path $AlvoDir -Force | Out-Null
                Move-Item -Path $_.FullName -Destination $AlvoDir -Force -ErrorAction SilentlyContinue
                $Movidos++
            }
            Falar-Skynet("Area de trabalho organizada. $Movidos arquivos movidos.")
            return "Area de Trabalho organizada com sucesso! Total de arquivos movidos: $Movidos."
        }
        "^desligar-pc$" {'''
    code = code.replace('        "^desligar-pc$" {', bloco_desk, 1)
    core_p.write_text(code, encoding="utf-8")

# 3. Cria Atalho "SKYNET Central 66827" na Área de Trabalho + Opção no botão direito do fundo do Desktop
ps_desk = '''
$Wsh = New-Object -ComObject WScript.Shell
$DeskLnk = [Environment]::GetFolderPath("Desktop") + "\\SKYNET Central 66827.lnk"
$Sc = $Wsh.CreateShortcut($DeskLnk)
$Sc.TargetPath = "http://localhost:5000"
$Sc.IconLocation = "shell32.dll,23"
$Sc.Save()
'''
subprocess.run(["powershell", "-NoProfile", "-Command", ps_desk], check=True)

with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Directory\Background\shell\SkynetDesktopCmd") as k:
    winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "⚡ Comando Rápido SKYNET")
    winreg.SetValueEx(k, "Icon", 0, winreg.REG_SZ, "shell32.dll,23")
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\Directory\Background\shell\SkynetDesktopCmd\command") as kc:
    winreg.SetValueEx(kc, "", 0, winreg.REG_SZ, r'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\SkynetPowerShell\skynet_win_bridge.ps1" -Modo prompt')

# Libera 'organizar-desktop' no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"organizar-desktop"' not in p_txt:
        py_p.write_text(p_txt.replace('"desligar-pc",', '"desligar-pc", "organizar-desktop",'), encoding="utf-8")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[CONCLUIDO] HUD, Organizador e Atalhos da Area de Trabalho ativados!")
