import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

# 1. Adiciona divisor/posicionador nativo de janelas (User32 MoveWindow) + comando vigiar-downloads
if "posicionar:" not in code:
    code = code.replace("analisar-copia", "analisar-copia|posicionar:|vigiar-downloads")
    
    # Adiciona MoveWindow na classe Win11Native se ainda nao existir
    if "MoveWindow" not in code:
        code = code.replace(
            'public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);',
            'public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);\n    [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);'
        )

    bloco_garimpo = '''        "^posicionar:\\s*(.+)" {
            $Lado = $Matches.Trim().ToLower()
            Add-Type -AssemblyName System.Windows.Forms
            $Area = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
            $Hwnd = [Win11Native]::GetForegroundWindow()
            [void][Win11Native]::ShowWindow($Hwnd, 9)
            if ($Lado -eq "esquerda") {
                [void][Win11Native]::MoveWindow($Hwnd, $Area.X, $Area.Y, [int]($Area.Width / 2), $Area.Height, $true)
                return "Janela encaixada na metade esquerda da tela."
            } elseif ($Lado -eq "direita") {
                [void][Win11Native]::MoveWindow($Hwnd, [int]($Area.Width / 2), $Area.Y, [int]($Area.Width / 2), $Area.Height, $true)
                return "Janela encaixada na metade direita da tela."
            } elseif ($Lado -eq "maximizar") {
                [void][Win11Native]::ShowWindow($Hwnd, 3)
                return "Janela maximizada."
            }
            return "Use: 'posicionar: esquerda', 'posicionar: direita' ou 'posicionar: maximizar'."
        }
        "^vigiar-downloads$" {
            $DlPath = [Environment]::GetFolderPath("UserProfile") + "\\Downloads"
            if (-not $Global:WatcherDl) {
                $Global:WatcherDl = New-Object System.IO.FileSystemWatcher $DlPath, "*.*"
                $Global:WatcherDl.EnableRaisingEvents = $true
                Register-ObjectEvent -InputObject $Global:WatcherDl -EventName Created -SourceIdentifier "SkynetDlWatcher" -Action {
                    $Nome = $Event.SourceEventArgs.Name
                    if ($Nome -notmatch '\.(tmp|crdownload|part)$') {
                        Notificar-Windows "SKYNET Downloads" "Novo arquivo detectado: $Nome"
                    }
                } | Out-Null
            }
            Falar-Skynet("Vigilancia da pasta Downloads ativada.")
            return "Sentinela ativa monitorando novos arquivos em: $DlPath"
        }
        "^analisar-copia$" {'''
    code = code.replace('        "^analisar-copia$" {', bloco_garimpo, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[1/3] Posicionador de Janelas e Vigia de Downloads instalados no Core 8080!")

# 2. Cria Sensor Nativo de USB/Pendrive (WMI Win32_VolumeChangeEvent) ligado ao Guardiao
usb_ps = ps_dir / "skynet_usb_sensor.ps1"
usb_ps.write_text('''Register-WmiEvent -Class Win32_VolumeChangeEvent -SourceIdentifier "SkynetUsbEvent" -Action {
    if ($Event.SourceEventArgs.NewEvent.EventType -eq 2) {
        $Drive = $Event.SourceEventArgs.NewEvent.DriveName
        $Disco = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$Drive'" -ErrorAction SilentlyContinue
        $LivreGB = if ($Disco) { [math]::Round($Disco.FreeSpace / 1GB, 1) } else { "?" }
        $Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
        Add-Type -AssemblyName System.Speech
        $S = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $S.SpeakAsync("Dispositivo externo conectado na unidade $Drive com $LivreGB gigabytes livres.") | Out-Null
    }
} | Out-Null
while ($true) { Start-Sleep 30 }
''', encoding="utf-8")

reg_usb = '''
$Act = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\\SkynetPowerShell\\skynet_usb_sensor.ps1"
$Trig = New-ScheduledTaskTrigger -AtLogOn
$Set = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Days 3650)
Register-ScheduledTask -TaskName "SkynetUsbSensorImortal" -Action $Act -Trigger $Trig -Settings $Set -Force | Out-Null
Start-ScheduledTask -TaskName "SkynetUsbSensorImortal"
'''
subprocess.run(["powershell", "-NoProfile", "-Command", reg_usb], check=True)
print("[2/3] Sensor nativo de Pendrive/USB registrado no Windows 11!")

# 3. Libera gatilhos no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"posicionar:"' not in p_txt:
        py_p.write_text(p_txt.replace('"analisar-copia",', '"analisar-copia", "posicionar:", "vigiar-downloads",'), encoding="utf-8")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[3/3] Novos sensores nativos do Windows 11 ativados com sucesso!")
