Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden -ErrorAction SilentlyContinue
$Ativo = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*skynet_core.ps1*" }
if (-not $Ativo) {
    Start-Process "powershell.exe" -ArgumentList '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\SkynetPowerShell\skynet_core.ps1"' -WindowStyle Hidden
    Start-Sleep -Seconds 2
}
Write-Host "[OK] Robo SKYNET Core (Porta 8080) e Ollama ativos e operacionais!" -ForegroundColor Green
Start-Sleep -Seconds 2
