import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Cria o motor de Wake-Word Offline ("Skynet") usando System.Speech.Recognition nativo do Windows 11
wake_ps = ps_dir / "skynet_wakeword.ps1"
wake_ps.write_text('''Add-Type -AssemblyName System.Speech, System.Windows.Forms, Microsoft.VisualBasic
$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }

try {
    $Rec = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    $Choices = New-Object System.Speech.Recognition.Choices
    $Choices.Add("Skynet")
    $Choices.Add("Ativar Skynet")
    $Gb = New-Object System.Speech.Recognition.GrammarBuilder($Choices)
    $Grammar = New-Object System.Speech.Recognition.Grammar($Gb)
    $Rec.LoadGrammar($Grammar)
    $Rec.SetInputToDefaultAudioDevice()

    while ($true) {
        $Result = $Rec.Recognize((New-TimeSpan -Seconds 5))
        if ($Result -and $Result.Confidence -ge 0.65) {
            # Verifica se o robo 8080 ja nao esta falando para evitar auto-escuta
            $Falando = $false
            try { $Falando = (Invoke-RestMethod -Uri "http://localhost:8080/falando" -TimeoutSec 2).falando } catch {}
            if (-not $Falando) {
                [console]::beep(900, 150)
                Start-Process "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\\SkynetPowerShell\\skynet_win_bridge.ps1 -Modo prompt"
                Start-Sleep -Seconds 3
            }
        }
    }
} catch {
    # Caso nao haja microfone conectado no momento, aguarda sem travar
    while ($true) { Start-Sleep 60 }
}
''', encoding="utf-8")

# 2. Cria a Sentinela de Eventos de Rede e Energia do Windows 11
net_power_ps = ps_dir / "skynet_net_power.ps1"
net_power_ps.write_text('''Add-Type -AssemblyName System.Speech, System.Windows.Forms
$S = New-Object System.Speech.Synthesis.SpeechSynthesizer

Register-ObjectEvent -InputObject ([System.Net.NetworkInformation.NetworkChange]) -EventName NetworkAvailabilityChanged -SourceIdentifier "SkynetNetChange" -Action {
    $Online = $Event.SourceEventArgs.IsAvailable
    if ($Online) {
        $S.SpeakAsync("Conexao de rede restabelecida.") | Out-Null
    } else {
        $S.SpeakAsync("Atencao: conexao de rede perdida.") | Out-Null
    }
} | Out-Null

Register-ObjectEvent -InputObject ([Microsoft.Win32.SystemEvents]) -EventName PowerModeChanged -SourceIdentifier "SkynetPowerChange" -Action {
    if ($Event.SourceEventArgs.Mode -eq "StatusChange") {
        $S.SpeakAsync("Estado de energia do Windows alterado.") | Out-Null
    }
} | Out-Null

while ($true) { Start-Sleep 30 }
''', encoding="utf-8")

# 3. Registra as duas tarefas no Agendador do Windows 11 (na sessao do usuario para acessar microfone e audio)
reg_tasks = '''
$Set = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Days 3650) -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1)
$Trig = New-ScheduledTaskTrigger -AtLogOn

$ActWake = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\\SkynetPowerShell\\skynet_wakeword.ps1"
Register-ScheduledTask -TaskName "SkynetWakeWordImortal" -Action $ActWake -Trigger $Trig -Settings $Set -Force | Out-Null
Start-ScheduledTask -TaskName "SkynetWakeWordImortal"

$ActNet = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\\SkynetPowerShell\\skynet_net_power.ps1"
Register-ScheduledTask -TaskName "SkynetNetPowerImortal" -Action $ActNet -Trigger $Trig -Settings $Set -Force | Out-Null
Start-ScheduledTask -TaskName "SkynetNetPowerImortal"
'''
subprocess.run(["powershell", "-NoProfile", "-Command", reg_tasks], check=True)
print("[1/2] Wake-Word Offline ('Skynet') e Sentinela de Rede/Energia ativados!")

# 4. Garante Interface 66827 blindada e executa Backup Final Seguro no GitHub
html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
if html_p.exists():
    subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])

backup_py = ps_dir / "backup_final_seguro.py"
if backup_py.exists():
    print("[2/2] Salvando pacote completo e blindado no GitHub...")
    subprocess.run([r"C:\Users\Administrador\AppData\Local\Programs\Python\Python313\python.exe", str(backup_py)])
