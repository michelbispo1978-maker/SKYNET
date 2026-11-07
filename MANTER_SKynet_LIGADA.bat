@echo off
cd /d D:\SKYNET\Michelbds-7870
:loop
echo [SKYNET] Subindo backend...
python SKYNET_BACKEND_CORRIGIDO.py
echo [SKYNET] Caiu! Reiniciando em 3s...
timeout /t 3 /nobreak >nul
goto loop