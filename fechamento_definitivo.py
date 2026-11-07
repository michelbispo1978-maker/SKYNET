import pathlib, re, shutil, subprocess

ps_dir = pathlib.Path(r"C:\SkynetPowerShell")

# 1. Limpa pasta temp para liberar espaço em disco
temp_dir = ps_dir / "temp"
if temp_dir.exists():
    for item in temp_dir.iterdir():
        try:
            if item.is_file(): item.unlink()
            elif item.is_dir(): shutil.rmtree(item)
        except Exception:
            pass
print("[1/4] Arquivos temporarios limpos!")

# 2. Atualiza o catalogo 'ajuda' com todos os comandos da Plataforma Windows 11
core_p = ps_dir / "skynet_core.ps1"
code = core_p.read_text(encoding="utf-8-sig")

catalogo_final = '''        "^ajuda$" {
            $Catalogo = @"
=== PLATAFORMA UNIFICADA WINDOWS 11 + SKYNET ===

[NUCLEO WINDOWS 11 & UI AUTOMATION]
- janela-ativa | focar: [app] -> Identifica ou traz qualquer janela para frente
- clicar-texto: [botao] | digitar-na-tela: [texto] -> Clica e digita em programas
- modo-turbo | rotina: dev | rotina: encerrar -> Desempenho e macros completas
- dispositivos | abrir: [app/config] -> Bluetooth, audio e paineis do Win 11
- nova-area | desktop-esq | desktop-dir -> Areas de trabalho virtuais
- analisar-copia -> Analisa/traduz o conteudo atual do Ctrl+C

[INTELIGENCIA COGNITIVA & ESPECIALISTAS]
- especialista: [codigo|juridico|saude|financas|professor] | [pergunta]
- analisar-tela: [pergunta] -> OCR nativo do monitor + analise da IA
- ler-tudo: [arquivo] | aprender-pasta: [pasta] -> Le PDF/DOCX/TXT e indexa (RAG)
- plano: [objetivo] -> Executa cadeia autonoma de comandos
- investigar: [tema] | pesquisar: [termo] | resumir-url: [link]

[MEMORIA, REDE & SEGURANCA]
- lembrar: [fato] | consultar-memoria | historico
- velocidade-net | rede-wifi | raio-x | saude-ssd | energia | brilho: [0-100]
- gerar-senha | limpar-ram | otimizar-windows | destravar-pc | sirene
- sincronizar-github | reiniciar-colmeia | gerar-relatorio

[ATALHOS GLOBAIS DO SISTEMA]
- Terminal/Win+R: skynet [comando] ou skynet://[comando]
- Qualquer tela: Ctrl + Alt + S | Explorer: Botao direito > Analisar com SKYNET
- Bandeja do Windows (relogio): Icone de Escudo SKYNET | Celular: @skynet_v4_michel_bot
"@
            return $Catalogo
        }'''

if '"^ajuda$"' in code:
    code = re.sub(r'        "\^ajuda\$"\s*\{.*?^\s*\}', catalogo_final, code, count=1, flags=re.S | re.M)
    core_p.write_text(code, encoding="utf-8")
print("[2/4] Catalogo 'ajuda' consolidado com todos os comandos Windows 11!")

# 3. Reinicia o Motor Core e garante proteção ReadOnly da Interface 66827
html_p = pathlib.Path(r"D:\SKYNET\Michelbds-7870\Index.html")
if html_p.exists():
    subprocess.run(["powershell", "-Command", f"Set-ItemProperty '{html_p}' -Name IsReadOnly -Value $true"])

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[3/4] Motor Core 8080 reiniciado e Interface 66827 blindada!")

# 4. Executa o backup final blindado no GitHub
backup_script = ps_dir / "backup_final_seguro.py"
if backup_script.exists():
    print("[4/4] Sincronizando versao definitiva com o GitHub...")
    subprocess.run([r"C:\Users\Administrador\AppData\Local\Programs\Python\Python313\python.exe", str(backup_script)])
