import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

if "sirene" not in code:
    code = code.replace("vigiar-tela", "vigiar-tela|sirene|bip|servicos|reiniciar-servico:")
    bloco = '''        "^sirene" {
            1..3 | ForEach-Object { [Console]::Beep(900, 250); [Console]::Beep(1400, 250) }
            $Synthesizer.SpeakAsync("Alerta sonoro ativado.") | Out-Null
            return "Sirene de alerta disparada com sucesso."
        }
        "^bip" {
            [Console]::Beep(1200, 300)
            return "Sinal sonoro emitido."
        }
        "^servicos" {
            $Lista = Get-Service -Name "WlanSvc","AudioSrv","mpssvc","WinDefend","Spooler" -ErrorAction SilentlyContinue | ForEach-Object { "$($_.Name): $($_.Status)" }
            return "Status de Servicos Criticos:`n" + ($Lista -join "`n")
        }
        "^reiniciar-servico:\\s*(.+)" {
            $NomeSvc = $Matches[1].Trim()
            Restart-Service -Name $NomeSvc -Force -ErrorAction Stop
            $Synthesizer.SpeakAsync("Servico $NomeSvc reiniciado.") | Out-Null
            return "Servico '$NomeSvc' reiniciado com sucesso."
        }
        "^vigiar-tela" {'''
    code = code.replace('        "^vigiar-tela" {', bloco, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[OK] Sirene e Gerenciador de Servicos instalados!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core reiniciado com alertas sonoros e controle de servicos!")
