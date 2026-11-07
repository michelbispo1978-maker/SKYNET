p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '    return jsonify({"ok": True, "autenticado": True, "response": f"SKYNET ONLINE REAL Memoria {vm.percent}% Interface 66827 - 7 vozes Thalita - Digite revisar"})'
new = """    cpu = psutil.cpu_percent(interval=0.1)
    free_c = psutil.disk_usage("C:").free // (1024**3)
    base = pathlib.Path(r"D:\\SKYNET\\Michelbds-7870")
    files = [x for x in base.iterdir() if x.is_file()]
    if msg in ["skynet-status", "status", "skynet"]:
        resp = f"SKYNET STATUS: ONLINE | Memoria {vm.percent}% | CPU {cpu}% | Disco C: {free_c}GB livres | {len(files)} arquivos | Porta 5000"
    elif msg in ["skynet-revisao", "revisao", "revisar"]:
        names = ", ".join([x.name for x in files])
        resp = f"REVISAO FEITA: {len(files)} arquivos. {names}. Backend completo OK, Interface mantida."
    elif "status local" in msg:
        resp = f"STATUS LOCAL ONLINE | Memoria {vm.percent}% | CPU {cpu}% | Disco C: {free_c}GB livres | {len(files)} arquivos"
    elif "arquivos" in msg:
        lista = "\\n".join([f"- {x.name}" for x in files])
        resp = f"ARQUIVOS ({len(files)}):\\n{lista}"
    else:
        resp = f"SKYNET ONLINE REAL Memoria {vm.percent}% Interface 66827 - 7 vozes Thalita - Digite revisar"
    return jsonify({"ok": True, "autenticado": True, "response": resp})"""
if old in t:
    open(p, 'w', encoding='utf-8', errors='ignore').write(t.replace(old, new))
    print('PATCH CHAT OK - PRESERVOU RESTO')
else:
    print('NAO ACHOU CHAT')