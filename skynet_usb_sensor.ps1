Register-WmiEvent -Class Win32_VolumeChangeEvent -SourceIdentifier "SkynetUsbEvent" -Action {
    if ($Event.SourceEventArgs.NewEvent.EventType -eq 2) {
        $Drive = $Event.SourceEventArgs.NewEvent.DriveName
        $Disco = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$Drive'" -ErrorAction SilentlyContinue
        $LivreGB = if ($Disco) { [math]::Round($Disco.FreeSpace / 1GB, 1) } else { "?" }
        $Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
        Add-Type -AssemblyName System.Speech
        $S = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $S.SpeakAsync("Dispositivo externo conectado na unidade $Drive com $LivreGB gigabytes livres.") | Out-Null
    }
} | Out-Null
while ($true) { Start-Sleep 30 }
