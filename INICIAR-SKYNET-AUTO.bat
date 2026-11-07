@echo off
start "Ollama SKYNET" /min cmd /c "ollama serve"
timeout /t 8 /nobreak >nul
cd /d D:\SKYNET\Michelbds-7870
start "SKYNET Backend" /min cmd /c "python SKYNET-BACKEND-CORRIGIDO-V2.py"
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5000
exit
