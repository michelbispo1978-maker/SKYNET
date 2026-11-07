# Skynet Guardião Autônomo v2.0 - Vigilância e Auto-Cura 24/7
$DbDir = "C:\SkynetPowerShell\database"
Add-Type -AssemblyName System.Speech
$Voz = New-Object System.Speech.Synthesis.SpeechSynthesizer

function Registrar-Evento ($Tipo, $Msg) {
    try {
        $Id = (Get-Date).Ticks
        $Payload = @{ id = $Id; data = (Get-Date -Format "yyyy-MM-dd HH:mm:ss"); tipo = $Tipo; entrada = $Msg } | ConvertTo-Json
        Set-Content -Path (Join-Path $DbDir "auto_$Id.json") -Value $Payload -Encoding UTF8
    } catch {}
}

$Voz.SpeakAsync("Módulo de autonomia inteligente ativado. Vigilância contínua iniciada.") | Out-Null
Registrar-Evento "Autonomia" "Guardião 24/7 iniciado com sucesso."

while ($true) {
    try {
        # 1. Verifica consumo de RAM e otimiza automaticamente se passar de 82%
        $OS = Get-CimInstance Win32_OperatingSystem
        $RamUso = [math]::Round((($OS.TotalVisibleMemorySize - $OS.FreePhysicalMemory) / $OS.TotalVisibleMemorySize) * 100, 1)
        if ($RamUso -gt 82) {
            [System.GC]::Collect()
            Get-Process | Where-Object { $_.WorkingSet64 -gt 180MB -and $_.ProcessName -notmatch "python|ollama|powershell|System" } | ForEach-Object { try { $_.MinWorkingSet = 1MB } catch {} }
            Registrar-Evento "Auto-RAM" "Memória em $RamUso% detectada. Otimização preventiva executada."
        }

        # 2. Vigia a Porta 8080 (Robô Core)
        try { Invoke-RestMethod -Uri "http://localhost:8080/status" -TimeoutSec 3 | Out-Null }
        catch {
            Start-ScheduledTask -TaskName "SkynetCoreImortal" -ErrorAction SilentlyContinue
            $Voz.SpeakAsync("Alerta: motor principal reiniciado automaticamente.") | Out-Null
            Registrar-Evento "Auto-Cura" "Porta 8080 offline. Tarefa SkynetCoreImortal reativada."
        }

        # 3. Vigia a Porta 5000 (Interface Web)
        try { Invoke-WebRequest -Uri "http://localhost:5000/" -UseBasicParsing -TimeoutSec 3 | Out-Null }
        catch {
            Start-ScheduledTask -TaskName "SkynetWeb5000Imortal" -ErrorAction SilentlyContinue
            Registrar-Evento "Auto-Cura" "Porta 5000 offline. Servidor Web reativado."
        }
            # 5. Verifica lembretes agendados por voz no agenda_voz.json
        $AgendaFile = "C:\SkynetPowerShell\database\agenda_voz.json"
        if (Test-Path $AgendaFile) {
            $HoraAtual = Get-Date -Format "HH:mm"
            $Itens = @(Get-Content $AgendaFile -Raw | ConvertFrom-Json)
            $Alterou = $false
            foreach ($Item in $Itens) {
                if (-not $Item.disparado -and $Item.hora -eq $HoraAtual) {
                    $Item.disparado = $true
                    $Alterou = $true
                    $Voz.SpeakAsync("Lembrete agendado: $($Item.texto)") | Out-Null
                    Registrar-Evento "Agenda-Voz" "Alerta disparado às ${HoraAtual}: $($Item.texto)"
                }
            }
            if ($Alterou) { $Itens | ConvertTo-Json | Set-Content -Path $AgendaFile -Encoding UTF8 }
        }
            # 7. Sentinela Visual Proativo (a cada 15 minutos)
        if ($null -eq $global:CicloVisual) { $global:CicloVisual = 0 }
        $global:CicloVisual++
        if ($global:CicloVisual -ge 30) {
            $global:CicloVisual = 0
            try {
                $Headers = @{ "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL"; "Content-Type" = "application/json" }
                $BodyVig = @{ entrada = "vigiar-tela" } | ConvertTo-Json
                $ResVig = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $Headers -Body $BodyVig -TimeoutSec 90
                if ($ResVig.resultado -and $ResVig.resultado -notmatch "normal e operacional") {
                    Registrar-Evento "Sentinela-Visual" $ResVig.resultado
                }
            } catch {}
        }
    } catch {}
    Start-Sleep -Seconds 30
}



