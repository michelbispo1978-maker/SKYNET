import pathlib, subprocess, winreg

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Cria handler para protocolo skynet:// no Windows 11
uri_handler = ps_dir / "skynet_uri_handler.ps1"
uri_handler.write_text('''param([string]$RawUri)
Add-Type -AssemblyName System.Web, System.Windows.Forms
$Cmd = $RawUri -replace '^skynet://', ''
$Cmd = [System.Web.HttpUtility]::UrlDecode($Cmd).Trim('/')
if ([string]::IsNullOrWhiteSpace($Cmd)) { $Cmd = "raio-x" }

$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
try {
    $Body = @{ entrada = $Cmd } | ConvertTo-Json -Compress
    $Res = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $Headers -Body ([System.Text.Encoding]::UTF8.GetBytes($Body)) -TimeoutSec 90
    $Texto = if ($Res.resultado) { $Res.resultado } else { "$($Res.erro)" }
    [System.Windows.Forms.MessageBox]::Show($Texto, "SKYNET Protocolo ($Cmd)", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information) | Out-Null
} catch {
    [System.Windows.Forms.MessageBox]::Show("Erro ao executar skynet://$Cmd : $_", "SKYNET", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error) | Out-Null
}
''', encoding="utf-8")

# Registra skynet:// no Registro do Windows 11 (HKCU)
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\skynet") as k:
    winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "URL:SKYNET Protocol")
    winreg.SetValueEx(k, "URL Protocol", 0, winreg.REG_SZ, "")
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\skynet\shell\open\command") as kc:
    winreg.SetValueEx(kc, "", 0, winreg.REG_SZ, f'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "{uri_handler}" "%1"')
print("[1/2] Protocolo nativo skynet:// registrado no Windows 11!")

# 2. Adiciona janela-ativa, focar:, areas virtuais e modo-turbo ao skynet_core.ps1
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

win11_api = '''Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class Win11Native {
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
}
"@
'''

if "class Win11Native" not in code:
    code = win11_api + "\n" + code

if "janela-ativa" not in code:
    code = code.replace("investigar:", "investigar:|janela-ativa|focar:|nova-area|desktop-esq|desktop-dir|modo-turbo")
    bloco_win11 = '''        "^janela-ativa$" {
            $Hwnd = [Win11Native]::GetForegroundWindow()
            $Sb = New-Object System.Text.StringBuilder 256
            [void][Win11Native]::GetWindowText($Hwnd, $Sb, 256)
            $PidOut = 0
            [void][Win11Native]::GetWindowThreadProcessId($Hwnd, [ref]$PidOut)
            $Proc = Get-Process -Id $PidOut -ErrorAction SilentlyContinue
            $Info = "=== JANELA ATIVA WINDOWS 11 ===`nTitulo: $($Sb.ToString())`nProcesso: $($Proc.ProcessName) (PID: $PidOut)"
            Falar-Skynet("Voce esta usando $($Proc.ProcessName).")
            return $Info
        }
        "^focar:\\s*(.+)" {
            $Alvo = $Matches.Trim()
            $Proc = Get-Process | Where-Object { $_.MainWindowTitle -match $Alvo -or $_.ProcessName -match $Alvo } | Select-Object -First 1
            if ($Proc -and $Proc.MainWindowHandle -ne [IntPtr]::Zero) {
                [void][Win11Native]::ShowWindow($Proc.MainWindowHandle, 9)
                [void][Win11Native]::SetForegroundWindow($Proc.MainWindowHandle)
                Falar-Skynet("Focando em $($Proc.ProcessName).")
                return "Janela ativada: $($Proc.MainWindowTitle)"
            }
            return "Nenhuma janela aberta encontrada para '$Alvo'."
        }
        "^nova-area$" {
            [Win11Native]::keybd_event(0x5B, 0, 0, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x11, 0, 0, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x44, 0, 0, [UIntPtr]::Zero)
            Start-Sleep -Milliseconds 60
            [Win11Native]::keybd_event(0x44, 0, 2, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x11, 0, 2, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x5B, 0, 2, [UIntPtr]::Zero)
            return "Nova area de trabalho virtual criada no Windows 11."
        }
        "^desktop-esq$" {
            [Win11Native]::keybd_event(0x5B, 0, 0, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x11, 0, 0, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x25, 0, 0, [UIntPtr]::Zero)
            Start-Sleep -Milliseconds 60
            [Win11Native]::keybd_event(0x25, 0, 2, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x11, 0, 2, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x5B, 0, 2, [UIntPtr]::Zero)
            return "Alternado para a area de trabalho virtual a esquerda."
        }
        "^desktop-dir$" {
            [Win11Native]::keybd_event(0x5B, 0, 0, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x11, 0, 0, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x27, 0, 0, [UIntPtr]::Zero)
            Start-Sleep -Milliseconds 60
            [Win11Native]::keybd_event(0x27, 0, 2, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x11, 0, 2, [UIntPtr]::Zero)
            [Win11Native]::keybd_event(0x5B, 0, 2, [UIntPtr]::Zero)
            return "Alternado para a area de trabalho virtual a direita."
        }
        "^modo-turbo$" {
            powercfg /setactive SCHEME_MIN 2>$null
            [System.GC]::Collect()
            Falar-Skynet("Modo turbo do Windows 11 ativado. Energia em alto desempenho e memoria otimizada.")
            Notificar-Windows "SKYNET MODO TURBO" "Plano Alto Desempenho ativado no Windows 11!"
            return "=== MODO TURBO WINDOWS 11 ATIVADO ===`nPlano de Energia: Alto Desempenho (SCHEME_MIN)`nMemoria RAM liberada."
        }
        "^investigar:\\s*(.+)" {'''
    code = code.replace('        "^investigar:\\s*(.+)" {', bloco_win11, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[2/2] Modulos nativos Windows 11 instalados no skynet_core.ps1!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado com reconhecimento total Windows 11!")
