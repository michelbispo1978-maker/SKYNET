p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
# Só adiciona o campo "memories" que a interface espera, sem apagar o "memory" que já existe
old = 'return jsonify({"ok": True, "memory": MEMORY})'
new = 'return jsonify({"ok": True, "memory": MEMORY, "memories": [{"key": k, "value": v, "ts": ""} for k, v in MEMORY.items()]})'
if old in t:
    open(p, 'w', encoding='utf-8', errors='ignore').write(t.replace(old, new))
    print('PATCH MEMORY OK - PRESERVOU RESTO')
else:
    print('NAO ACHOU MEMORY - ME MANDA O TRECHO')