import pathlib
p = pathlib.Path("SKYNET-BACKEND-CORRIGIDO-V2.py")
txt = p.read_text(encoding="utf-8", errors="ignore")
txt = txt.replace(
    'elif msg in ["skynet-status", "status", "skynet"]:',
    'elif msg in ["skynet-status", "status", "skynet", "status local"]:'
)
txt = txt.replace(
    'elif "skynet-status" in q or q.strip() == "status":',
    'elif "skynet-status" in q or "status local" in q or q.strip() == "status":'
)
p.write_text(txt, encoding="utf-8")
print("Fix aplicado")
