import os, stat, pathlib, re, subprocess

repo = pathlib.Path(r"C:\SkynetPowerShell\git_sync")
repo.mkdir(parents=True, exist_ok=True)

# 1. Garante .gitignore blindado contra vazamento de tokens e arquivos temporários
(repo / ".gitignore").write_text("secrets.json\n*.env\n*.key\n*.log\ntemp/\ndatabase/\n", encoding="utf-8")

# 2. Copia os arquivos principais do Motor Core e da Interface 66827 (sem secrets.json)
origens = [
    pathlib.Path(r"C:\SkynetPowerShell"),
    pathlib.Path(r"D:\SKYNET\Michelbds-7870")
]
exts_permitidas = {".ps1", ".py", ".html", ".json", ".bat", ".md"}
ignorados = {"secrets.json", "rag_index.json", "memoria_mestre.json"}

padrao_tg = re.compile(r'\b\d{8,11}:[A-Za-z0-9_-]{30,50}\b')
padrao_gh = re.compile(r'\bghp_[A-Za-z0-9]{20,50}\b')

for pasta in origens:
    if not pasta.exists():
        continue
    for arq in pasta.iterdir():
        if arq.is_file() and arq.suffix.lower() in exts_permitidas and arq.name not in ignorados:
            destino = repo / arq.name
            if destino.exists():
                os.chmod(destino, stat.S_IWRITE)
            txt = arq.read_text(encoding="utf-8", errors="ignore")
            txt = padrao_tg.sub("TOKEN_PROTEGIDO_NO_SECRETS_JSON", txt)
            txt = padrao_gh.sub("TOKEN_PROTEGIDO_NO_CREDENTIAL_MANAGER", txt)
            destino.write_text(txt, encoding="utf-8")

# 3. Executa commit limpo e push para o GitHub
cmds = [
    ["git", "-C", str(repo), "add", "-A"],
    ["git", "-C", str(repo), "commit", "-m", "SKYNET Fusao Total Windows + Telegram + Especialistas (Backup Seguro)"],
    ["git", "-C", str(repo), "push", "-u", "origin", "main", "-f"]
]
for c in cmds:
    res = subprocess.run(c, capture_output=True, text=True)
    if res.stdout: print(res.stdout.strip())
    if res.stderr: print(res.stderr.strip())
