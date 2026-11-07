p = 'SKYNET_BACKEND_CORRIGIDO.py'
t = open(p, encoding='utf-8', errors='ignore').read()
old = '        else:\n            result = f"{task} OK"'
new = '''        elif task in ["updates", "update", "windows_update"]:
            try:
                import subprocess
                out = subprocess.check_output(["powershell", "-Command", "Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5 HotFixID, Description, InstalledOn | Format-Table -AutoSize | Out-String"], timeout=12, text=True, errors="ignore")
                result = f"UPDATES - Ultimos 5 HotFix instalados:\\n{out}\\nVerificado via Get-HotFix ✅"
            except Exception as e:
                result = f"UPDATES - Nao consegui ler Windows Update: {e}"
        else:
            result = f"{task} OK"'''
if old in t:
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8', errors='ignore').write(t)
    print('PATCH UPDATES REAL OK')
else:
    print('NAO ACHOU ELSE')
