import pathlib, re, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

# 1. Remove o bloco /falando de onde estava (depois da auth)
bloco_falando = '''if ($Req.Url.AbsolutePath -eq "/falando") {
                    $EstaFalando = ($Synthesizer.State -eq "Speaking") -or ($Global:FilaVoz.Count -gt 0)
                    $JsonOut = @{ falando = $EstaFalando } | ConvertTo-Json
                    $Buf = [System.Text.Encoding]::UTF8.GetBytes($JsonOut)
                    $Resp.ContentType = "application/json"
                    $Resp.Headers.Add("Access-Control-Allow-Origin", "*")
                    $Resp.OutputStream.Write($Buf, 0, $Buf.Length)
                    $Resp.Close()
                    continue
                }'''

code = re.sub(r'if \(\$Req\.Url\.AbsolutePath -eq "/falando"\)\s*\{.*?continue\s*\}', '', code, flags=re.S)

# 2. Insere o /falando logo após $Resp = $Context.Response (antes da checagem de Authorization)
if "$Resp = $Context.Response" in code:
    code = code.replace("$Resp = $Context.Response", "$Resp = $Context.Response\n                " + bloco_falando, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[OK] Rota /falando liberada antes da autenticacao com CORS!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado!")
