
# === ATALHOS GLOBAIS DO MODO SHELL SKYNET ===
Start-Job -Name "SkynetShellHotkeys" -ScriptBlock {
    Add-Type -TypeDefinition @"
    using System;
    using System.Runtime.InteropServices;
    public class SkynetHotkeys {
        [DllImport("user32.dll")] public static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);
        [DllImport("user32.dll")] public static extern bool GetMessage(out MSG lpMsg, IntPtr hWnd, uint wMsgFilterMin, uint wMsgFilterMax);
        public struct MSG { public IntPtr hwnd; public uint message; public IntPtr wParam; public IntPtr lParam; public uint time; public int pt_x; public int pt_y; }
    }
"@
    # Modifiers: Ctrl (0x0002) + Alt (0x0001) = 0x0003
    [SkynetHotkeys]::RegisterHotKey([IntPtr]::Zero, 1, 0x0003, 0x45) | Out-Null # Ctrl+Alt+E (Explorer)
    [SkynetHotkeys]::RegisterHotKey([IntPtr]::Zero, 2, 0x0003, 0x54) | Out-Null # Ctrl+Alt+T (Terminal)
    [SkynetHotkeys]::RegisterHotKey([IntPtr]::Zero, 3, 0x0003, 0x46) | Out-Null # Ctrl+Alt+F (Firefox/Navegador)
    [SkynetHotkeys]::RegisterHotKey([IntPtr]::Zero, 4, 0x0003, 0x50) | Out-Null # Ctrl+Alt+P (Pasta SkynetPowerShell)
    [SkynetHotkeys]::RegisterHotKey([IntPtr]::Zero, 5, 0x0003, 0x57) | Out-Null # Ctrl+Alt+W (Restaurar Windows 11)

    $Msg = New-Object SkynetHotkeys+MSG
    while ([SkynetHotkeys]::GetMessage([ref]$Msg, [IntPtr]::Zero, 0, 0)) {
        if ($Msg.message -eq 0x0312) {
            switch ([int]$Msg.wParam) {
                1 { Start-Process "explorer.exe" }
                2 { Start-Process "powershell.exe" -Verb RunAs }
                3 { try { Start-Process "firefox.exe" } catch { Start-Process "msedge.exe" } }
                4 { Start-Process "explorer.exe" -ArgumentList "C:\SkynetPowerShell" }
                5 {
                    Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" -Name "Shell" -ErrorAction SilentlyContinue
                    Start-Process "explorer.exe"
                }
            }
        }
    }
} | Out-Null

# Garante que os motores da colmeia estao ativos
foreach ($t in @("SkynetCoreImortal", "SkynetWeb5000Imortal", "SkynetAutonomyImortal", "SkynetTelegramImortal")) {
    Start-ScheduledTask -TaskName $t -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 2

# Abre a Interface 66827 em tela cheia como ambiente principal do sistema
$Edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$Chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (Test-Path $Chrome) {
    Start-Process $Chrome -ArgumentList "--app=http://localhost:5000 --start-maximized"
} elseif (Test-Path $Edge) {
    Start-Process $Edge -ArgumentList "--app=http://localhost:5000 --start-maximized"
} else {
    Start-Process "http://localhost:5000"
}

# Inicia o Mini-HUD e mantem o loop vivo do Shell
Start-Process "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\SkynetPowerShell\skynet_hud.ps1"
Add-Type -AssemblyName System.Speech
$S = New-Object System.Speech.Synthesis.SpeechSynthesizer
$S.SpeakAsync("Sistema operacional Skynet carregado como interface principal.") | Out-Null

while ($true) { Start-Sleep -Seconds 15 }
