import pathlib, re, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8-sig")

# Remove blocos antigos de /falando
code = re.sub(r'if \(\$Req\.Url\.AbsolutePath -eq "/falando"\)\s*\{.*?continue\s*\}', '', code, flags=re.S)

# Injeta /falando imediatamente após GetContext() antes de qualquer checagem de Authorization
bloco_falando = '''$Context = $Listener.GetContext()
                $Req = $Context.Request
                $Resp = $Context.Response
                if ($Req.Url.AbsolutePath -eq "/falando") {
                    $EstaFalando = ($Synthesizer.State -eq "Speaking") -or ($Global:FilaVoz.Count -gt 0)
                    $JsonOut = @{ falando = $EstaFalando } | ConvertTo-Json
                    $Buf = [System.Text.Encoding]::UTF8.GetBytes($JsonOut)
                    $Resp.ContentType = "application/json"
                    $Resp.Headers.Add("Access-Control-Allow-Origin", "*")
                    $Resp.OutputStream.Write($Buf, 0, $Buf.Length)
                    $Resp.Close()
                    continue
                }'''

code = code.replace('$Context = $Listener.GetContext()', bloco_falando, 1)

# Garante que Falar-Skynet sempre limpe falas duplicadas iguais na fila
nova_funcao = '''function Falar-Skynet([string]$Texto) {
    if ([string]::IsNullOrWhiteSpace($Texto) -or -not $Synthesizer) { return }
    if ($Global:FilaVoz.Contains($Texto)) { return }
    $Global:FilaVoz.Enqueue($Texto)
    if ($Synthesizer.State -ne 'Speaking' -and $Global:FilaVoz.Count -gt 0) {
        $Prox = $Global:FilaVoz.Dequeue()
        $Synthesizer.SpeakAsync($Prox) | Out-Null
    }
}'''
code = re.sub(r'function Falar-Skynet\(\[string\]\$Texto\)\s*\{.*?\n\}', nova_funcao, code, count=1, flags=re.S)

core_p.write_text(code, encoding="utf-8")
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[1/2] Motor Core 8080 atualizado com trava unica de voz!")
