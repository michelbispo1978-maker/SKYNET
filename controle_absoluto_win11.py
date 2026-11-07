import pathlib, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

# 1. Adiciona comandos de controle administrativo total no skynet_core.ps1
if "matar-app:" not in code:
    code = code.replace("olhar-foto:", "olhar-foto:|matar-app:|servico:|ps-admin:|reiniciar-pc|desligar-pc")
    bloco_admin = '''        "^matar-app:\\s*(.+)" {
            $AlvoProc = $Matches.Trim() -replace '\.exe$', ''
            $Procs = Get-Process -Name "*$AlvoProc*" -ErrorAction SilentlyContinue
            if ($Procs) {
                $Count = $Procs.Count
                $Procs | Stop-Process -Force -ErrorAction SilentlyContinue
                Falar-Skynet("Processo $AlvoProc encerrado.")
                return "Controle Absoluto: $Count instancia(s) de '$AlvoProc' encerradas a forca."
            }
            return "Nenhum processo ativo encontrado com o nome '$AlvoProc'."
        }
        "^servico:\\s*(start|stop|restart)\\s+(.+)" {
            $AcaoSvc = $Matches.Trim().ToLower()
            $NomeSvc = $Matches.Trim()
            try {
                if ($AcaoSvc -eq "start") { Start-Service -Name $NomeSvc -ErrorAction Stop }
                elseif ($AcaoSvc -eq "stop") { Stop-Service -Name $NomeSvc -Force -ErrorAction Stop }
                elseif ($AcaoSvc -eq "restart") { Restart-Service -Name $NomeSvc -Force -ErrorAction Stop }
                Falar-Skynet("Servico $NomeSvc atualizado.")
                return "Servico '$NomeSvc' -> acao '$AcaoSvc' executada com privilegio administrativo."
            } catch {
                return "Erro ao gerenciar servico '$NomeSvc': $_"
            }
        }
        "^ps-admin:\\s*(.+)" {
            $ScriptAdmin = $Matches.Trim()
            try {
                $OutAdmin = Invoke-Expression $ScriptAdmin | Out-String
                if ([string]::IsNullOrWhiteSpace($OutAdmin)) { $OutAdmin = "Comando administrativo executado sem saida textual." }
                return "=== EXECUCAO ADMIN WINDOWS 11 ===`n$($OutAdmin.Trim())"
            } catch {
                return "Erro na execucao administrativa: $_"
            }
        }
        "^reiniciar-pc$" {
            Falar-Skynet("Reiniciando o Windows 11 em 5 segundos.")
            Start-Job -ScriptBlock { Start-Sleep 5; Restart-Computer -Force } | Out-Null
            return "Comando de reinicializacao do Windows 11 acionado (5 segundos)."
        }
        "^desligar-pc$" {
            Falar-Skynet("Desligando o Windows 11 em 5 segundos.")
            Start-Job -ScriptBlock { Start-Sleep 5; Stop-Computer -Force } | Out-Null
            return "Comando de desligamento do Windows 11 acionado (5 segundos)."
        }
        "^olhar-foto:\\s*(.+)" {'''
    code = code.replace('        "^olhar-foto:\\s*(.+)" {', bloco_admin, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[1/3] Comandos administrativos (matar-app, servico, ps-admin, energia) instalados!")

# 2. Libera novos gatilhos no /api/chat mantendo Index.html 66827 intacto
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
if py_p.exists():
    p_txt = py_p.read_text(encoding="utf-8")
    if '"matar-app:"' not in p_txt:
        py_p.write_text(p_txt.replace('"olhar-foto:",', '"olhar-foto:", "matar-app:", "servico:", "ps-admin:", "reiniciar-pc", "desligar-pc",'), encoding="utf-8")
        print("[2/3] Gatilhos administrativos liberados no chat principal (/api/chat)!")

# 3. Eleva privilégios das tarefas principais para RunLevel Highest (Administrador Total)
ps_elevate = '''
foreach ($tName in @("SkynetCoreImortal", "SkynetAutonomyImortal", "SkynetWeb5000Imortal", "SkynetUpdaterImortal")) {
    $Task = Get-ScheduledTask -TaskName $tName -ErrorAction SilentlyContinue
    if ($Task) {
        $Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
        Set-ScheduledTask -TaskName $tName -Principal $Principal | Out-Null
        Stop-ScheduledTask -TaskName $tName -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500
        Start-ScheduledTask -TaskName $tName -ErrorAction SilentlyContinue
    }
}
'''
subprocess.run(["powershell", "-NoProfile", "-Command", ps_elevate], check=True)
print("[3/3] Privilegios elevados para SYSTEM (RunLevel Highest) e motores reiniciados!")
