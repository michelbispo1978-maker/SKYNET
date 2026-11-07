import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

if "gerar-relatorio" not in code:
    code = code.replace("vigiar-tela", "vigiar-tela|gerar-relatorio")
    bloco = '''        "^gerar-relatorio" {
            $ArqCsv = "$env:USERPROFILE\\Desktop\\Relatorio_SKYNET_$(Get-Date -Format 'yyyyMMdd_HHmm').csv"
            $Logs = Get-ChildItem "C:\\SkynetPowerShell\\database\\*.json" -ErrorAction SilentlyContinue | Select-Object -First 50
            $Linhas = @("Data;Tipo;Descricao")
            foreach ($F in $Logs) {
                try {
                    $J = Get-Content $F.FullName -Raw | ConvertFrom-Json
                    if ($J.data) { $Linhas += "$($J.data);$($J.tipo);$($J.entrada -replace ';', ',')" }
                } catch {}
            }
            $Linhas | Set-Content -Path $ArqCsv -Encoding UTF8
            $Synthesizer.SpeakAsync("Relatorio exportado para a Area de Trabalho.") | Out-Null
            return "Relatorio CSV salvo com $($Linhas.Count - 1) eventos em: $ArqCsv"
        }
        "^vigiar-tela" {'''
    code = code.replace('        "^vigiar-tela" {', bloco, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[OK] skynet_core.ps1 atualizado!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor reiniciado com sucesso!")
