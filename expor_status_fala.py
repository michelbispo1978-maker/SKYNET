import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

rota_falando = '''if ($Req.Url.AbsolutePath -eq "/falando") {
                    $EstaFalando = ($Synthesizer.State -eq "Speaking") -or ($Global:FilaVoz.Count -gt 0)
                    $JsonOut = @{ falando = $EstaFalando } | ConvertTo-Json
                    $Buf = [System.Text.Encoding]::UTF8.GetBytes($JsonOut)
                    $Resp.ContentType = "application/json"
                    $Resp.OutputStream.Write($Buf, 0, $Buf.Length)
                    $Resp.Close()
                    continue
                }
                if ($Req.Url.AbsolutePath -eq "/command")'''

if "/falando" not in code:
    code = code.replace('if ($Req.Url.AbsolutePath -eq "/command")', rota_falando, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[OK] Endpoint /falando adicionado no skynet_core.ps1!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado!")
