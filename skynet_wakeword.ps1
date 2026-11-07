Add-Type -AssemblyName System.Speech, System.Windows.Forms, Microsoft.VisualBasic
$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }

try {
    $Rec = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    $Choices = New-Object System.Speech.Recognition.Choices
    $Choices.Add("Skynet")
    $Choices.Add("Ativar Skynet")
    $Gb = New-Object System.Speech.Recognition.GrammarBuilder($Choices)
    $Grammar = New-Object System.Speech.Recognition.Grammar($Gb)
    $Rec.LoadGrammar($Grammar)
    $Rec.SetInputToDefaultAudioDevice()

    while ($true) {
        $Result = $Rec.Recognize((New-TimeSpan -Seconds 5))
        if ($Result -and $Result.Confidence -ge 0.65) {
            # Verifica se o robo 8080 ja nao esta falando para evitar auto-escuta
            $Falando = $false
            try { $Falando = (Invoke-RestMethod -Uri "http://localhost:8080/falando" -TimeoutSec 2).falando } catch {}
            if (-not $Falando) {
                [console]::beep(900, 150)
                Start-Process "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\SkynetPowerShell\skynet_win_bridge.ps1 -Modo prompt"
                Start-Sleep -Seconds 3
            }
        }
    }
} catch {
    # Caso nao haja microfone conectado no momento, aguarda sem travar
    while ($true) { Start-Sleep 60 }
}
