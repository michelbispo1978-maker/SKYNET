import pathlib, subprocess

tg_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_telegram.ps1")
code = tg_p.read_text(encoding="utf-8")

bloco_doc = '''            $Msg = $Item.message
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
                    New-Item -ItemType Directory -Path "C:\\SkynetPowerShell\\temp" -Force | Out-Null
                    $LocalDoc = "C:\\SkynetPowerShell\\temp\\$FileName"
                    Invoke-WebRequest -Uri "https://telegram.org" -OutFile $LocalDoc -TimeoutSec 30
                    $PayloadDoc = @{ entrada = "ler-tudo: $LocalDoc" } | ConvertTo-Json -Compress
                    $ResDoc = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $HeadersCore -Body ([System.Text.Encoding]::UTF8.GetBytes($PayloadDoc)) -TimeoutSec 120
                    Enviar-TextoTg $Remetente $ResDoc.resultado
                } catch {
                    Enviar-TextoTg $Remetente "Erro ao processar arquivo do Telegram: $_"
                }
                continue
            }

            if (-not $Msg.text) { continue }'''

if "$Msg.document" not in code:
    old_chunk = '''            $Msg = $Item.message
            if (-not $Msg -or -not $Msg.text) { continue }
            $Remetente = "$($Msg.chat.id)"
            if ($Remetente -ne $ChatAutorizado) { continue }'''
    code = code.replace(old_chunk, bloco_doc, 1)
    tg_p.write_text(code, encoding="utf-8")
    print("[OK] Leitor de documentos enviado pelo Telegram ativado!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetTelegramImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetTelegramImortal'"])
print("[CONCLUIDO] Bot do Telegram reiniciado com suporte a arquivos!")
