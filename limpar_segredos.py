import pathlib, re, json, subprocess

pasta_ps = pathlib.Path(r"C:\SkynetPowerShell")
pasta_git = pathlib.Path(r"C:\SkynetPowerShell\git_sync")
secrets_file = pasta_ps / "secrets.json"

# 1. Cria estrutura do cofre local caso nao exista
dados_secretos = {"TELEGRAM_BOT_TOKEN": "COLE_SEU_NOVO_TOKEN_AQUI", "TELEGRAM_CHAT_ID": "COLE_SEU_CHAT_ID_AQUI"}
if secrets_file.exists():
    try:
        dados_secretos.update(json.loads(secrets_file.read_text(encoding="utf-8")))
    except Exception:
        pass

# 2. Higieniza skynet_telegram.ps1 e quaisquer scripts .ps1/.py/.html
padrao_tg = re.compile(r'\b\d{8,11}:[A-Za-z0-9_-]{30,50}\b')
padrao_gh = re.compile(r'\bghp_[A-Za-z0-9]{20,50}\b')

for base_dir in [pasta_ps, pasta_git, pathlib.Path(r"D:\SKYNET\Michelbds-7870")]:
    if not base_dir.exists():
        continue
    for arq in base_dir.rglob("*"):
        if arq.is_file() and arq.suffix.lower() in {".ps1", ".py", ".html", ".json", ".txt", ".bat"} and arq.name != "secrets.json":
            txt = arq.read_text(encoding="utf-8", errors="ignore")
            m_tg = padrao_tg.search(txt)
            if m_tg and dados_secretos["TELEGRAM_BOT_TOKEN"] == "COLE_SEU_NOVO_TOKEN_AQUI":
                dados_secretos["TELEGRAM_BOT_TOKEN"] = m_tg.group(0)
            novo_txt = padrao_tg.sub('$((Get-Content "C:\\SkynetPowerShell\\secrets.json" -Raw | ConvertFrom-Json).TELEGRAM_BOT_TOKEN)', txt)
            novo_txt = padrao_gh.sub('TOKEN_REMOVIDO_USE_CREDENTIAL_MANAGER', novo_txt)
            if novo_txt != txt:
                arq.write_text(novo_txt, encoding="utf-8")
                print(f"[LIMPO] Segredo removido de: {arq}")

secrets_file.write_text(json.dumps(dados_secretos, indent=2), encoding="utf-8")
print(f"[COFRE] Credenciais isoladas em: {secrets_file}")

# 3. Cria .gitignore blindado na pasta git_sync
if pasta_git.exists():
    gi = pasta_git / ".gitignore"
    gi.write_text("secrets.json\n*.env\n*.key\n*.log\n", encoding="utf-8")
    print("[OK] .gitignore blindado criado!")
