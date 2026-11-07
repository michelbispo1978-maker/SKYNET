p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '        resp = f"Pronto. Memoria {vm.percent}% | Interface 66827 | Digite se reintegra, skynet-status ou skynet-revisao"'
new = '        resp = f""'
if old in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH SEM MSG OK - AGORA FICA QUIETO')
else:
    print('NAO ACHOU PRONTO')
