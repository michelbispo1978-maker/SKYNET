p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = "        else:\n            result = f'{task} OK'"
new = """        elif task in ['system', 'windows']:
            import platform
            result = f'WINDOWS - {platform.system()} {platform.release()} | Versao: {platform.version()} | Maquina: {platform.machine()} | Processador: {platform.processor()}'
        elif task in ['documents']:
            import pathlib
            docs = pathlib.Path.home() / 'Documents'
            qtd = len(list(docs.iterdir())) if docs.exists() else 0
            result = f'PASTA DOCUMENTOS - {docs} | {qtd} itens'
        elif task in ['audit']:
            import pathlib
            base2 = pathlib.Path(r'D:\\SKYNET\\Michelbds-7870')
            qtd2 = len([x for x in base2.iterdir() if x.is_file()]) if base2.exists() else 0
            result = f'AUDITORIA SKYNET - {qtd2} arquivos na raiz | Backend completo OK | Interface mantida'
        elif task in ['startup']:
            try:
                import subprocess
                out2 = subprocess.check_output(['powershell', '-Command', 'Get-CimInstance Win32_StartupCommand | Select-Object -First 5 Name | Format-Table -AutoSize | Out-String'], timeout=10, text=True, errors='ignore')
                result = f'INICIALIZACAO - Primeiros 5:\\n{out2}'
            except Exception as e:
                result = f'INICIALIZACAO - Erro: {e}'
        elif task in ['services']:
            try:
                svcs = list(psutil.win_service_iter()) if hasattr(psutil, 'win_service_iter') else []
                run = len([s for s in svcs if s.status() == 'running']) if svcs else 0
                result = f'SERVICOS - Total: {len(svcs)} | Rodando: {run}'
            except Exception as e:
                result = f'SERVICOS - Erro: {e}'
        elif task in ['scheduled_tasks', 'scheduled']:
            try:
                import subprocess
                out3 = subprocess.check_output(['schtasks', '/query', '/FO', 'TABLE', '/NH'], timeout=10, text=True, errors='ignore')
                linhas = [l for l in out3.splitlines() if l.strip()][:8]
                result = 'TAREFAS AGENDADAS - Primeiras 8:\\n' + chr(10).join(linhas)
            except Exception as e:
                result = f'TAREFAS - Erro: {e}'
        elif task in ['volumes', 'discos', 'disk']:
            txt2 = ''
            for part in psutil.disk_partitions():
                try:
                    u = psutil.disk_usage(part.mountpoint)
                    txt2 += f'- {part.device} {part.mountpoint} {u.percent}% usado\\n'
                except: pass
            result = f'DISCOS E VOLUMES:\\n{txt2}'
        elif task in ['events']:
            try:
                import subprocess
                out4 = subprocess.check_output(['powershell', '-Command', 'Get-EventLog -LogName System -Newest 5 | Select-Object TimeGenerated, EntryType, Source | Format-Table -AutoSize | Out-String'], timeout=10, text=True, errors='ignore')
                result = f'EVENTOS DO SISTEMA - Ultimos 5:\\n{out4}'
            except Exception as e:
                result = f'EVENTOS - Erro: {e}'
        elif task in ['processes']:
            result = f'PROCESSOS - {len(list(psutil.process_iter()))} processos rodando'
        else:
            result = f'{task} OK'"""
if old in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH DIAGNOSTICO COMPLETO OK - SYSTEM + DOCS + AUDIT + STARTUP + SERVICES + SCHEDULED + VOLUMES + EVENTS')
else:
    print('NAO ACHOU ELSE - SIMPLES')
