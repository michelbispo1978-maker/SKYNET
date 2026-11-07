import pathlib, subprocess

# 1. Atualiza os prefixos no Backend Python /api/chat
py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
py_code = py_p.read_text(encoding="utf-8")
if "velocidade-net" not in py_code:
    py_code = py_code.replace('"energia",', '"energia", "velocidade-net", "rede-wifi", "brilho:", "historico",')
    py_p.write_text(py_code, encoding="utf-8")
    print("[OK] Gatilhos liberados no /api/chat!")

# 2. Adiciona os botões no PC Manager da interface 66827
html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $false"])
html = html_p.read_text(encoding="utf-8")
if "velocidade-net" not in html:
    html = html.replace(
        "['❓ Ajuda', 'ajuda']",
        "['🌐 Internet', 'velocidade-net'], ['📡 Rede Wi-Fi', 'rede-wifi'], ['📜 Histórico', 'historico'], ['❓ Ajuda', 'ajuda']"
    )
    html_p.write_text(html, encoding="utf-8")
    print("[OK] Botoes adicionados no PC Manager!")

subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[CONCLUIDO] Servidor Web 5000 atualizado! Pressione Ctrl+F5 no navegador.")
