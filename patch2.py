p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = 'if "taskmgr" in t or "gerenciador" in t:'
new = 'if "taskmgr" in t or "task_manager" in t or "task manager" in t or "gerenciador" in t or "open_task" in t:'
if old in t:
    open(p, 'w', encoding='utf-8', errors='ignore').write(t.replace(old, new))
    print('PATCH TASKMGR OK')
else:
    print('NAO ACHOU - JA TA ARRUMADO OU LINHA DIFERENTE')