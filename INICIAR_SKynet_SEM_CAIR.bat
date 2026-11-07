@echo off
cd /d D:\SKYNET\Michelbds-7870
taskkill /F /IM python.exe
timeout /t 1 /nobreak >nul
start "" /min pythonw SKYNET_BACKEND_CORRIGIDO.py
timeout /t 3 /nobreak >nul
echo SKYNET rodando em segundo plano, sem cair!
echo Abra http://127.0.0.1:5000 no Chrome
pause