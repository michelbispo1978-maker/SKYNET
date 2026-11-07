import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
linhas = core_p.read_text(encoding="utf-8-sig").splitlines()

# Remove chaves '}' órfãs no início do arquivo antes da primeira linha válida de código
while linhas and linhas[0].strip() in ("", "}", "};"):
    linhas.pop(0)

core_p.write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("[OK] Chaves orfas removidas do topo do skynet_core.ps1!")

# Reinicia a tarefa imortal do Motor Core 8080
subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado!")
