Add-Type -AssemblyName System.Windows.Forms, System.Drawing
$Headers = @{ "Content-Type" = "application/json"; "Authorization" = "Bearer SKYNET-66827-FUSAO-TOTAL" }

function Enviar-Core($Cmd) {
    try {
        $B = @{ entrada = $Cmd } | ConvertTo-Json -Compress
        $R = Invoke-RestMethod -Uri "http://localhost:8080/command" -Method Post -Headers $Headers -Body ([System.Text.Encoding]::UTF8.GetBytes($B)) -TimeoutSec 60
        $Tray.ShowBalloonTip(4000, "SKYNET ($Cmd)", ($R.resultado -replace "`r`n", " "), [System.Windows.Forms.ToolTipIcon]::Info)
    } catch {
        $Tray.ShowBalloonTip(4000, "SKYNET Erro", "$_", [System.Windows.Forms.ToolTipIcon]::Error)
    }
}

$Tray = New-Object System.Windows.Forms.NotifyIcon
$Tray.Icon = [System.Drawing.SystemIcons]::Shield
$Tray.Text = "SKYNET Nucleo Windows 11 (Online)"
$Tray.Visible = $true

$Menu = New-Object System.Windows.Forms.ContextMenuStrip
$Menu.Items.Add("Abrir Central 66827 (Web)").Add_Click({ Start-Process "http://localhost:5000" })
$Menu.Items.Add("Ativar Modo Turbo Win 11").Add_Click({ Enviar-Core "modo-turbo" })
$Menu.Items.Add("Raio-X do Sistema").Add_Click({ Enviar-Core "raio-x" })
$Menu.Items.Add("Limpar Memoria RAM").Add_Click({ Enviar-Core "limpar-ram" })
$Menu.Items.Add("Sincronizar GitHub").Add_Click({ Enviar-Core "sincronizar-github" })
$Menu.Items.Add("Sair do Icone").Add_Click({ $Tray.Visible = $false; [System.Windows.Forms.Application]::Exit() })
$Tray.ContextMenuStrip = $Menu
$Tray.Add_DoubleClick({ Start-Process "http://localhost:5000" })

[System.Windows.Forms.Application]::Run()
