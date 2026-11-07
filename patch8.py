p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
if '/api/research/run' not in t:
    add = chr(10) + '@app.route("/api/research/run", methods=["POST"])' + chr(10) + 'def research_run():' + chr(10) + '    data = request.get_json() or {}' + chr(10) + '    q = (data.get("query") or "").lower()' + chr(10) + '    import pathlib' + chr(10) + '    base = pathlib.Path(r"D:\\SKYNET\\Michelbds-7870")' + chr(10) + '    files = [x for x in base.iterdir() if x.is_file() and (not q or q in x.name.lower())]' + chr(10) + '    sources = [{"title": x.name, "url": "file:///" + str(x).replace(chr(92), "/")} for x in files]' + chr(10) + '    report = f"PESQUISA HIBRIDA REAL: {q} - LOCAL: {len(files)} arquivos"' + chr(10) + '    return jsonify({"ok": True, "report": report, "sources": sources, "stats": {"web": 0, "files": len(files), "memory": 0, "total": len(sources)}})' + chr(10)
    t = t.replace('if __name__ ==', add + chr(10) + 'if __name__ ==')
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH RESEARCH OK')
else:
    print('JA TEM RESEARCH')
