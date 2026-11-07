import pathlib, psutil, subprocess, sys, time, platform
BASE=pathlib.Path(r"D:\SKYNET\Michelbds-7870")
while True:
    try:
        # Verifica se backend tá rodando
        running=False
        for proc in psutil.process_iter(['cmdline']):
            try:
                cmd=' '.join(proc.info['cmdline'] or [])
                if 'SKYNET_BACKEND_CORRIGIDO.py' in cmd:
                    running=True
                    break
            except: pass
        if not running:
            print("Backend caiu! Reiniciando...")
            subprocess.Popen([sys.executable+"w", str(BASE/"SKYNET_BACKEND_CORRIGIDO.py")], cwd=str(BASE))
        time.sleep(30)
    except:
        time.sleep(30)
