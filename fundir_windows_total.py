import pathlib, subprocess, winreg

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Cria o script ponte usado pelo Botão Direito do Explorer e pelo Atalho Ctrl+Alt+S
bridge_win = ps_dir / "skynet_win_bridge.ps1"
bridge_win.write_text('''param([string]$Modo = "prompt", [string]$Alvo = "")
Add-Type -AssemblyName Microsoft.VisualBasic, System.Windows.Forms
$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }

if ($Modo -eq "arquivo" -and $Alvo) {
    $Cmd = "ler-tudo: $Alvo"
} elseif ($Modo -eq "pasta" -and $Alvo) {
    $Cmd = "aprender-pasta: $Alvo"
} else {
    $Cmd = [Microsoft.VisualBasic.Interaction]::InputBox("Digite um comando ou pergunta para a SKYNET:", "SKYNET FUSAO WINDOWS (Ctrl+Alt+S)", "raio-x")
}

if ([string]::IsNullOrWhiteSpace($Cmd)) { exit }

try {
    $Body = @{ entrada = $Cmd } | ConvertTo-Json -Compress
    $Res = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $Headers -Body ([System.Text.Encoding]::UTF8.GetBytes($Body)) -TimeoutSec 120
    $Texto = if ($Res.resultado) { $Res.resultado } else { "$($Res.erro)" }
    [System.Windows.Forms.MessageBox]::Show($Texto, "SKYNET - Resposta Nativa", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information) | Out-Null
} catch {
    [System.Windows.Forms.MessageBox]::Show("Erro ao comunicar com Skynet Core 8080: $_", "SKYNET", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error) | Out-Null
}
''', encoding="utf-8")
print("[1/4] Ponte nativa Windows (skynet_win_bridge.ps1) criada!")

# 2. Registra Botão Direito no Windows Explorer (Arquivos e Pastas) em HKCU (seguro, sem mexer no sistema)
cmd_arq = f'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "{bridge_win}" -Modo arquivo -Alvo "%1"'
cmd_dir = f'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "{bridge_win}" -Modo pasta -Alvo "%V"'

for reg_path, cmd_val in [
    (r"Software\Classes\*\shell\SkynetAnalisar", cmd_arq),
    (r"Software\Classes\Directory\shell\SkynetAnalisar", cmd_dir)
]:
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path) as k:
        winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "🧠 Analisar com SKYNET")
        winreg.SetValueEx(k, "Icon", 0, winreg.REG_SZ, "shell32.dll,23")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path + r"\command") as kc:
        winreg.SetValueEx(kc, "", 0, winreg.REG_SZ, cmd_val)
print("[2/4] Menu de contexto 'Analisar com SKYNET' registrado no Windows Explorer!")

# 3. Cria Atalho Global Ctrl + Alt + S no Menu Iniciar do Usuário
ps_shortcut = f'''
$Wsh = New-Object -ComObject WScript.Shell
$LnkPath = [Environment]::GetFolderPath("StartMenu") + "\\Programs\\SKYNET Comando Rapido.lnk"
$Sc = $Wsh.CreateShortcut($LnkPath)
$Sc.TargetPath = "powershell.exe"
$Sc.Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"C:\\SkynetPowerShell\\skynet_win_bridge.ps1`" -Modo prompt"
$Sc.Hotkey = "CTRL+ALT+S"
$Sc.IconLocation = "shell32.dll,23"
$Sc.Save()
'''
subprocess.run(["powershell", "-NoProfile", "-Command", ps_shortcut], check=True)
print("[3/4] Atalho global Ctrl + Alt + S configurado no Windows!")

# 4. Adiciona Notificações Nativas (Balão na Barra de Tarefas) no Core + Briefing ao Desbloquear o PC
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

fn_notify = '''function Notificar-Windows([string]$Titulo, [string]$Msg) {
    try {
        Add-Type -AssemblyName System.Windows.Forms, System.Drawing
        $N = New-Object System.Windows.Forms.NotifyIcon
        $N.Icon = [System.Drawing.SystemIcons]::Information
        $N.BalloonTipTitle = $Titulo
        $N.BalloonTipText = if ($Msg.Length -gt 200) { $Msg.Substring(0, 200) + "..." } else { $Msg }
        $N.Visible = $true
        $N.ShowBalloonTip(5000)
        Start-Job -ScriptBlock { param($ic) Start-Sleep 6; $ic.Dispose() } -ArgumentList $N | Out-Null
    } catch {}
}
'''

if "function Notificar-Windows" not in code:
    code = fn_notify + "\n" + code
    code = code.replace('Falar-Skynet("Analisando o conteudo da tela.")', 'Falar-Skynet("Analisando o conteudo da tela."); Notificar-Windows "SKYNET Visao" "Lendo conteudo da tela..."')
    core_p.write_text(code, encoding="utf-8")

# Registra evento nativo ao desbloquear a sessão do Windows (OnSessionUnlock)
unlock_ps = ps_dir / "skynet_unlock.ps1"
unlock_ps.write_text('''$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
$Body = @{ entrada = "energia" } | ConvertTo-Json -Compress
try {
    $R = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $Headers -Body ([System.Text.Encoding]::UTF8.GetBytes($Body)) -TimeoutSec 15
    Add-Type -AssemblyName System.Speech
    $S = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $S.Speak("Bem-vindo de volta, Michel. Sistemas Skynet operando normalmente.")
} catch {}
''', encoding="utf-8")

reg_unlock = '''
$Act = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\\SkynetPowerShell\\skynet_unlock.ps1"
$StateChangeTrigger = Get-CimClass -Namespace ROOT\\Microsoft\\Windows\\TaskScheduler -ClassName MSFT_TaskSessionStateChangeTrigger
$Trig = New-CimInstance -CimClass $StateChangeTrigger -ClientOnly
$Trig.StateChange = 8
$Trig.Enabled = $true
$Set = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "SkynetUnlockBriefing" -Action $Act -Trigger $Trig -Settings $Set -Force | Out-Null
Stop-ScheduledTask -TaskName "SkynetCoreImortal" -ErrorAction SilentlyContinue
Start-Sleep 1
Start-ScheduledTask -TaskName "SkynetCoreImortal" -ErrorAction SilentlyContinue
'''
subprocess.run(["powershell", "-NoProfile", "-Command", reg_unlock], check=True)
print("[4/4] Notificacoes nativas e Briefing ao Desbloquear o Windows ativados!")
