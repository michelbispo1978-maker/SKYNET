import pathlib, re, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8-sig")

# 1. Remove qualquer Register-ObjectEvent órfão sobre $Synthesizer no início ou duplicado
code = re.sub(r'Register-ObjectEvent\s+-InputObject\s+\$Synthesizer\s+-EventName\s+SpeakCompleted\s+-Action\s*\{.*?\}\s*\|\s*Out-Null\r?\n?', '', code, flags=re.S)

# 2. Garante inicialização limpa do SpeechSynthesizer + FilaVoz no início do script
init_voz = '''Add-Type -AssemblyName System.Speech
if (-not $Synthesizer) { $Synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer }
$Global:FilaVoz = [System.Collections.Queue]::Synchronized((New-Object System.Collections.Queue))
function Falar-Skynet([string]$Texto) {
    if ([string]::IsNullOrWhiteSpace($Texto) -or -not $Synthesizer) { return }
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

# Remove definição duplicada de Falar-Skynet se já existir abaixo
code = re.sub(r'\$Global:FilaVoz\s*=.*?function Falar-Skynet\(.*?\n\}\r?\n?', '', code, flags=re.S)

code = init_voz + "\n" + code.lstrip()
core_p.write_text(code, encoding="utf-8")
print("[OK] Inicializacao de voz e Register-ObjectEvent corrigidos no skynet_core.ps1!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado!")
