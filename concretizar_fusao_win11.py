import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Cria o ícone nativo na Bandeja do Windows 11 (System Tray ao lado do relógio)
tray_ps = ps_dir / "skynet_tray.ps1"
tray_ps.write_text('''Add-Type -AssemblyName System.Windows.Forms, System.Drawing
$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }

function Enviar-Core($Cmd) {
    try {
        $B = @{ entrada = $Cmd } | ConvertTo-Json -Compress
        $R = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $Headers -Body ([System.Text.Encoding]::UTF8.GetBytes($B)) -TimeoutSec 60
        $Tray.ShowBalloonTip(4000, "SKYNET ($Cmd)", ($R.resultado -replace "`r`n", " "), [System.Windows.Forms.ToolTipIcon]::Info)
    } catch {
        $Tray.ShowBalloonTip(4000, "SKYNET Erro", "$_", [System.Windows.Forms.ToolTipIcon]::Error)
    }
}

$Tray = New-Object System.Windows.Forms.NotifyIcon
$Tray.Icon = [System.Drawing.SystemIcons]::Shield
$Tray.Text = "SKYNET Nucleo Windows 11 (Online)"
$Tray.Visible = $true

$Menu = New-Object System.Windows.Forms.ContextMenuStrip
$Menu.Items.Add("Abrir Central 66827 (Web)").Add_Click({ Start-Process "http://localhost:5000" })
$Menu.Items.Add("Ativar Modo Turbo Win 11").Add_Click({ Enviar-Core "modo-turbo" })
$Menu.Items.Add("Raio-X do Sistema").Add_Click({ Enviar-Core "raio-x" })
$Menu.Items.Add("Limpar Memoria RAM").Add_Click({ Enviar-Core "limpar-ram" })
$Menu.Items.Add("Sincronizar GitHub").Add_Click({ Enviar-Core "sincronizar-github" })
$Menu.Items.Add("Sair do Icone").Add_Click({ $Tray.Visible = $false; [System.Windows.Forms.Application]::Exit() })
$Tray.ContextMenuStrip = $Menu
$Tray.Add_DoubleClick({ Start-Process "http://localhost:5000" })

[System.Windows.Forms.Application]::Run()
''', encoding="utf-8")

# Inicia o ícone na sessão atual do usuário e registra na inicialização
startup_bat = pathlib.Path.home() / r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\SKYNET_Tray.bat"
startup_bat.write_text('@echo off\nstart "" powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\\SkynetPowerShell\\skynet_tray.ps1"\n', encoding="utf-8")
subprocess.Popen(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", str(tray_ps)])
print("[1/3] Icone nativo na Bandeja do Windows 11 ativado!")

# 2. Adiciona Controle de Dispositivos (Bluetooth/Audio/Hardware) + Sentinela de Copia no skynet_core.ps1
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

if "dispositivos" not in code:
    code = code.replace("rotina:", "rotina:|dispositivos|analisar-copia")
    bloco_hw = '''        "^dispositivos$" {
            $Bt = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue | Where-Object { $_.Status -eq "OK" } | Select-Object -First 6 | ForEach-Object { "- [BT] $($_.FriendlyName)" }
            $Audio = Get-PnpDevice -Class AudioEndpoint -ErrorAction SilentlyContinue | Where-Object { $_.Status -eq "OK" } | Select-Object -First 6 | ForEach-Object { "- [AUDIO] $($_.FriendlyName)" }
            return "=== DISPOSITIVOS ATIVOS WINDOWS 11 ===`n" + (($Bt + $Audio) -join "`n")
        }
        "^analisar-copia$" {
            $Clip = Get-Clipboard -Raw -ErrorAction SilentlyContinue
            if ([string]::IsNullOrWhiteSpace($Clip)) { return "Area de transferencia vazia." }
            if ($Clip.Length -gt 2500) { $Clip = $Clip.Substring(0, 2500) }
            $Payload = @{ model = "skynet:final"; prompt = "Analise, resuma ou explique o erro/texto copiado abaixo em portugues de forma direta:`n`n$Clip"; stream = $false } | ConvertTo-Json
            $Resp = Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $Payload -ContentType "application/json" -TimeoutSec 90
            return "=== ANALISE DO CTRL+C ===`n$($Resp.response)"
        }
        "^rotina:\\s*(.+)" {'''
    code = code.replace('        "^rotina:\\s*(.+)" {', bloco_hw, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[2/3] Comandos 'dispositivos' e 'analisar-copia' instalados no Core 8080!")

# 3. Libera novos gatilhos no chat principal (/api/chat) mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"dispositivos"' not in p_txt:
        py_p.write_text(p_txt.replace('"rotina:",', '"rotina:", "dispositivos", "analisar-copia",'), encoding="utf-8")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[3/3] Fusao Windows 11 + SKYNET 100% concretizada!")
