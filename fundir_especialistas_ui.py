import pathlib, subprocess

py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
py_code = py_p.read_text(encoding="utf-8")
if "especialista:" not in py_code:
    py_code = py_code.replace('"plano:",', '"plano:", "especialista:", "ler-tudo:", "investigar:",')
    py_p.write_text(py_code, encoding="utf-8")
    print("[OK] Gatilhos de especializacao liberados no /api/chat!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[CONCLUIDO] Servidor Web 5000 atualizado! Pressione Ctrl+F5 no navegador.")
