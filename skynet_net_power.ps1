Add-Type -AssemblyName System.Speech, System.Windows.Forms
$S = New-Object System.Speech.Synthesis.SpeechSynthesizer

Register-ObjectEvent -InputObject ([System.Net.NetworkInformation.NetworkChange]) -EventName NetworkAvailabilityChanged -SourceIdentifier "SkynetNetChange" -Action {
    $Online = $Event.SourceEventArgs.IsAvailable
    if ($Online) {
        $S.SpeakAsync("Conexao de rede restabelecida.") | Out-Null
    } else {
        $S.SpeakAsync("Atencao: conexao de rede perdida.") | Out-Null
    }
} | Out-Null

Register-ObjectEvent -InputObject ([Microsoft.Win32.SystemEvents]) -EventName PowerModeChanged -SourceIdentifier "SkynetPowerChange" -Action {
    if ($Event.SourceEventArgs.Mode -eq "StatusChange") {
        $S.SpeakAsync("Estado de energia do Windows alterado.") | Out-Null
    }
} | Out-Null

while ($true) { Start-Sleep 30 }
