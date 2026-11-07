import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

if "eventos-erro" not in code:
    code = code.replace("organizar-desktop", "organizar-desktop|eventos-erro|volume:|mudo|faxina-win11")
    bloco_novo = '''        "^eventos-erro$" {
            $Evs = Get-WinEvent -FilterHashtable @{ LogName = 'System','Application'; Level = 2 } -MaxEvents 6 -ErrorAction SilentlyContinue | ForEach-Object { "[$($_.TimeCreated.ToString('dd/MM HH:mm'))] ($($_.ProviderName)): $($_.Message -split '`n' | Select-Object -First 1)" }
            if (-not $Evs) { return "Nenhum erro critico recente registrado no Visualizador de Eventos do Windows 11." }
            $ResumoEv = $Evs -join "`n"
            $PayloadEv = @{ model = "skynet:final"; prompt = "Analise estes erros recentes do Windows 11 e diga de forma curta qual e a provavel causa e como resolver:`n$ResumoEv"; stream = $false } | ConvertTo-Json
            $RespEv = try { (Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $PayloadEv -ContentType "application/json" -TimeoutSec 60).response } catch { "IA offline no momento." }
            return "=== ULTIMOS ERROS DO WINDOWS 11 ===`n$ResumoEv`n`n=== DIAGNOSTICO IA ===`n$RespEv"
        }
        "^volume:\\s*(\\d+)" {
            $VolAlvo = [int]$Matches
            if ($VolAlvo -lt 0) { $VolAlvo = 0 }
            if ($VolAlvo -gt 100) { $VolAlvo = 100 }
            $Wsh = New-Object -ComObject WScript.Shell
            1..50 | ForEach-Object { $Wsh.SendKeys([char]174) }
            $Passos = [math]::Round($VolAlvo / 2)
            if ($Passos -gt 0) { 1..$Passos | ForEach-Object { $Wsh.SendKeys([char]175) } }
            return "Volume do Windows 11 ajustado para aproximadamente $VolAlvo%."
        }
        "^mudo$" {
            $Wsh = New-Object -ComObject WScript.Shell
            $Wsh.SendKeys([char]173)
            return "Audio do Windows 11 alternado (Mudo/Ativo)."
        }
        "^faxina-win11$" {
            $Antes = [math]::Round((Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace / 1GB, 2)
            Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
            Remove-Item "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
            Clear-RecycleBin -Force -ErrorAction SilentlyContinue
            $Depois = [math]::Round((Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace / 1GB, 2)
            $Ganho = [math]::Round($Depois - $Antes, 2)
            Falar-Skynet("Faxina profunda concluida no Windows 11.")
            return "=== FAXINA PROFUNDA WINDOWS 11 ===`nEspaco livre antes: $Antes GB`nEspaco livre agora: $Depois GB`nRecuperado: $Ganho GB"
        }
        "^organizar-desktop$" {'''
    code = code.replace('        "^organizar-desktop$" {', bloco_novo, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[1/3] Eventos, Volume, Mudo e Faxina Win 11 instalados no Core 8080!")

# Libera gatilhos no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"eventos-erro"' not in p_txt:
        py_p.write_text(p_txt.replace('"organizar-desktop",', '"organizar-desktop", "eventos-erro", "volume:", "mudo", "faxina-win11",'), encoding="utf-8")
        print("[2/3] Gatilhos liberados no chat principal (/api/chat)!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[3/3] Motores reiniciados e Interface 66827 preservada!")
