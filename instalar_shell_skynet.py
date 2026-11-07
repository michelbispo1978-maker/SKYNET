import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Cria o Lançador Oficial de Shell do Windows 11 para a SKYNET
shell_ps = ps_dir / "skynet_os_shell.ps1"
shell_ps.write_text('''# Garante que os motores da colmeia estao ativos
foreach ($t in @("SkynetCoreImortal", "SkynetWeb5000Imortal", "SkynetAutonomyImortal", "SkynetTelegramImortal")) {
    Start-ScheduledTask -TaskName $t -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 2

# Abre a Interface 66827 em tela cheia como ambiente principal do sistema
$Edge = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
$Chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
if (Test-Path $Chrome) {
    Start-Process $Chrome -ArgumentList "--app=http://localhost:5000 --start-maximized"
} elseif (Test-Path $Edge) {
    Start-Process $Edge -ArgumentList "--app=http://localhost:5000 --start-maximized"
} else {
    Start-Process "http://localhost:5000"
}

# Inicia o Mini-HUD e mantem o loop vivo do Shell
Start-Process "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\\SkynetPowerShell\\skynet_hud.ps1"
Add-Type -AssemblyName System.Speech
$S = New-Object System.Speech.Synthesis.SpeechSynthesizer
$S.SpeakAsync("Sistema operacional Skynet carregado como interface principal.") | Out-Null

while ($true) { Start-Sleep -Seconds 15 }
''', encoding="utf-8")

# 2. Adiciona comandos 'modo-shell-skynet' e 'modo-shell-windows' no skynet_core.ps1
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

if "modo-shell-skynet" not in code:
    code = code.replace("reabrir-aba", "reabrir-aba|modo-shell-skynet|modo-shell-windows")
    bloco_shell = r'''        "^modo-shell-skynet$" {
            $Winlogon = "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon"
            Set-ItemProperty -Path $Winlogon -Name "Shell" -Value 'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\SkynetPowerShell\skynet_os_shell.ps1"' -Force
            Falar-Skynet("Modo Shell Skynet ativado. No proximo login a Skynet assumira o lugar da area de trabalho do Windows 11.")
            return "=== MODO SHELL SKYNET ATIVADO ===`nA SKYNET agora e o Shell principal do seu usuario no Windows 11.`n- Para testar agora: encerre a sessao ou reinicie.`n- Para abrir o Explorer dentro dela: digite 'abrir: explorer'.`n- Para voltar ao Windows padrao: digite 'modo-shell-windows'."
        }
        "^modo-shell-windows$" {
            $Winlogon = "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon"
            Remove-ItemProperty -Path $Winlogon -Name "Shell" -ErrorAction SilentlyContinue
            if (-not (Get-Process explorer -ErrorAction SilentlyContinue)) { Start-Process explorer.exe }
            Falar-Skynet("Shell padrao do Windows 11 restaurado.")
            return "=== SHELL PADRAO WINDOWS 11 RESTAURADO ===`nO explorer.exe voltou a ser o ambiente principal."
        }
        "^reabrir-aba$" {'''
    code = code.replace('        "^reabrir-aba$" {', bloco_shell, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[1/3] Comandos 'modo-shell-skynet' e 'modo-shell-windows' instalados!")

# 3. Libera gatilhos no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"modo-shell-skynet"' not in p_txt:
        py_p.write_text(p_txt.replace('"reabrir-aba",', '"reabrir-aba", "modo-shell-skynet", "modo-shell-windows",'), encoding="utf-8")
        print("[2/3] Gatilhos liberados no chat principal (/api/chat)!")

html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
if html_p.exists():
    subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[3/3] Alternador de Shell pronto! Salvando no GitHub...")

backup_py = ps_dir / "backup_final_seguro.py"
if backup_py.exists():
    subprocess.run([r"C:\Users\Administrador\AppData\Local\Programs\Python\Python313\python.exe", str(backup_py)])
