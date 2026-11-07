import os, pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Cria o comando global 'skynet.cmd' para funcionar em qualquer CMD, Terminal ou Win+R
cmd_global = ps_dir / "skynet.cmd"
cmd_global.write_text('''@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$q = '%*'; if (-not $q) { $q = 'raio-x' }; $h = @{'Content-Type'='application/json';'Authorization'='Bearer SKYNET-66827-FUSAO-TOTAL'}; $b = @{entrada=$q} | ConvertTo-Json -Compress; $r = Invoke-RestMethod -Uri 'http://localhost:8080/command' -Method Post -Headers $h -Body ([System.Text.Encoding]::UTF8.GetBytes($b)) -TimeoutSec 90; Write-Output $r.resultado"
''', encoding="utf-8")

# Adiciona C:\SkynetPowerShell ao PATH do usuário no Windows 11
ps_path = '''
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*C:\\SkynetPowerShell*") {
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;C:\\SkynetPowerShell", "User")
}
'''
subprocess.run(["powershell", "-NoProfile", "-Command", ps_path], check=True)
print("[1/3] Comando global 'skynet' registrado no PATH do Windows 11!")

# 2. Adiciona Lançador Universal de Programas e Configurações do Win 11 (abrir: ...) no skynet_core.ps1
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

if '"^abrir:\\s*(.+)"' not in code:
    code = code.replace("modo-turbo", "modo-turbo|abrir:")
    bloco_abrir = '''        "^abrir:\\s*(.+)" {
            $App = $Matches.Trim().ToLower()
            $AtalhosWin11 = @{
                "configuracoes" = "ms-settings:"
                "bluetooth"     = "ms-settings:bluetooth"
                "wifi"          = "ms-settings:network-wifi"
                "som"           = "ms-settings:sound"
                "tarefas"       = "taskmgr.exe"
                "explorer"      = "explorer.exe"
                "bloco"         = "notepad.exe"
                "calculadora"   = "calc.exe"
                "chrome"        = "chrome.exe"
                "edge"          = "msedge.exe"
            }
            $AlvoExec = if ($AtalhosWin11.ContainsKey($App)) { $AtalhosWin11[$App] } else { $App }
            try {
                Start-Process $AlvoExec
                Falar-Skynet("Abrindo $App no Windows 11.")
                return "Aplicativo ou painel iniciado: $AlvoExec"
            } catch {
                return "Nao consegui abrir '$App' diretamente: $_"
            }
        }
        "^modo-turbo" {'''
    code = code.replace('        "^modo-turbo" {', bloco_abrir, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[2/3] Lancador universal 'abrir:' instalado no skynet_core.ps1!")

# 3. Libera 'abrir:' no chat principal (/api/chat) mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    py_code = py_p.read_text(encoding="utf-8")
    if '"abrir:"' not in py_code:
        py_code = py_code.replace('"modo-turbo",', '"modo-turbo", "abrir:",')
        py_p.write_text(py_code, encoding="utf-8")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[3/3] Nucleo central Windows 11 + SKYNET ativado e interface 66827 preservada!")
