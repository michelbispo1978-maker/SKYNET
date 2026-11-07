import pathlib, subprocess

core_p = pathlib.Path(r"C:\SkynetPowerShell\skynet_core.ps1")
code = core_p.read_text(encoding="utf-8")

if "saude-ssd" not in code:
    code = code.replace("vigiar-tela", "vigiar-tela|saude-ssd|pesquisar:")
    bloco = '''        "^saude-ssd" {
            $DiscosFisicos = Get-PhysicalDisk | ForEach-Object {
                $Rel = $_ | Get-StorageReliabilityCounter -ErrorAction SilentlyContinue
                $Temp = if ($Rel.Temperature) { "$($Rel.Temperature)C" } else { "N/D" }
                $Desg = if ($Rel.Wear) { "$($Rel.Wear)%" } else { "0%" }
                "$($_.FriendlyName) ($($_.MediaType)) -> Status: $($_.HealthStatus) | Temp: $Temp | Desgaste: $Desg"
            }
            $Synthesizer.SpeakAsync("Diagnostico fisico dos discos concluido.") | Out-Null
            return "Saude de Armazenamento:`n" + ($DiscosFisicos -join "`n")
        }
        "^pesquisar:\\s*(.+)" {
            $Busca = [uri]::EscapeDataString($Matches.Trim())
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            $HtmlBusca = (Invoke-WebRequest -Uri "https://duckduckgo.com" -UserAgent "Mozilla/5.0" -UseBasicParsing -TimeoutSec 15).Content
            $Trechos = ([regex]::Matches($HtmlBusca, '<a class="result__snippet"[^>]*>(.*?)</a>') | Select-Object -First 4 | ForEach-Object { $_.Groups.Value -replace '<[^>]+>', '' }) -join "`n- "
            if (-not $Trechos) { return "Nenhum resultado encontrado na busca." }
            $Payload = @{ model = "skynet:final"; prompt = "Com base nestes trechos encontrados na web, responda em portugues de forma direta e clara sobre '$($Matches)':`n- $Trechos"; stream = $false } | ConvertTo-Json
            $RespBusca = Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $Payload -ContentType "application/json" -TimeoutSec 60
            $Synthesizer.SpeakAsync($RespBusca.response) | Out-Null
            return "Pesquisa Autonoma ($($Matches)):`n$($RespBusca.response)"
        }
        "^vigiar-tela" {'''
    code = code.replace('        "^vigiar-tela" {', bloco, 1)
    core_p.write_text(code, encoding="utf-8")
    print("[OK] Saude SSD e Pesquisa Autonoma instaladas!")

subprocess.run(["powershell", "-Command", "Stop-ScheduledTask -TaskName 'SkynetCoreImortal'; Start-Sleep 1; Start-ScheduledTask -TaskName 'SkynetCoreImortal'"])
print("[CONCLUIDO] Motor Core reiniciado com diagnostico de SSD e pesquisa web!")
