import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

if "portas-abertas" not in code:
    code = code.replace("limpar-tudo", "limpar-tudo|portas-abertas|bloquear-ip:|clicar-pos:|atalho:|senhas-wifi|reset-rede")

    # Adiciona API nativa de mouse na classe Win11Native
    if "SetCursorPos" not in code:
        code = code.replace(
            'public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);',
            'public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);\n    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);\n    [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, UIntPtr dwExtraInfo);'
        )

    bloco_profundo = r'''        "^portas-abertas$" {
            $Conns = Get-NetTCPConnection -State Established,Listen -ErrorAction SilentlyContinue | Select-Object -First 15 | ForEach-Object {
                $PName = (Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName
                "[$($_.State)] Porta $($_.LocalPort) -> $($_.RemoteAddress):$($_.RemotePort) ($PName)"
            }
            return "=== MONITOR DE PORTAS & CONEXOES WIN 11 ===`n" + ($Conns -join "`n")
        }
        "^bloquear-ip:\s*(.+)" {
            $IpAlvo = $Matches.Trim()
            $RuleName = "SKYNET_BLOCK_$($IpAlvo -replace '[^\d\.]','_')"
            New-NetFirewallRule -DisplayName $RuleName -Direction Outbound -RemoteAddress $IpAlvo -Action Block -ErrorAction SilentlyContinue | Out-Null
            New-NetFirewallRule -DisplayName "${RuleName}_IN" -Direction Inbound -RemoteAddress $IpAlvo -Action Block -ErrorAction SilentlyContinue | Out-Null
            Falar-Skynet("Endereco IP bloqueado no Firewall do Windows 11.")
            return "Firewall Windows 11: IP '$IpAlvo' bloqueado (Entrada e Saida)."
        }
        "^clicar-pos:\s*(\d+)\s*,\s*(\d+)" {
            $X = [int]$Matches
            $Y = [int]$Matches
            [void][Win11Native]::SetCursorPos($X, $Y)
            Start-Sleep -Milliseconds 50
            [Win11Native]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
            [Win11Native]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
            return "Clique esquerdo executado na coordenada ($X, $Y)."
        }
        "^atalho:\s*(.+)" {
            $Teclas = $Matches.Trim()
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.SendKeys]::SendWait($Teclas)
            return "Atalho de teclado '$Teclas' enviado para a janela ativa."
        }
        "^senhas-wifi$" {
            $Perfis = (netsh wlan show profiles) | Select-String ":\s+(.+)$" | ForEach-Object { $_.Matches.Groups.Value.Trim() }
            if (-not $Perfis) { return "Nenhum perfil Wi-Fi salvo encontrado neste computador." }
            $ResWifi = foreach ($p in $Perfis) {
                $Det = (netsh wlan show profile name="$p" key=clear) | Select-String "Conte.do da Chave|Key Content"
                $Senha = if ($Det) { ($Det -split ":")[-1].Trim() } else { "(Aberta / Sem senha)" }
                "- Rede: $p | Senha: $Senha"
            }
            return "=== SENHAS WI-FI SALVAS NO WINDOWS 11 ===`n" + ($ResWifi -join "`n")
        }
        "^reset-rede$" {
            ipconfig /flushdns | Out-Null
            ipconfig /release | Out-Null
            ipconfig /renew | Out-Null
            Falar-Skynet("Cache DNS limpo e conexao de rede renovada.")
            return "Rede Windows 11 renovada (DNS limpo e IP atualizado)."
        }
        "^limpar-tudo$" {'''
    code = code.replace('        "^limpar-tudo$" {', bloco_profundo, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[1/3] Monitor de Portas, Firewall, Mouse, Wi-Fi e Reset de Rede instalados!")

# 2. Libera novos gatilhos no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"portas-abertas"' not in p_txt:
        py_p.write_text(p_txt.replace('"limpar-tudo",', '"limpar-tudo", "portas-abertas", "bloquear-ip:", "clicar-pos:", "atalho:", "senhas-wifi", "reset-rede",'), encoding="utf-8")
        print("[2/3] Gatilhos liberados no chat principal (/api/chat)!")

# 3. Cria atalhos indexáveis na Busca Global do Windows 11 (Menu Iniciar)
ps_search = '''
$Wsh = New-Object -ComObject WScript.Shell
$ProgDir = [Environment]::GetFolderPath("StartMenu") + "\\Programs\\SKYNET Win11"
New-Item -ItemType Directory -Path $ProgDir -Force | Out-Null
$Acoes = @{
    "SKYNET Modo Turbo"  = "modo-turbo"
    "SKYNET Limpar Tudo" = "limpar-tudo"
    "SKYNET Status Total" = "status-total"
    "SKYNET Win11 Enxuto" = "win11-essencial"
}
foreach ($k in $Acoes.Keys) {
    $Sc = $Wsh.CreateShortcut("$ProgDir\\$k.lnk")
    $Sc.TargetPath = "powershell.exe"
    $Sc.Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"C:\\SkynetPowerShell\\skynet_uri_handler.ps1`" `"skynet://$($Acoes[$k])`""
    $Sc.IconLocation = "shell32.dll,23"
    $Sc.Save()
}
'''
subprocess.run(["powershell", "-NoProfile", "-Command", ps_search], check=True)
print("[3/3] Atalhos nativos indexados na Pesquisa Global do Windows 11 (Win + S)!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
