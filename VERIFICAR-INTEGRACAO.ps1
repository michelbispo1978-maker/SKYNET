function CheckLocalhostIntegration {
    Write-Host "=== SKYNET - Verificacao de Integracao Local ===" -ForegroundColor Cyan
    Write-Host "Só leitura, sem apagar nada, sem mudar interface, só 127.0.0.1" -ForegroundColor Gray

    # 1 - Porta 5000 em 127.0.0.1?
    $port = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalAddress -eq "127.0.0.1" }
    if ($port) { Write-Host "[OK] Porta 5000 ouvindo em 127.0.0.1" -ForegroundColor Green }
    else { Write-Host "[FALHOU] Porta 5000 nao esta em 127.0.0.1" -ForegroundColor Red }

    # 2 - Ollama rodando?
    try {
        $o = Invoke-RestMethod http://127.0.0.1:11434/api/tags -TimeoutSec 5
        Write-Host "[OK] Ollama rodando - Modelos: $($o.models.Count)" -ForegroundColor Green
    } catch {
        Write-Host "[FALHOU] Ollama nao respondeu em 127.0.0.1:11434" -ForegroundColor Red
    }

    # 3 - Startup tem só o AUTO?
    $startup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
    $files = Get-ChildItem $startup | Select-Object -ExpandProperty Name
    Write-Host "Startup: $($files -join ', ')" -ForegroundColor Yellow

    # 4 - Log
    $log = "D:\SKYNET\LOG-INTEGRACAO.txt"
    "Verificacao em $(Get-Date) - Porta 5000: $($null -ne $port) - Ollama: $($null -ne $o) - Startup: $($files -join ', ')" | Out-File $log -Append -Encoding utf8
    Write-Host "Log salvo em $log" -ForegroundColor Cyan
}

CheckLocalhostIntegration