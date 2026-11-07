import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

funcao_voz = '''$Global:FilaVoz = [System.Collections.Queue]::Synchronized((New-Object System.Collections.Queue))
function Falar-Skynet([string]$Texto) {
    if ([string]::IsNullOrWhiteSpace($Texto)) { return }
    $Global:FilaVoz.Enqueue($Texto)
    if ($Synthesizer.State -ne 'Speaking' -and $Global:FilaVoz.Count -gt 0) {
        $Prox = $Global:FilaVoz.Dequeue()
        $Synthesizer.SpeakAsync($Prox) | Out-Null
    }
}
Register-ObjectEvent -InputObject $Synthesizer -EventName SpeakCompleted -Action {
    if ($Global:FilaVoz.Count -gt 0) {
        $Prox = $Global:FilaVoz.Dequeue()
        $Event.Sender.SpeakAsync($Prox) | Out-Null
    }
} | Out-Null
'''

if "function Falar-Skynet" not in code:
    code = code.replace('$Synthesizer.SpeakAsync(', 'Falar-Skynet(')
    code = code.replace(') | Out-Null', ')')
    code = funcao_voz + "\n" + code
    core_p.write_text(code, encoding="utf-8")
    print("[OK] Fila de voz anti-atropelamento ativada no skynet_core.ps1!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core reiniciado com fila unica de voz!")
