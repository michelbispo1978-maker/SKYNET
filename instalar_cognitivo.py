import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

if "analisar-tela:" not in code:
    code = code.replace("historico", "historico|analisar-tela:|aprender-pasta:|plano:")
    bloco = '''        "^analisar-tela:\\s*(.*)" {
            $PerguntaTela = if ($Matches.Trim()) { $Matches.Trim() } else { "Descreva e resuma o que esta na tela." }
            Falar-Skynet("Analisando o conteudo da tela.")
            Add-Type -AssemblyName System.Windows.Forms,System.Drawing
            $Bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            $Bmp = New-Object System.Drawing.Bitmap $Bounds.Width, $Bounds.Height
            $G = [System.Drawing.Graphics]::FromImage($Bmp)
            $G.CopyFromScreen($Bounds.Location, [System.Drawing.Point]::Empty, $Bounds.Size)
            $TmpImg = "C:\\SkynetPowerShell\\temp\\ocr_screen.png"
            New-Item -ItemType Directory -Path "C:\\SkynetPowerShell\\temp" -Force | Out-Null
            $Bmp.Save($TmpImg, [System.Drawing.Imaging.ImageFormat]::Png)
            $G.Dispose(); $Bmp.Dispose()
            try {
                Add-Type -AssemblyName System.Runtime.WindowsRuntime
                $null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
                $null = [Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
                $null = [Windows.Graphics.Imaging.BitmapDecoder,Windows.Foundation,ContentType=WindowsRuntime]
                $AsTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters().ParameterType.Name -eq 'IAsyncOperation`1' })
                function Await($WinRtTask, $ResultType) {
                    $NetTask = $AsTaskGeneric.MakeGenericMethod($ResultType).Invoke($null, @($WinRtTask))
                    $NetTask.Wait(-1) | Out-Null
                    $NetTask.Result
                }
                $File = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($TmpImg)) ([Windows.Storage.StorageFile])
                $Stream = Await ($File.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
                $Decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($Stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
                $SoftBmp = Await ($Decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
                $Ocr = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
                $OcrRes = Await ($Ocr.RecognizeAsync($SoftBmp)) ([Windows.Media.Ocr.OcrResult])
                $Stream.Dispose()
                $TextoTela = $OcrRes.Text
                if ([string]::IsNullOrWhiteSpace($TextoTela)) { return "Nenhum texto legivel detectado na tela." }
                $PromptOcr = "Texto capturado da tela do usuario:`n$TextoTela`n`nPedido do usuario: $PerguntaTela"
                $Payload = @{ model = "skynet:final"; prompt = $PromptOcr; stream = $false } | ConvertTo-Json
                $RespOcr = Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $Payload -ContentType "application/json" -TimeoutSec 90
                return "=== ANALISE VISUAL DA TELA ===`n$($RespOcr.response)"
            } catch {
                return "Erro no OCR nativo: $_"
            }
        }
        "^aprender-pasta:\\s*(.+)" {
            $DirAlvo = $Matches.Trim().Trim('"')
            if (-not (Test-Path $DirAlvo)) { return "Pasta nao encontrada: $DirAlvo" }
            $Exts = @(".txt", ".md", ".py", ".ps1", ".json", ".log")
            $Arqs = Get-ChildItem -Path $DirAlvo -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $Exts -contains $_.Extension.ToLower() } | Select-Object -First 40
            $Indice = @()
            foreach ($a in $Arqs) {
                $Conteudo = (Get-Content $a.FullName -Raw -ErrorAction SilentlyContinue)
                if ($Conteudo) {
                    if ($Conteudo.Length -gt 1800) { $Conteudo = $Conteudo.Substring(0, 1800) }
                    $Indice += @{ arquivo = $a.Name; caminho = $a.FullName; texto = $Conteudo }
                }
            }
            $RagFile = "C:\\SkynetPowerShell\\database\\rag_index.json"
            New-Item -ItemType Directory -Path "C:\\SkynetPowerShell\\database" -Force | Out-Null
            $Indice | ConvertTo-Json -Depth 3 | Set-Content $RagFile -Encoding UTF8
            Falar-Skynet("Base de conhecimento atualizada com $($Indice.Count) arquivos.")
            return "=== RAG LOCAL ATUALIZADO ===`nPasta: $DirAlvo`nArquivos indexados: $($Indice.Count)`nAgora a IA consultara esses documentos automaticamente nas suas perguntas."
        }
        "^plano:\\s*(.+)" {
            $Objetivo = $Matches.Trim()
            Falar-Skynet("Criando e executando plano autonomo.")
            $GuiaCmds = "Comandos validos disponiveis: raio-x, saude-ssd, limpar-ram, otimizar-windows, destravar-pc, velocidade-net, rede-wifi, energia, consultar-memoria, gerar-relatorio, sincronizar-github, analisar-tela: resumo"
            $PromptPlano = "Converta o objetivo abaixo em uma lista simples de comandos validos (um por linha, sem explicacoes, sem numeracao). $GuiaCmds`nObjetivo: $Objetivo"
            $PayloadP = @{ model = "skynet:final"; prompt = $PromptPlano; stream = $false } | ConvertTo-Json
            $RespP = Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $PayloadP -ContentType "application/json" -TimeoutSec 60
            $Passos = $RespP.response -split "`r?`n" | ForEach-Object { $_.Trim().TrimStart('-','*','1','2','3','4','5','6','7','8','9','0','.',' ') } | Where-Object { $_ -ne "" } | Select-Object -First 5
            if (-not $Passos) { return "Nao consegui gerar passos executaveis para esse objetivo." }
            $RelatorioPlano = @("=== EXECUCAO DE PLANO AUTONOMO ===", "Objetivo: $Objetivo", "Passos: $($Passos -join ' -> ')", "")
            $HLocal = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
            foreach ($p in $Passos) {
                try {
                    $B = @{ entrada = $p } | ConvertTo-Json -Compress
                    $R = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $HLocal -Body ([System.Text.Encoding]::UTF8.GetBytes($B)) -TimeoutSec 60
                    $RelatorioPlano += "[PASSO: $p]`n$($R.resultado)`n"
                } catch {
                    $RelatorioPlano += "[PASSO: $p] Falhou: $_`n"
                }
            }
            return ($RelatorioPlano -join "`n")
        }
        "^historico" {'''
    code = code.replace('        "^historico" {', bloco, 1)

    # Injeta busca automatica no RAG Local antes de enviar perguntas ao Ollama
    rag_hook = '''$RagContext = ""
                                if (Test-Path "C:\\SkynetPowerShell\\database\\rag_index.json") {
                                    $Docs = @(Get-Content "C:\\SkynetPowerShell\\database\\rag_index.json" -Raw | ConvertFrom-Json)
                                    $Palavras = $RawText.ToLower() -split '\\W+' | Where-Object { $_.Length -ge 4 }
                                    $Hits = foreach ($d in $Docs) {
                                        $Score = 0
                                        foreach ($w in $Palavras) { if ($d.texto.ToLower().Contains($w)) { $Score++ } }
                                        if ($Score -gt 0) { [PSCustomObject]@{ Score = $Score; Nome = $d.arquivo; Texto = $d.texto } }
                                    }
                                    $TopDocs = $Hits | Sort-Object Score -Descending | Select-Object -First 2
                                    if ($TopDocs) {
                                        $RagContext = "Documentos locais relevantes:`n" + (($TopDocs | ForEach-Object { "[$($_.Nome)]: $($_.Texto)" }) -join "`n---`n") + "`n`n"
                                    }
                                }
                                $OllamaPayload = @{ model = $Model; prompt = ($MemContext + $RagContext + $RawText); stream = $false } | ConvertTo-Json'''
    code = code.replace(
        '$OllamaPayload = @{ model = $Model; prompt = ($MemContext + $RawText); stream = $false } | ConvertTo-Json',
        rag_hook,
        1
    )

    core_p.write_text(code, encoding="utf-8")
    print("[OK] Visao OCR, RAG Local e Agente Planejador instalados no skynet_core.ps1!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core 8080 reiniciado com inteligencia cognitiva!")
