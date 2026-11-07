Add-Type -AssemblyName System.Speech, System.Windows.Forms
$S = New-Object System.Speech.Synthesis.SpeechSynthesizer

Register-ObjectEvent -InputObject ([System.Net.NetworkInformation.NetworkChange]) -EventName NetworkAvailabilityChanged -SourceIdentifier "SkynetNetChange" -Action {
    if ($Event.SourceEventArgs.IsAvailable) {
        $S.SpeakAsync("Conexao de rede restabelecida.") | Out-Null
    } else {
        $S.SpeakAsync("Atencao: conexao de rede perdida.") | Out-Null
    }
} | Out-Null

Register-ObjectEvent -InputObject ([Microsoft.Win32.SystemEvents]) -EventName PowerModeChanged -SourceIdentifier "SkynetPowerChange" -Action {
    $Modo = $Event.SourceEventArgs.Mode
    if ($Modo -eq "Suspend") {
        [System.GC]::Collect()
    } elseif ($Modo -eq "Resume") {
        $S.SpeakAsync("Sistema retomado da suspensao. Motores Skynet online.") | Out-Null
    } elseif ($Modo -eq "StatusChange") {
        $S.SpeakAsync("Estado de energia do Windows alterado.") | Out-Null
    }
} | Out-Null

while ($true) { Start-Sleep 30 }
