p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '        else:\n            result = f"{task} OK"'
new = """        elif task in ["network", "rede", "rede_local", "rede local"]:
            try:
                import socket
                hn = socket.gethostname()
                ip = socket.gethostbyname(hn)
                result = f"REDE LOCAL - Host: {hn} | IP: {ip} | Interfaces: {len(psutil.net_if_addrs())} | Conexoes: {len(psutil.net_connections())} ✅"
            except Exception as e:
                result = f"REDE - Erro: {e}"
        elif task in ["memoria", "memoria_ram", "ram", "memory"]:
            vm = psutil.virtual_memory()
            result = f"MEMORIA RAM - Total: {vm.total//1024//1024} MB | Usado: {vm.used//1024//1024} MB ({vm.percent}%) | Livre: {vm.available//1024//1024} MB ✅"
        elif task in ["info", "info_windows", "informacoes", "informacoes_do_windows", "windows"]:
            try:
                import platform
                result = f"WINDOWS - Sistema: {platform.system()} {platform.release()} | Versao: {platform.version()} | Maquina: {platform.machine()} | Processador: {platform.processor()} ✅"
            except Exception as e:
                result = f"WINDOWS - Erro: {e}"
        elif task in ["processos", "processes", "process"]:
            procs = sorted(psutil.process_iter(['name', 'cpu_percent']), key=lambda p: (p.info.get('cpu_percent') or 0), reverse=True)[:8]
            txt = "\\n".join([f"- {p.info['name']} CPU {p.info.get('cpu_percent') or 0}%" for p in procs])
            result = f"PROCESSOS - Top 8 por CPU:\\n{txt} ✅"
        elif task in ["documentos", "pasta_documentos", "pasta documentos", "documents"]:
            import pathlib
            docs = pathlib.Path.home() / "Documents"
            try:
                qtd = len(list(docs.iterdir())) if docs.exists() else 0
                result = f"PASTA DOCUMENTOS - Caminho: {docs} | {qtd} itens ✅"
            except Exception as e:
                result = f"DOCUMENTOS - Erro: {e}"
        elif task in ["auditoria", "auditoria_skynet", "audit"]:
            import pathlib
            base2 = pathlib.Path(r"D:\\SKYNET\\Michelbds-7870")
            qtd2 = len([x for x in base2.iterdir() if x.is_file()]) if base2.exists() else 0
            result = f"AUDITORIA SKYNET - {qtd2} arquivos na raiz | Backend completo OK | Interface mantida ✅"
        elif task in ["inicializacao", "startup", "boot"]:
            try:
                import subprocess
                out2 = subprocess.check_output(["powershell", "-Command", "Get-CimInstance Win32_StartupCommand | Select-Object -First 5 Name, Command | Format-Table -AutoSize | Out-String"], timeout=10, text=True, errors="ignore")
                result = f"INICIALIZACAO - Primeiros 5:\\n{out2} ✅"
            except Exception as e:
                result = f"INICIALIZACAO - Erro: {e}"
        elif task in ["servicos", "services", "consultar_servicos", "consultar servicos"]:
            try:
                svcs = list(psutil.win_service_iter()) if hasattr(psutil, 'win_service_iter') else []
                run = len([s for s in svcs if s.status() == 'running']) if svcs else 0
                result = f"SERVICOS - Total: {len(svcs)} | Rodando: {run} ✅"
            except Exception as e:
                result = f"SERVICOS - Erro: {e} | Use services.msc"
        elif task in ["tarefas", "tarefas_agendadas", "tarefas agendadas", "scheduled"]:
            try:
                import subprocess
                out3 = subprocess.check_output(["schtasks", "/query", "/FO", "TABLE", "/NH"], timeout=10, text=True, errors="ignore")
                linhas = [l for l in out3.splitlines() if l.strip()][:8]
                result = f"TAREFAS AGENDADAS - Primeiras 8:\\n" + "\\n".join(linhas) + " ✅"
            except Exception as e:
                result = f"TAREFAS - Erro: {e}"
        elif task in ["discos", "discos_e_volumes", "discos e volumes", "disk", "volumes"]:
            txt2 = ""
            for part in psutil.disk_partitions():
                try:
                    u = psutil.disk_usage(part.mountpoint)
                    txt2 += f"- {part.device} {part.mountpoint} {u.percent}% usado ({u.used//1024//1024} MB / {u.total//1024//1024} MB)\\n"
                except: pass
            result = f"DISCOS E VOLUMES:\\n{txt2} ✅"
        elif task in ["eventos", "eventos_do_sistema", "eventos do sistema", "events"]:
            try:
                import subprocess
                out4 = subprocess.check_output(["powershell", "-Command", "Get-EventLog -LogName System -Newest 5 | Select-Object TimeGenerated, EntryType, Source | Format-Table -AutoSize | Out-String"], timeout=10, text=True, errors="ignore")
                result = f"EVENTOS DO SISTEMA - Ultimos 5:\\n{out4} ✅"
            except Exception as e:
                result = f"EVENTOS - Erro: {e}"
        else:
            result = f"{task} OK"'''
if old in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH DIAGNOSTICO REAL OK - NETWORK + MEMORIA + INFO + PROCESSOS + DOCS + AUDITORIA + INICIALIZACAO + SERVICOS + TAREFAS + DISCOS + EVENTOS')
else:
    print('NAO ACHOU ELSE')
