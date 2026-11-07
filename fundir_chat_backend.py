import pathlib, subprocess

py_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py")
code = py_p.read_text(encoding="utf-8")

gatilhos = '''    # --- FUSÃO NATIVA: Roteia comandos de hardware, visão, voz e automação para o Robô 8080 ---
    prefixos_robo = (
        "raio-x", "saude-ssd", "limpar-ram", "otimizar-windows", "destravar-pc",
        "servicos", "reiniciar-servico:", "sirene", "bip", "ver-tela", "vigiar-tela",
        "pesquisar:", "resumir-url:", "achar-arquivo", "ler-doc", "ler-area",
        "lembrar:", "consultar-memoria", "agendar:", "digitar:", "criar-script:",
        "executar-python:", "modo-trabalho", "modo-foco", "midia-play", "midia-next",
        "vol-up", "vol-down", "vol-mute", "minimizar-tudo", "desligar-monitor",
        "bloquear-tela", "suspender-pc", "relatorio-geral", "gerar-relatorio",
        "sincronizar-github", "reiniciar-colmeia", "traduzir:", "gerar-senha",
        "energia", "ajuda", "scan-rede", "iot-", "abrir-"
    )
    if any(msg.strip().startswith(p) for p in prefixos_robo):
        try:
            import urllib.request, json as _json
            payload_robo = _json.dumps({"entrada": msg_original.strip()}).encode("utf-8")
            req_robo = urllib.request.Request(
                "http://localhost:8080/command",
                data=payload_robo,
                headers={"Content-Type": "application/json", "Authorization": "Bearer SKYNET-66827-FUSAO-TOTAL"},
                method="POST"
            )
            with urllib.request.urlopen(req_robo, timeout=90) as r_robo:
                res_j = _json.loads(r_robo.read().decode("utf-8", errors="ignore"))
            saida = res_j.get("resultado") or res_j.get("erro") or str(res_j)
            return jsonify({"ok": True, "autenticado": True, "response": saida, "model": "SKYNET-CORE-8080"})
        except Exception as e_robo:
            return jsonify({"ok": True, "autenticado": True, "response": f"Erro ao acionar Robo 8080: {e_robo}"})

    elif "arquivos" in msg:'''

if "FUSÃO NATIVA: Roteia comandos" not in code:
    code = code.replace('    elif "arquivos" in msg:', gatilhos, 1)
    py_p.write_text(code, encoding="utf-8")
    print("[OK] Backend /api/chat unificado com o Robo 8080!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetWeb5000Imortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetWeb5000Imortal'"])
print("[CONCLUIDO] Servidor Web 5000 reiniciado com fusao nativa!")
