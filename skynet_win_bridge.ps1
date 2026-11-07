param([string]$Modo = "prompt", [string]$Alvo = "")
Add-Type -AssemblyName Microsoft.VisualBasic, System.Windows.Forms
$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }

if ($Modo -eq "arquivo" -and $Alvo) {
    $Cmd = "ler-tudo: $Alvo"
} elseif ($Modo -eq "pasta" -and $Alvo) {
    $Cmd = "aprender-pasta: $Alvo"
} else {
    $Cmd = [Microsoft.VisualBasic.Interaction]::InputBox("Digite um comando ou pergunta para a SKYNET:", "SKYNET FUSAO WINDOWS (Ctrl+Alt+S)", "raio-x")
}

if ([string]::IsNullOrWhiteSpace($Cmd)) { exit }

try {
    $Body = @{ entrada = $Cmd } | ConvertTo-Json -Compress
    $Res = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $Headers -Body ([System.Text.Encoding]::UTF8.GetBytes($Body)) -TimeoutSec 120
    $Texto = if ($Res.resultado) { $Res.resultado } else { "$($Res.erro)" }
    [System.Windows.Forms.MessageBox]::Show($Texto, "SKYNET - Resposta Nativa", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information) | Out-Null
} catch {
    [System.Windows.Forms.MessageBox]::Show("Erro ao comunicar com Skynet Core 8080: $_", "SKYNET", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error) | Out-Null
}
