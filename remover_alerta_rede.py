import pathlib, re, subprocess

auto_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_autonomia.ps1")
code = auto_p.read_text(encoding="utf-8")

# 1. Remove o Sentinela de Conexão Externa (Sentinela-Rede)
code = re.sub(r'\s*# 4\. Vigia conexão com a Internet.*?Registrar-Evento "Sentinela-Rede"[^\n]*\n\s*\}\n\s*\}', '', code, flags=re.S)

# 2. Remove o Sentinela de Intrusos Wi-Fi (Sentinela-WiFi)
code = re.sub(r'\s*# Sentinela de Intrusos Wi-Fi.*?Registrar-Evento "Sentinela-WiFi"[^\n]*\n\s*if \(-not \$ModoNoturno\) \{[^}]*\}\n\s*\}', '', code, flags=re.S)

auto_p.write_text(code, encoding="utf-8")
print("[OK] Alertas de rede removidos do skynet_autonomia.ps1!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetAutonomyImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetAutonomyImortal'"])
print("[CONCLUIDO] Guardiao Autonomo reiniciado sem alertas de rede!")
