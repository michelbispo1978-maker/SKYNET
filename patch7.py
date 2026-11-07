p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
if '/api/memory/list' not in t:
    add = chr(10) + '@app.route("/api/memory/list", methods=["GET"])' + chr(10) + 'def memory_list():' + chr(10) + '    return jsonify({"ok": True, "memory": {}, "memories": []})' + chr(10)
    t = t.replace('if __name__ ==', add + chr(10) + 'if __name__ ==')
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH MEMORY ADD OK')
else:
    print('JA TEM')
