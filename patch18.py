p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
# 1. Adiciona a WEB REAL logo depois do files
old1 = '    sources = [{"title": x.name, "url": "file:///" + str(x).replace(chr(92), "/")} for x in files]'
new1 = """    web_sources = []
    try:
        import urllib.request, urllib.parse, json as _json
        _url = "https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch=" + urllib.parse.quote(q) + "&format=json&srlimit=3"
        _req = urllib.request.Request(_url, headers={'User-Agent': 'SKYNET/1.0 (Windows 11; Python)'})
        _raw = urllib.request.urlopen(_req, timeout=5).read().decode('utf-8', errors='ignore')
        _j = _json.loads(_raw)
        for _s in _j.get("query", {}).get("search", []):
            web_sources.append({"title": _s.get("title", ""), "url": "https://pt.wikipedia.org/wiki/" + urllib.parse.quote(_s.get("title", ""))})
    except Exception:
        web_sources = []
    sources = web_sources + [{"title": x.name, "url": "file:///" + str(x).replace(chr(92), "/")} for x in files]"""
if old1 in t:
    t = t.replace(old1, new1)
    print('PASSO 1 WEB OK')
else:
    print('NAO ACHOU SOURCES')
# 2. Report passa a mostrar WEB + LOCAL
old2 = 'report = f"PESQUISA HIBRIDA REAL: {q} - LOCAL: {len(files)} arquivos"'
new2 = 'report = f"PESQUISA HIBRIDA REAL: {q} - WEB: {len(web_sources)} (Wikipedia real) | LOCAL: {len(files)} arquivos\\n" + "\\n".join(["- WEB: " + s["title"] for s in web_sources] + ["- LOCAL: " + x.name for x in files])'
if old2 in t:
    t = t.replace(old2, new2)
    print('PASSO 2 REPORT OK')
else:
    print('NAO ACHOU REPORT')
# 3. Stats web passa de 0 pra len(web_sources) - so no return final, nao no open_
# O return final tem "report": report, o do open_ tem "report": report tambem, entao troca o ultimo
if '"stats": {"web": 0, "files": len(files)' in t:
    # Troca so a ultima ocorrencia
    idx = t.rfind('"stats": {"web": 0, "files": len(files)')
    t = t[:idx] + '"stats": {"web": len(web_sources), "files": len(files)' + t[idx+len('"stats": {"web": 0, "files": len(files)'):]
    print('PASSO 3 STATS OK')
open(p, 'w', encoding='utf-8', errors='ignore').write(t)
print('PATCH WEB COMPLETO FEITO')
