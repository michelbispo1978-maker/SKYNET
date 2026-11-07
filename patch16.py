p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '    sources = [{"title": x.name, "url": "file:///" + str(x).replace(chr(92), "/")} for x in files]'
new = """    # WEB REAL via 【entity-Wikipedia¦canonical_name=Wikipédia】
    web_sources = []
    try:
        import urllib.request, urllib.parse, json as _json
        _url = "https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch=" + urllib.parse.quote(q) + "&format=json&srlimit=3"
        _raw = urllib.request.urlopen(_url, timeout=5).read().decode('utf-8', errors='ignore')
        _j = _json.loads(_raw)
        for _s in _j.get("query", {}).get("search", []):
            web_sources.append({"title": _s.get("title", ""), "url": "https://pt.wikipedia.org/wiki/" + urllib.parse.quote(_s.get("title", ""))})
    except Exception as _e:
        web_sources = []
    sources = web_sources + [{"title": x.name, "url": "file:///" + str(x).replace(chr(92), "/")} for x in files]"""
if old in t and 'WEB REAL via 【entity-Wikipedia¦canonical_name=Wikipédia】' not in t:
    t = t.replace(old, new)
    # Atualiza o stats web de 0 pra len(web_sources) e o report
    t = t.replace('"stats": {"web": 0,', '"stats": {"web": len(web_sources),')
    t = t.replace('WEB: 0 (offline local)', 'WEB: {len(web_sources)} (Wikipedia real)')
    # Se o report ainda usa len(files) pra total, deixa, o sources ja inclui web
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH WEB REAL OK')
else:
    print('JA TEM WEB OU NAO ACHOU')
