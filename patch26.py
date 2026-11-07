p = 'Index.html'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '<input id="skynet-voice-auto" type="checkbox">'
new = '<input id="skynet-voice-auto" type="checkbox" checked>'
if old in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH VOZ AUTO OK - AGORA VEM MARCADO')
else:
    print('NAO ACHOU VOZ AUTO')
