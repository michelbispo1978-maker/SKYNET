p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '    if "reintegra" in q:'
new = '''    # Comandos open_ na hibrida tambem abrem o app
    if q.strip().startswith("open_"):
        import subprocess, os
        mapa = {"open_notepad": ("notepad.exe", "Bloco de Notas aberto!"), "open_calculator": ("calc.exe", "Calculadora aberta!"), "open_task_manager": ("taskmgr.exe", "Gerenciador de Tarefas aberto!"), "open_explorer": ("explorer.exe", "Explorador de Arquivos aberto!"), "open_chrome": ("cmd /c start chrome", "Chrome/Edge aberto!"), "open_settings": ("ms-settings:", "Configuracoes abertas!")}
        task = q.strip()
        if task in mapa:
            cmd, msg = mapa[task]
            try:
                subprocess.Popen(cmd, shell=True)
                report = f"TAREFA: {task}\\nRESULTADO:\\n{msg} ✅"
            except Exception as e:
                report = f"TAREFA: {task}\\nERRO: {e}"
        else:
            report = f"TAREFA: {task}\\nRESULTADO: Comando nao mapeado"
        return jsonify({"ok": True, "report": report, "sources": [], "stats": {"web": 0, "files": 0, "memory": 0, "total": 0}})
    if "reintegra" in q:'''
if old in t and 'Comandos open_ na hibrida' not in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH HIBRIDA OPEN OK')
else:
    print('JA TEM OPEN OU NAO ACHOU')
