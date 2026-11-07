import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
ps_dir.mkdir(parents=True, exist_ok=True)

# 1. Configura limites rígidos de RAM para o Ollama no Windows 11 (máx 1 modelo e libera em 2 min)
ps_env = '''
[Environment]::SetEnvironmentVariable("OLLAMA_MAX_LOADED_MODELS", "1", "Machine")
[Environment]::SetEnvironmentVariable("OLLAMA_NUM_PARALLEL", "1", "Machine")
[Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "2m", "Machine")
'''
subprocess.run(["powershell", "-NoProfile", "-Command", ps_env], check=True)
print("[1/3] Limites de memoria do Ollama configurados (1 modelo por vez, Keep-Alive 2m)!")

# 2. Cria/Atualiza o Guardião Autônomo com trava rigorosa de 80% de RAM via API nativa psapi.dll
auto_ps = ps_dir / "skynet_autonomia.ps1"
auto_ps.write_text('''Add-Type @"
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
''', encoding="utf-8")

# 3. Reinicia a tarefa imortal SkynetAutonomyImortal com privilégio SYSTEM
ps_restart = '''
$Act = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\\SkynetPowerShell\\skynet_autonomia.ps1"
$Trig = New-ScheduledTaskTrigger -AtStartup
$Prin = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$Set = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Days 3650) -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask -TaskName "SkynetAutonomyImortal" -Action $Act -Trigger $Trig -Principal $Prin -Settings $Set -Force | Out-Null
Start-ScheduledTask -TaskName "SkynetAutonomyImortal"
'''
subprocess.run(["powershell", "-NoProfile", "-Command", ps_restart], check=True)
print("[2/3] Guardiao de Teto 80% de RAM ativo 24/7!")

# 4. Salva essa blindagem no GitHub automaticamente
backup_py = ps_dir / "backup_final_seguro.py"
if backup_py.exists():
    print("[3/3] Registrando atualizacao no GitHub...")
    subprocess.run([r"C:\Users\Administrador\AppData\Local\Programs\Python\Python313\python.exe", str(backup_py)])
