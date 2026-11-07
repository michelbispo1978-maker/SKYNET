p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
old = "  frResults.textContent='ðŸ” Pesquisando"
if old not in t:
    # tenta achar a linha do Pesquisando sem o emoji quebrado
    import re
    m = re.search(r"frResults\.textContent='[^']*Pesquisando[^\n]*", t)
    print('ACHEI LINHA:' if m else 'NAO ACHOU', m.group(0)[:120] if m else '')
else:
    new = "  frResults.textContent=''; frSources.innerHTML=''; frResults.scrollTop=0; frSources.scrollTop=0;\n  frResults.textContent='ðŸ” Pesquisando"
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH LIMPA PESQUISA OK')
