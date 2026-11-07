[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
# Skynet Telegram Bridge v1.0 - Controle Remoto Blindado
$BotToken = "8765758342:AAE8Q8cINhDOmjjhp0yfFORAeLAeNk1xdic"
$AdminId  = "257638854216"
$BridgeUrl = "http://localhost:5000/api/robo-bridge"

if ($BotToken -eq "SEU_TOKEN_AQUI") { exit }

$Offset = 0
while ($true) {
    try {
        $Updates = Invoke-RestMethod -Uri "https://telegram.org" -TimeoutSec 35
        foreach ($Up in $Updates.result) {
            $Offset = $Up.update_id + 1
            $ChatId = "$($Up.message.chat.id)"
            $Texto = "$($Up.message.text)".Trim()

            # Trava de segurança: ignora qualquer pessoa que não seja o seu ID
            if ($ChatId -ne $AdminId -or -not $Texto) { continue }

                        if ($Texto -eq "/tela") {
                $Body = @{ entrada = "ver-tela" } | ConvertTo-Json
                $Res = Invoke-RestMethod -Uri $BridgeUrl -Method Post -Body $Body -ContentType "application/json" -TimeoutSec 90
                $Resp = "[$($Res.decisao)]: $($Res.resultado)"
            } elseif ($Texto -eq "/status") {
                $St = Invoke-RestMethod -Uri $BridgeUrl -Method Get
                $Resp = "SKYNET ONLINE | CPU: $($St.cpu)% | RAM: $($St.ram)% | Versão: $($St.versao)"
            } else {
                $Cmd = if ($Texto -eq "/ram") { "limpar-ram" } elseif ($Texto -eq "/rede") { "scan-rede" } else { $Texto }
                $Body = @{ entrada = $Cmd; modelo = "skynet:final" } | ConvertTo-Json
                $Res = Invoke-RestMethod -Uri $BridgeUrl -Method Post -Body $Body -ContentType "application/json" -TimeoutSec 60
                $Resp = "[$($Res.decisao)]: $($Res.resultado)"
            }

            $SendBody = @{ chat_id = $ChatId; text = $Resp } | ConvertTo-Json
            Invoke-RestMethod -Uri "https://telegram.org" -Method Post -Body $SendBody -ContentType "application/json; charset=utf-8" | Out-Null
        }
    } catch { Start-Sleep -Seconds 5 }
}



