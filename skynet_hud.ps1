Add-Type -AssemblyName System.Windows.Forms, System.Drawing

$Form = New-Object System.Windows.Forms.Form
$Form.Text = "SKYNET HUD"
$Form.Size = New-Object System.Drawing.Size(270, 58)
$Form.FormBorderStyle = "None"
$Form.TopMost = $true
$Form.BackColor = [System.Drawing.Color]::FromArgb(12, 22, 38)
$Form.Opacity = 0.88
$Form.StartPosition = "Manual"
$Screen = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$Form.Location = New-Object System.Drawing.Point(($Screen.Width - 285), 15)

# Permite arrastar o HUD para qualquer canto da tela
$dragging = $false; $dragCursor = [System.Drawing.Point]::Empty; $dragForm = [System.Drawing.Point]::Empty
$Form.Add_MouseDown({ $script:dragging = $true; $script:dragCursor = [System.Windows.Forms.Cursor]::Position; $script:dragForm = $Form.Location })
$Form.Add_MouseMove({ if ($script:dragging) { $dif = [System.Drawing.Point]::Subtract([System.Windows.Forms.Cursor]::Position, [System.Drawing.Size]$script:dragCursor); $Form.Location = [System.Drawing.Point]::Add($script:dragForm, [System.Drawing.Size]$dif) } })
$Form.Add_MouseUp({ $script:dragging = $false })

$Lbl = New-Object System.Windows.Forms.Label
$Lbl.ForeColor = [System.Drawing.Color]::FromArgb(0, 240, 255)
$Lbl.Font = New-Object System.Drawing.Font("Consolas", 8.5, [System.Drawing.FontStyle]::Bold)
$Lbl.Location = New-Object System.Drawing.Point(10, 8)
$Lbl.Size = New-Object System.Drawing.Size(175, 42)
$Lbl.Text = "SKYNET ONLINE`nCarregando telemetria..."
$Form.Controls.Add($Lbl)

$Btn = New-Object System.Windows.Forms.Button
$Btn.Text = "⚡ CMD"
$Btn.FlatStyle = "Flat"
$Btn.BackColor = [System.Drawing.Color]::FromArgb(0, 131, 143)
$Btn.ForeColor = [System.Drawing.Color]::White
$Btn.Font = New-Object System.Drawing.Font("Segoe UI", 8, [System.Drawing.FontStyle]::Bold)
$Btn.Location = New-Object System.Drawing.Point(190, 13)
$Btn.Size = New-Object System.Drawing.Size(68, 30)
$Btn.Add_Click({ Start-Process "powershell.exe" -ArgumentList "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File C:\SkynetPowerShell\skynet_win_bridge.ps1 -Modo prompt" })
$Form.Controls.Add($Btn)

$Timer = New-Object System.Windows.Forms.Timer
$Timer.Interval = 3000
$Timer.Add_Tick({
    try {
        $Os = Get-CimInstance Win32_OperatingSystem
        $RamPct = [math]::Round((($Os.TotalVisibleMemorySize - $Os.FreePhysicalMemory) / $Os.TotalVisibleMemorySize) * 100, 0)
        $CpuPct = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
        $Lbl.Text = "SKYNET HUD [ONLINE]`nCPU: $CpuPct% | RAM: $RamPct%"
    } catch {}
})
$Timer.Start()
[System.Windows.Forms.Application]::Run($Form)
