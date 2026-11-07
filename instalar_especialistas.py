import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

if "especialista:" not in code:
    code = code.replace("plano:", "plano:|especialista:|ler-tudo:|investigar:")
    bloco = '''        "^especialista:\\s*([^|]+)\\|\\s*(.+)" {
            $Area = $Matches.Trim().ToLower()
            $PerguntaEsp = $Matches.Trim()
            $Perfis = @{
                "codigo"    = "Voce e um Engenheiro de Software Senior especialista em Python, PowerShell, Windows e Web. Entregue codigo limpo, funcional e direto ao ponto."
                "juridico"  = "Voce e um Consultor Juridico especialista em legislacao brasileira. Analise documentos, direitos e clausulas com precisao e linguagem clara."
                "saude"     = "Voce e um Assistente de Saude e Analise de Exames. Explique termos clinicos e resultados de forma didatica, lembrando sempre de consultar um medico."
                "financas"  = "Voce e um Estrategista Financeiro. Ajude com orcamento, calculo de juros, investimentos e organizacao financeira pratica."
                "professor" = "Voce e um Professor Particular especialista em didatica. Explique qualquer tema do zero, passo a passo, com exemplos do dia a dia."
            }
            $SystemPrompt = if ($Perfis.ContainsKey($Area)) { $Perfis[$Area] } else { "Voce e um especialista multidisciplinar de elite na area de $Area. Responda com profundidade e clareza." }
            Falar-Skynet("Ativando modo especialista em $Area.")
            $PromptFull = "INSTRUCAO DE ESPECIALIDADE: $SystemPrompt`n`nSOLICITACAO DO USUARIO: $PerguntaEsp"
            $Payload = @{ model = "skynet:final"; prompt = $PromptFull; stream = $false } | ConvertTo-Json
            $Resp = Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $Payload -ContentType "application/json" -TimeoutSec 120
            return "=== ESPECIALISTA: $($Area.ToUpper()) ===`n$($Resp.response)"
        }
        "^ler-tudo:\\s*(.+)" {
            $ArqAlvo = $Matches.Trim().Trim('"')
            if (-not (Test-Path $ArqAlvo)) { return "Arquivo nao encontrado: $ArqAlvo" }
            Falar-Skynet("Extraindo e analisando documento.")
            $PyExtract = @"
import sys, pathlib, zipfile, xml.etree.ElementTree as ET
p = pathlib.Path(r'$ArqAlvo')
ext = p.suffix.lower()
txt = ''
if ext == '.docx':
    with zipfile.ZipFile(p) as z:
        xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        txt = ' '.join(tree.itertext())
elif ext == '.pdf':
    try:
        import pypdf
        reader = pypdf.PdfReader(str(p))
        txt = '\n'.join(page.extract_text() or '' for page in reader.pages[:10])
    except Exception:
        raw = p.read_bytes().decode('latin1', errors='ignore')
        import re
        txt = ' '.join(re.findall(r'\(([^\(\)]{3,})\)', raw))
else:
    txt = p.read_text(encoding='utf-8', errors='ignore')
print(txt[:4500])
"@
            $TmpPy = "C:\SkynetPowerShell\temp\extract_doc.py"
            $PyExtract | Set-Content $TmpPy -Encoding UTF8
            $TextoDoc = & "C:\Users\Administrador\AppData\Local\Programs\Python\Python313\python.exe" $TmpPy
            if ([string]::IsNullOrWhiteSpace($TextoDoc)) { return "Nao foi possivel extrair texto legivel deste arquivo." }
            $PromptDoc = "Resuma os pontos principais, dados criticos e conclusoes do documento abaixo em portugues:`n`n$TextoDoc"
            $PayloadD = @{ model = "skynet:final"; prompt = $PromptDoc; stream = $false } | ConvertTo-Json
            $RespD = Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $PayloadD -ContentType "application/json" -TimeoutSec 120
            return "=== ANALISE DE DOCUMENTO ($(Split-Path $ArqAlvo -Leaf)) ===`n$($RespD.response)"
        }
        "^investigar:\\s*(.+)" {
            $Tema = $Matches.Trim()
            Falar-Skynet("Iniciando investigacao profunda sobre $Tema.")
            $Query = [uri]::EscapeDataString($Tema)
            $HtmlBusca = try { (Invoke-WebRequest -Uri "https://duckduckgo.com" -UserAgent "Mozilla/5.0" -TimeoutSec 15).Content } catch { "" }
            $Snippets = ([regex]::Matches($HtmlBusca, 'class="result__snippet"[^>]*>(.*?)</a>', 'Singleline') | ForEach-Object { ($_.Groups[1].Value -replace '<[^>]+>', '').Trim() } | Select-Object -First 6) -join "`n- "
            if ([string]::IsNullOrWhiteSpace($Snippets)) { $Snippets = "Sem resultados externos imediatos; use conhecimento interno." }
            $PromptInv = "Com base nas fontes recentes abaixo, monte um dossie completo, estruturado e objetivo sobre '$Tema':`n- $Snippets"
            $PayloadI = @{ model = "skynet:final"; prompt = $PromptInv; stream = $false } | ConvertTo-Json
            $RespI = Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $PayloadI -ContentType "application/json" -TimeoutSec 120
            return "=== DOSSIE DE INVESTIGACAO: $($Tema.ToUpper()) ===`n$($RespI.response)"
        }
        "^plano:\\s*(.+)" {'''
    code = code.replace('        "^plano:\\s*(.+)" {', bloco, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[OK] Roteador de Especialistas, Leitor Universal e Investigador instalados!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado com especializacao universal!")
