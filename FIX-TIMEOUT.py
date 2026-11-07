import pathlib
p = pathlib.Path("SKYNET-BACKEND-CORRIGIDO-V2.py")
txt = p.read_text(encoding="utf-8", errors="ignore")
txt = txt.replace("timeout=60", "timeout=180")
p.write_text(txt, encoding="utf-8")
print("Timeout 180s aplicado")
