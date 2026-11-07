$SecretsPath = "C:\SkynetPowerShell\secrets.json"
if (-not (Test-Path $SecretsPath)) {
    Write-Host "[ERRO] Arquivo secrets.json nao encontrado!" -ForegroundColor Red
    exit 1
}

$Secrets = Get-Content $SecretsPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Token = $Secrets.TELEGRAM_BOT_TOKEN
$ChatAutorizado = "$($Secrets.TELEGRAM_CHAT_ID)".Trim()

if ($Token -match "COLE_SEU" -or [string]::IsNullOrWhiteSpace($Token)) {
    Write-Host "[AVISO] Abra C:\SkynetPowerShell\secrets.json e cole seu novo Token do @BotFather primeiro!" -ForegroundColor Yellow
    exit 1
}

$BaseUri = "https://telegram.org"
$Offset = 0
$HeadersCore = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }

function Enviar-TextoTg($ChatId, $Texto) {
    if ([string]::IsNullOrWhiteSpace($Texto)) { $Texto = "Comando executado." }
    if ($Texto.Length -gt 3900) { $Texto = $Texto.Substring(0, 3900) + "`n...[truncado]" }
    $Body = @{ chat_id = $ChatId; text = $Texto } | ConvertTo-Json -Compress
    try { Invoke-RestMethod -Uri "$BaseUri/sendMessage" -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($Body)) -ContentType "application/json" -TimeoutSec 15 | Out-Null } catch {}
}

function Enviar-FotoTg($ChatId, $CaminhoFoto, $Legenda) {
    if (-not (Test-Path $CaminhoFoto)) { return }
    try {
        curl.exe -s -F "chat_id=$ChatId" -F "photo=@$CaminhoFoto" -F "caption=$Legenda" "$BaseUri/sendPhoto" | Out-Null
    } catch {}
}

# Descobre seu CHAT_ID automaticamente caso ainda esteja vazio no secrets.json
if ($ChatAutorizado -match "COLE_SEU" -or [string]::IsNullOrWhiteSpace($ChatAutorizado)) {
    Write-Host "[AGUARDANDO] Envie um 'oi' para o seu bot no Telegram agora para capturar seu CHAT_ID automaticamente..." -ForegroundColor Cyan
    while ($true) {
        try {
            $Upd = Invoke-RestMethod -Uri "$BaseUri/getUpdates?timeout=10" -TimeoutSec 15
            if ($Upd.result.Count -gt 0) {
                $Ultimo = $Upd.result[-1]
                $ChatAutorizado = "$($Ultimo.message.chat.id)"
                $Offset = $Ultimo.update_id + 1
                $Secrets.TELEGRAM_CHAT_ID = $ChatAutorizado
                $Secrets | ConvertTo-Json -Depth 3 | Set-Content $SecretsPath -Encoding UTF8
                Enviar-TextoTg $ChatAutorizado "SKYNET CONECTADA! Seu Chat ID ($ChatAutorizado) foi vinculado com seguranca."
                Write-Host "[OK] Chat ID $ChatAutorizado salvo no secrets.json!" -ForegroundColor Green
                break
            }
        } catch {}
        Start-Sleep 2
    }
}

Write-Host "[ONLINE] Ponte Telegram -> Skynet Core 8080 ativa!" -ForegroundColor Green

while ($true) {
    try {
        $Updates = Invoke-RestMethod -Uri "$BaseUri/getUpdates?offset=$Offset&timeout=20" -TimeoutSec 30
        foreach ($Item in $Updates.result) {
            $Offset = $Item.update_id + 1
            $Msg = $Item.message
            if (-not $Msg) { continue }
            $Remetente = "$($Msg.chat.id)"
            if ($Remetente -ne $ChatAutorizado) { continue }

            # Se o usuario enviou um documento (PDF, DOCX, TXT, PY, etc.) pelo Telegram
            if ($Msg.document) {
                $FileId = $Msg.document.file_id
                $FileName = $Msg.document.file_name
                Enviar-TextoTg $Remetente "Recebi '$FileName'. Baixando e analisando com o Leitor Universal..."
                try {
                    $FileInfo = Invoke-RestMethod -Uri "$BaseUri/getFile?file_id=$FileId" -TimeoutSec 20
                    $FilePathTg = $FileInfo.result.file_path
                    New-Item -ItemType Directory -Path "C:\SkynetPowerShell\temp" -Force | Out-Null
                    $LocalDoc = "C:\SkynetPowerShell\temp\$FileName"
                    Invoke-WebRequest -Uri "https://telegram.org" -OutFile $LocalDoc -TimeoutSec 30
                    $PayloadDoc = @{ entrada = "ler-tudo: $LocalDoc" } | ConvertTo-Json -Compress
                    $ResDoc = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $HeadersCore -Body ([System.Text.Encoding]::UTF8.GetBytes($PayloadDoc)) -TimeoutSec 120
                    Enviar-TextoTg $Remetente $ResDoc.resultado
                } catch {
                    Enviar-TextoTg $Remetente "Erro ao processar arquivo do Telegram: $_"
                }
                continue
            }

            if (-not $Msg.text) { continue }

            $CmdTexto = $Msg.text.Trim()
            $Payload = @{ entrada = $CmdTexto } | ConvertTo-Json -Compress
            $Res = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $HeadersCore -Body ([System.Text.Encoding]::UTF8.GetBytes($Payload)) -TimeoutSec 90
            $Resposta = if ($Res.resultado) { $Res.resultado } else { "$($Res.erro)" }

            Enviar-TextoTg $Remetente $Resposta

            if ($CmdTexto.ToLower().StartsWith("ver-tela")) {
                $PrintPath = Get-ChildItem "C:\SkynetPowerShell\*.png", "C:\SkynetPowerShell\temp\*.png" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
                if ($PrintPath) { Enviar-FotoTg $Remetente $PrintPath.FullName "Captura de tela atual" }
            }
        }
    } catch {
        Start-Sleep 3
    }
}
