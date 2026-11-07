p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
old = "if(mode==='security')"
new = """if(mode==='nuc'){ fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:'status local'})}).then(r=>r.json()).then(d=>addMsg('assistant',d.response||'Falha')); }
    if(mode==='files'){ fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:'arquivos'})}).then(r=>r.json()).then(d=>addMsg('assistant',d.response||'Falha')); }
    if(mode==='security')"""
if old in t:
    open(p, 'w', encoding='utf-8', errors='ignore').write(t.replace(old, new))
    print('PATCH OK')
else:
    print('JA TEM OU NAO ACHOU')