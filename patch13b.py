p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
old = "frResults.textContent='🔍 Pesquisando"
new = "frResults.textContent=''; frSources.innerHTML=''; frResults.scrollTop=0; frSources.scrollTop=0; frResults.textContent='🔍 Pesquisando"
if old in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH LIMPA PESQUISA OK - AGORA LIMPA E ROLA')
else:
    print('NAO ACHOU DE NOVO')
