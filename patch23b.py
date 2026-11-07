p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = 'return jsonify({"ok": True, "port": 5000, "autenticado": True, "memoria": vm.percent, "mode": "local", "core_editavel": True, "response": f"ONLINE 5000 Memoria {vm.percent}%"})'
new = """ollama_on = False
    try:
        import urllib.request
        req = urllib.request.Request('http://127.0.0.1:11434/api/tags', headers={'User-Agent': 'SKYNET/1.0'})
        with urllib.request.urlopen(req, timeout=2) as rr:
            ollama_on = (rr.status == 200)
    except:
        ollama_on = False
    return jsonify({"ok": True, "port": 5000, "autenticado": True, "memoria": vm.percent, "mode": "local", "core_editavel": True, "ollama_local": ollama_on, "ollama": ollama_on, "response": f"ONLINE 5000 Memoria {vm.percent}%"})"""
if old in t:
    t = t.replace(old, new, 1)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH STATUS OLLAMA OK - SO ADICIONOU ollama_local')
else:
    print('NAO ACHOU RETURN STATUS')
    # mostra como ta a linha pra debug
    import re
    for line in t.splitlines():
        if '/api/status' in line or 'ONLINE 5000' in line:
            print(repr(line))
