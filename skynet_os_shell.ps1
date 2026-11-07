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
