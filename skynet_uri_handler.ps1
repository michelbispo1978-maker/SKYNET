param([string]$RawUri)
Add-Type -AssemblyName System.Web, System.Windows.Forms
$Cmd = $RawUri -replace '^skynet://', ''
$Cmd = [System.Web.HttpUtility]::UrlDecode($Cmd).Trim('/')
if ([string]::IsNullOrWhiteSpace($Cmd)) { $Cmd = "raio-x" }

$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }
try {
    $Body = @{ entrada = $Cmd } | ConvertTo-Json -Compress
    $Res = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $Headers -Body ([System.Text.Encoding]::UTF8.GetBytes($Body)) -TimeoutSec 90
    $Texto = if ($Res.resultado) { $Res.resultado } else { "$($Res.erro)" }
    [System.Windows.Forms.MessageBox]::Show($Texto, "SKYNET Protocolo ($Cmd)", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information) | Out-Null
} catch {
    [System.Windows.Forms.MessageBox]::Show("Erro ao executar skynet://$Cmd : $_", "SKYNET", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error) | Out-Null
}
