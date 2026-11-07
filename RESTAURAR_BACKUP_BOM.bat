@echo off
cd /d D:\SKYNET\Michelbds-7870
echo Restaurando SKYNET do backup bom...
taskkill /F /IM python.exe
copy /Y "BACKUP_2026-11-06_1215\SKYNET_BACKEND_CORRIGIDO.py" "SKYNET_BACKEND_CORRIGIDO.py"
copy /Y "BACKUP_2026-11-06_1215\Index.html" "Index.html"
echo.
echo RESTAURADO! Agora rode:
echo python SKYNET_BACKEND_CORRIGIDO.py
pause