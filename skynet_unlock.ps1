$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
$Body = @{ entrada = "energia" } | ConvertTo-Json -Compress
try {
    $R = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $Headers -Body ([System.Text.Encoding]::UTF8.GetBytes($Body)) -TimeoutSec 15
    Add-Type -AssemblyName System.Speech
    $S = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $S.Speak("Bem-vindo de volta, Michel. Sistemas Skynet operando normalmente.")
} catch {}
