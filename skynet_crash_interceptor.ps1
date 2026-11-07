Add-Type -AssemblyName System.Speech
$S = New-Object System.Speech.Synthesis.SpeechSynthesizer
$UltimoId = (Get-WinEvent -FilterHashtable @{ LogName='Application'; Id=1000 } -MaxEvents 1 -ErrorAction SilentlyContinue).RecordId

while ($true) {
    try {
        $Ev = Get-WinEvent -FilterHashtable @{ LogName='Application'; Id=1000 } -MaxEvents 1 -ErrorAction SilentlyContinue
        if ($Ev -and $Ev.RecordId -ne $UltimoId) {
            $UltimoId = $Ev.RecordId
            $AppFalhou = ($Ev.Message -split "`n" | Select-Object -First 1) -replace 'Nome do aplicativo com falha:\s*|Faulting application name:\s*', ''
            $AppNome = ($AppFalhou -split ',')[0].Trim()
            if ($AppNome) {
                $S.SpeakAsync("Alerta do sistema: o aplicativo $AppNome parou de funcionar.") | Out-Null
            }
        }
    } catch {}
    Start-Sleep -Seconds 5
}
