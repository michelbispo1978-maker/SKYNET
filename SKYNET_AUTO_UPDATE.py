import os, pathlib, psutil, requests, shutil, time, subprocess, sys
BASE=pathlib.Path(r"D:\SKYNET\Michelbds-7870")
def check_and_update():
    try:
        # Verifica se backend tá rodando
        running=False
        for proc in psutil.process_iter(['name','cmdline']):
            try:
                if 'SKYNET_BACKEND_CORRIGIDO.py' in ' '.join(proc.info['cmdline'] or []):
                    running=True
                    break
            except: pass
        
        if not running:
            # Reinicia backend se caiu
            print("Backend caiu! Reiniciando...")
            subprocess.Popen([sys.executable+"w", str(BASE/"SKYNET_BACKEND_CORRIGIDO.py")], cwd=str(BASE))
            return "Reiniciado!"
        
        # Verifica porta 5000
        import socket
        s=socket.socket()
        s.settimeout(1)
        try:
            s.connect(("127.0.0.1",5000))
            s.close()
            return "ONLINE - Porta 5000 LISTENING"
        except:
            s.close()
            print("Porta 5000 OFFLINE! Reiniciando backend...")
            for proc in psutil.process_iter():
                try:
                    if 'python' in proc.name().lower():
                        for cmd in proc.cmdline():
                            if 'SKYNET' in cmd:
                                proc.kill()
                except: pass
            time.sleep(1)
            subprocess.Popen([sys.executable+"w", str(BASE/"SKYNET_BACKEND_CORRIGIDO.py")], cwd=str(BASE))
            return "Reiniciado - Porta 5000!"
    except Exception as e:
        return f"Erro auto-update: {e}"

if __name__=="__main__":
    while True:
        status=check_and_update()
        print(f"[{time.strftime('%H:%M:%S')}] Auto-update: {status}")
        time.sleep(30)
