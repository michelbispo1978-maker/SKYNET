Add-Type @"
using System;
using System.Runtime.InteropServices;
public class MemGuard {
    [DllImport("psapi.dll")] public static extern bool EmptyWorkingSet(IntPtr hwProc);
}
"@

$UltimoAviso = (Get-Date).AddMinutes(-10)

while ($true) {
    try {
        $Os = Get-CimInstance Win32_OperatingSystem
        $RamPct = [math]::Round((($Os.TotalVisibleMemorySize - $Os.FreePhysicalMemory) / $Os.TotalVisibleMemorySize) * 100, 1)

        if ($RamPct -ge 80.0) {
            # 1. Descarrega modelo ocioso do Ollama caso esteja ocupando RAM
            try {
                $Loaded = Invoke-RestMethod -Uri "http://127.0.0" -TimeoutSec 3
                foreach ($m in $Loaded.models) {
                    $Unload = @{ model = $m.name; keep_alive = 0 } | ConvertTo-Json -Compress
                    Invoke-RestMethod -Uri "http://127.0.0" -Method Post -Body $Unload -ContentType "application/json" -TimeoutSec 5 | Out-Null
                }
            } catch {}

            # 2. Enxuga Working Set de processos não-críticos do sistema
            Get-Process | Where-Object { $_.WorkingSet64 -gt 40MB -and $_.ProcessName -notin @("System","Idle","svchost","csrss","lsass","wininit","dwm","explorer","python","powershell") } | ForEach-Object {
                try { [void][MemGuard]::EmptyWorkingSet($_.Handle) } catch {}
            }
            [System.GC]::Collect()

            # 3. Avisa por voz no máximo uma vez a cada 5 minutos para não incomodar
            if (((Get-Date) - $UltimoAviso).TotalMinutes -ge 5) {
                $UltimoAviso = Get-Date
                Add-Type -AssemblyName System.Speech
                $S = New-Object System.Speech.Synthesis.SpeechSynthesizer
                $S.SpeakAsync("Teto de oitenta por cento atingido. Memoria RAM otimizada automaticamente.") | Out-Null
            }
        }
    } catch {}
    Start-Sleep -Seconds 8
}
