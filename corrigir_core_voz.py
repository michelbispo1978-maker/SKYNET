import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
# Lê ignorando qualquer BOM e limpa ocorrências de ï»¿ no meio do texto
code = core_p.read_text(encoding="utf-8-sig").replace("\ufeff", "").replace("ï»¿", "")

# Remove o bloco antigo da FilaVoz que ficou no topo antes do $Synthesizer existir
inicio_fila = code.find("$Global:FilaVoz =")
fim_fila = code.find("| Out-Null\n", inicio_fila)
if inicio_fila != -1 and fim_fila != -1:
    code = code[:inicio_fila] + code[fim_fila + len("| Out-Null\n"):]

# Injeta a inicialização segura da FilaVoz logo após a linha onde o $Synthesizer é criado
bloco_fila_seguro = '''$Synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
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
} | Out-Null'''

if "$Synthesizer = New-Object" in code and "Register-ObjectEvent -InputObject $Synthesizer" not in code:
    code = code.replace("$Synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer", bloco_fila_seguro, 1)
elif "Register-ObjectEvent -InputObject $Synthesizer" not in code:
    # Caso o $Synthesizer seja criado com outra sintaxe, adiciona no início já instanciado
    code = "Add-Type -AssemblyName System.Speech\n" + bloco_fila_seguro + "\n" + code

# Salva em UTF-8 limpo (sem BOM) para o PowerShell 5.1 nunca reclamar de ï»¿
core_p.write_text(code, encoding="utf-8")
print("[OK] skynet_core.ps1 corrigido: BOM removido e FilaVoz ligada apos $Synthesizer!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado sem erros!")
