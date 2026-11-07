import pathlib, subprocess, winreg

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Redireciona a tecla F1 (HelpPane.exe) do Windows 11 para o lançador da SKYNET
ifeo_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\HelpPane.exe"
with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, ifeo_path) as k:
    winreg.SetValueEx(k, "Debugger", 0, winreg.REG_SZ, r'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\SkynetPowerShell\skynet_win_bridge.ps1" -Modo prompt')
print("[1/3] Tecla F1 (Ajuda do Windows 11) redirecionada para a SKYNET!")

# 2. Atualiza a Sentinela de Rede & Energia para reagir à Suspensão e Despertar do Windows 11
net_power_ps = ps_dir / "skynet_net_power.ps1"
net_power_ps.write_text('''Add-Type -AssemblyName System.Speech, System.Windows.Forms
$S = New-Object System.Speech.Synthesis.SpeechSynthesizer

Register-ObjectEvent -InputObject ([System.Net.NetworkInformation.NetworkChange]) -EventName NetworkAvailabilityChanged -SourceIdentifier "SkynetNetChange" -Action {
    if ($Event.SourceEventArgs.IsAvailable) {
        $S.SpeakAsync("Conexao de rede restabelecida.") | Out-Null
    } else {
        $S.SpeakAsync("Atencao: conexao de rede perdida.") | Out-Null
    }
} | Out-Null

Register-ObjectEvent -InputObject ([Microsoft.Win32.SystemEvents]) -EventName PowerModeChanged -SourceIdentifier "SkynetPowerChange" -Action {
    $Modo = $Event.SourceEventArgs.Mode
    if ($Modo -eq "Suspend") {
        [System.GC]::Collect()
    } elseif ($Modo -eq "Resume") {
        $S.SpeakAsync("Sistema retomado da suspensao. Motores Skynet online.") | Out-Null
    } elseif ($Modo -eq "StatusChange") {
        $S.SpeakAsync("Estado de energia do Windows alterado.") | Out-Null
    }
} | Out-Null

while ($true) { Start-Sleep 30 }
''', encoding="utf-8")

subprocess.run(["powershell", "-NoProfile", "-Command", "Stop-ScheduledTask -TaskName 'SkynetNetPowerImortal' -ErrorAction SilentlyContinue; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetNetPowerImortal' -ErrorAction SilentlyContinue"], check=True)
print("[2/3] Eventos de Suspensao e Despertar do Windows 11 ligados a SKYNET!")

# 3. Mantém Interface 66827 ReadOnly e sincroniza versão final no GitHub
html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
if html_p.exists():
    subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])

backup_py = ps_dir / "backup_final_seguro.py"
if backup_py.exists():
    print("[3/3] Salvando no GitHub...")
    subprocess.run([r"C:\Users\Administrador\AppData\Local\Programs\Python\Python313\python.exe", str(backup_py)])
