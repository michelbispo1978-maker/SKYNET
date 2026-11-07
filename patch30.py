p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '        resp = f""'
new = '        resp = f"Olá"'
if old in t:
    t = t.replace(old, new, 1)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH OLA CURTO OK')
else:
    print('NAO ACHOU VAZIO')
