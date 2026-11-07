import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

if "executar-python:" not in code:
    code = code.replace("vigiar-tela", "vigiar-tela|executar-python:")
    bloco = '''        "^executar-python:\\s*(.+)" {
            \$PedidoPy = \(Matches[1].Trim()\)SandboxDir = "C:\\SkynetPowerShell\\sandbox"
            if (-not (Test-Path \$SandboxDir)) { New-Item -ItemType Directory -Path \(SandboxDir -Force \vert{} Out-Null }\)Payload = @{ model = "skynet:final"; prompt = "Escreva APENAS um codigo Python 3 funcional que imprima (print) o resultado final, sem blocos markdown, para: \$PedidoPy"; stream = \(false } \vert{} ConvertTo-Json\)RespPy = Invoke-RestMethod -Uri OllamaUri -Method Post -Body Payload -ContentType "application/json" -TimeoutSec 60
            CodigoLimpo = (RespPy.response -replace '```python|```', '').Trim()
            $ScriptPy = Join-Path $SandboxDir "run_sandbox.py"
            Set-Content -Path $ScriptPy -Value $CodigoLimpo -Encoding UTF8
            $PyExe = "C:\\Users\\Administrador\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
            $SaidaPy = (& $PyExe $ScriptPy 2>&1 | Out-String).Trim()
            $Synthesizer.SpeakAsync("Execucao Python concluida.") | Out-Null
            return "Python Sandbox:`n$SaidaPy`n---`nCodigo gerado:`n$CodigoLimpo"
        }
        "^vigiar-tela" {'''
    code = code.replace('        "^vigiar-tela" {', bloco, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[OK] Co-Piloto Python Sandbox instalado!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core reiniciado com Python Sandbox ativo!")
