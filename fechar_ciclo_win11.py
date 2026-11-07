import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

if "dormir-em:" not in code:
    code = code.replace("reset-rede", "reset-rede|dormir-em:|cancelar-sono|nova-aba:|fechar-aba|reabrir-aba")
    bloco_final = r'''        "^dormir-em:\s*(\d+)" {
            $Mins = [int]$Matches
            $Segs = $Mins * 60
            shutdown.exe /s /t $Segs /c "SKYNET: Desligamento programado em $Mins minutos."
            Falar-Skynet("Desligamento automatico programado para $Mins minutos.")
            return "Windows 11 programado para desligar em $Mins minutos ($Segs segundos). Use 'cancelar-sono' para abortar."
        }
        "^cancelar-sono$" {
            shutdown.exe /a 2>$null
            Falar-Skynet("Desligamento automatico cancelado.")
            return "Agendamento de desligamento do Windows 11 cancelado."
        }
        "^nova-aba:\s*(.+)" {
            $AlvoUrl = $Matches.Trim()
            if ($AlvoUrl -notmatch '^https?://') {
                $AlvoUrl = "https://google.com" + [uri]::EscapeDataString($AlvoUrl)
            }
            Start-Process $AlvoUrl
            return "Abrindo no navegador: $AlvoUrl"
        }
        "^fechar-aba$" {
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.SendKeys]::SendWait("^w")
            return "Aba atual fechada (Ctrl+W)."
        }
        "^reabrir-aba$" {
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.SendKeys]::SendWait("^+t")
            return "Ultima aba fechada reaberta (Ctrl+Shift+T)."
        }
        "^reset-rede$" {'''
    code = code.replace('        "^reset-rede$" {', bloco_final, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[1/3] Controle de Energia Programada e Abas de Navegador instalados!")

# Libera gatilhos no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"dormir-em:"' not in p_txt:
        py_p.write_text(p_txt.replace('"reset-rede",', '"reset-rede", "dormir-em:", "cancelar-sono", "nova-aba:", "fechar-aba", "reabrir-aba",'), encoding="utf-8")
        print("[2/3] Gatilhos liberados no chat principal (/api/chat)!")

html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
if html_p.exists():
    subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[3/3] Motores reiniciados! Executando backup final no GitHub...")

backup_py = ps_dir / "backup_final_seguro.py"
if backup_py.exists():
    subprocess.run([r"C:\Users\Administrador\AppData\Local\Programs\Python\Python313\python.exe", str(backup_py)])
