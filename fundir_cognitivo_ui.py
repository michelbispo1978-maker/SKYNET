import pathlib, subprocess

# 1. Libera os gatilhos no Backend Python /api/chat
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
py_code = py_p.read_text(encoding="utf-8")
if "analisar-tela:" not in py_code:
    py_code = py_code.replace('"historico",', '"historico", "analisar-tela:", "aprender-pasta:", "plano:",')
    py_p.write_text(py_code, encoding="utf-8")
    print("[OK] Gatilhos cognitivos liberados no /api/chat!")

# 2. Adiciona botao Analisar Tela no PC Manager da interface 66827
html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $false"])
html = html_p.read_text(encoding="utf-8")
if "analisar-tela:" not in html:
    html = html.replace(
        "['👁️ Ver Tela', 'ver-tela']",
        "['👁️ Ver Tela', 'ver-tela'], ['🧠 Analisar Tela', 'analisar-tela: resuma o que esta aberto na tela']"
    )
    html_p.write_text(html, encoding="utf-8")
    print("[OK] Botao Analisar Tela adicionado ao PC Manager!")

subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[CONCLUIDO] Servidor Web 5000 reiniciado! Pressione Ctrl+F5 no navegador.")
