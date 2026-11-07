p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = "urllib.request.urlopen(_url, timeout=5)"
new = "urllib.request.urlopen(urllib.request.Request(_url, headers={'User-Agent': 'SKYNET/1.0 (Windows 11; Python)'}), timeout=5)"
if old in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH USER-AGENT OK')
else:
    print('NAO ACHOU URLOPEN')
    # tenta achar a outra forma
    import re
    m = re.search(r"urllib\.request\.urlopen[^\n]*", t)
    print(m.group(0)[:200] if m else 'NENHUM')
