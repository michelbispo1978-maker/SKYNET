import pathlib, subprocess

py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
py_code = py_p.read_text(encoding="utf-8")
if "janela-ativa" not in py_code:
    py_code = py_code.replace('"investigar:",', '"investigar:", "janela-ativa", "focar:", "nova-area", "desktop-esq", "desktop-dir", "modo-turbo",')
    py_p.write_text(py_code, encoding="utf-8")
    print("[OK] Gatilhos Windows 11 liberados no /api/chat!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[CONCLUIDO] Servidor Web 5000 atualizado! Interface 66827 mantida intacta.")
