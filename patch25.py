p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '        resp = f"SKYNET ONLINE REAL Memoria {vm.percent}% Interface 66827 - 7 vozes Thalita - Digite revisar"'
new = '        resp = f"Ola, como posso ajudar? Memoria {vm.percent}% | Interface 66827 | Digite se reintegra, skynet-status ou skynet-revisao"'
if old in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH OLA AJUDAR OK')
else:
    print('NAO ACHOU OLA')
    for line in t.splitlines():
        if 'SKYNET ONLINE REAL' in line:
            print(repr(line))
