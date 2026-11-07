p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '        else:\n            result = f"{task} OK"'
new = "        elif task in ['memory', 'memoria', 'ram']:\n            vm = psutil.virtual_memory()\n            result = f'MEMORIA RAM - Total: {vm.total//1024//1024} MB | Usado: {vm.used//1024//1024} MB ({vm.percent}%) | Livre: {vm.available//1024//1024} MB'\n        elif task in ['network', 'rede']:\n            import socket\n            hn = socket.gethostname()\n            ip = socket.gethostbyname(hn)\n            result = f'REDE LOCAL - Host: {hn} | IP: {ip} | Interfaces: {len(psutil.net_if_addrs())}'\n        elif task in ['processes', 'processos']:\n            result = f'PROCESSOS - {len(list(psutil.process_iter()))} processos rodando'\n        elif task in ['disks', 'discos', 'disk']:\n            txt = ''\n            for part in psutil.disk_partitions():\n                try:\n                    u = psutil.disk_usage(part.mountpoint)\n                    txt += f'- {part.device} {u.percent}% usado\\n'\n                except: pass\n            result = f'DISCOS E VOLUMES:\\n{txt}'\n        elif task in ['info', 'windows', 'informacoes']:\n            import platform\n            result = f'WINDOWS - {platform.system()} {platform.release()} | Versao: {platform.version()} | Maquina: {platform.machine()}'\n        else:\n            result = f'{task} OK'"
if old in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH MEMORY + NETWORK INGLES OK')
else:
    print('NAO ACHOU ELSE')
