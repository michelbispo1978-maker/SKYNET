import pathlib, subprocess, winreg

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Redireciona o botão/atalho Copilot (Win+C) e protocolos de ajuda do Windows 11 para a SKYNET
try:
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\ms-copilot") as k:
        winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "URL:SKYNET Core")
        winreg.SetValueEx(k, "URL Protocol", 0, winreg.REG_SZ, "")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\ms-copilot\shell\open\command") as kc:
        winreg.SetValueEx(kc, "", 0, winreg.REG_SZ, r'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\SkynetPowerShell\skynet_win_bridge.ps1" -Modo prompt')
    print("[1/3] Protocolo Copilot (Win+C) do Windows 11 redirecionado para a SKYNET!")
except Exception as e:
    print(f"[AVISO] Redirecionamento ms-copilot: {e}")

# 2. Cria Interceptador em Tempo Real de Travamentos de Apps (Application Crash Watcher)
crash_ps = ps_dir / "skynet_crash_interceptor.ps1"
crash_ps.write_text('''Add-Type -AssemblyName System.Speech
$S = New-Object System.Speech.Synthesis.SpeechSynthesizer
$UltimoId = (Get-WinEvent -FilterHashtable @{ LogName='Application'; Id=1000 } -MaxEvents 1 -ErrorAction SilentlyContinue).RecordId

while ($true) {
    try {
        $Ev = Get-WinEvent -FilterHashtable @{ LogName='Application'; Id=1000 } -MaxEvents 1 -ErrorAction SilentlyContinue
        if ($Ev -and $Ev.RecordId -ne $UltimoId) {
            $UltimoId = $Ev.RecordId
            $AppFalhou = ($Ev.Message -split "`n" | Select-Object -First 1) -replace 'Nome do aplicativo com falha:\s*|Faulting application name:\s*', ''
            $AppNome = ($AppFalhou -split ',')[0].Trim()
            if ($AppNome) {
                $S.SpeakAsync("Alerta do sistema: o aplicativo $AppNome parou de funcionar.") | Out-Null
            }
        }
    } catch {}
    Start-Sleep -Seconds 5
}
''', encoding="utf-8")

reg_crash = '''
$Act = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\\SkynetPowerShell\\skynet_crash_interceptor.ps1"
$Trig = New-ScheduledTaskTrigger -AtLogOn
$Set = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Days 3650) -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask -TaskName "SkynetCrashInterceptor" -Action $Act -Trigger $Trig -Settings $Set -Force | Out-Null
Start-ScheduledTask -TaskName "SkynetCrashInterceptor"
'''
subprocess.run(["powershell", "-NoProfile", "-Command", reg_crash], check=True)
print("[2/3] Interceptador nativo de travamentos de apps (Event ID 1000) ativado!")

# 3. Registra extensão .skynet para abrir e executar comandos direto pelo Windows Explorer
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.skynet") as k:
    winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "SkynetCommandFile")
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\SkynetCommandFile\shell\open\command") as kc:
    winreg.SetValueEx(kc, "", 0, winreg.REG_SZ, r'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\SkynetPowerShell\skynet_win_bridge.ps1" -Modo arquivo -Alvo "%1"')
print("[3/3] Extensao nativa .skynet integrada ao kernel do Windows Explorer!")

# Garante Interface 66827 blindada e atualiza backup no GitHub
html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
if html_p.exists():
    subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])

backup_py = ps_dir / "backup_final_seguro.py"
if backup_py.exists():
    subprocess.run([r"C:\Users\Administrador\AppData\Local\Programs\Python\Python313\python.exe", str(backup_py)])
