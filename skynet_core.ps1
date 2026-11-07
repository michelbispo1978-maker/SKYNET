# Configurações Iniciais
$Port = 8080
$Url = "http://localhost:$Port/"
$DbDir = Join-Path $PSScriptRoot "database"

# Cria a pasta do banco de dados se não existir
if (-not (Test-Path $DbDir)) { New-Item -ItemType Directory -Path $DbDir | Out-Null }

# Inicializa o Listener HTTP do .NET
$Listener = New-Object System.Net.HttpListener
$Listener.Prefixes.Add($Url)

try {
    $Listener.Start()
    Write-Host "[SKYNET CORE] Servidor PowerShell operacional em $Url" -ForegroundColor Cyan
    Write-Host "[INFO] Pressione CTRL+C para desativar a colmeia.`n" -ForegroundColor Yellow

    # Loop infinito para processamento contínuo
    while ($Listener.IsListening) {
        # Aguarda uma conexão (Bloqueia até receber uma requisição)
        $Context = $Listener.GetContext()
        $Request = $Context.Request
        $Response = $Context.Response

        Write-Host "[REQUISIÇÃO] $($Request.HttpMethod) -> $($Request.Url.AbsolutePath)" -ForegroundColor Green

        # Configura os Headers Padrão de Resposta (JSON)
        $Response.ContentType = "application/json; charset=utf-8"
        $Response.Headers.Add("Access-Control-Allow-Origin", "*") # Libera CORS

        $ResponseData = ""
        
        # ROTEADOR DE ENDPOINTS
        switch ($Request.Url.AbsolutePath) {
            "/status" {
                # Coleta métricas reais do sistema operacional
                $Uptime = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
                $OsName = (Get-CimInstance Win32_OperatingSystem).Caption
                
                $StatusObj = @{
                    sistema = "Skynet PowerShell Core"
                    status  = "ONLINE"
                    so      = $OsName
                    ultimo_boot = $Uptime
                }
                $ResponseData = $StatusObj | ConvertTo-Json
                $Response.StatusCode = 200
            }

            "/command" {
                if ($Request.HttpMethod -eq "POST") {
                    # Lê o corpo (Payload) da requisição
                    $Reader = New-Object System.IO.StreamReader($Request.InputStream)
                    $Body = $Reader.ReadToEnd()
                    
                    # Valida se o conteúdo enviado é um JSON válido
                    try {
                        $JsonTest = $Body | ConvertTo-Html # Apenas validação rápida
                        
                        # Gera um ID único com base no timestamp
                        $Id = (Get-Date).Ticks
                        $FileName = "cmd_$Id.json"
                        $FilePath = Join-Path $DbDir $FileName
                        
                        # Salva o arquivo no "Banco de Dados"
                        Set-Content -Path $FilePath -Value $Body
                        
                        $ResultObj = @{
                            status = "SUCCESS"
                            id_registro = $Id
                            mensagem = "Diretiva gravada com sucesso nas sub-rotinas do PowerShell."
                        }
                        $ResponseData = $ResultObj | ConvertTo-Json
                        $Response.StatusCode = 200
                    }
                    catch {
                        $ResponseData = @{ erro = "JSON invalido ou corrompido." } | ConvertTo-Json
                        $Response.StatusCode = 400
                    }
                } else {
                    $ResponseData = @{ erro = "Metodo nao permitido. Use POST." } | ConvertTo-Json
                    $Response.StatusCode = 405
                }
            }

            Default {
                # Rota não encontrada
                $ResponseData = @{ erro = "Endpoint desconhecido pela Skynet." } | ConvertTo-Json
                $Response.StatusCode = 404
            }
        }

        # Converte a string de resposta em bytes e envia ao cliente
        $Buffer = [System.Text.Encoding]::UTF8.GetBytes($ResponseData)
        $Response.ContentLength64 = $Buffer.Length
        $Response.OutputStream.Write($Buffer, 0, $Buffer.Length)
        
        # Fecha a conexão da requisição atual
        $Response.Close()
    }
}
catch {
    Write-Host "`n[ALERTA] Servidor interrompido ou erro crítico: $_" -ForegroundColor Red
}
finally {
    $Listener.Stop()
    Write-Host "[SKYNET CENTRAL] Servidor desligado com segurança." -ForegroundColor Magenta
}
