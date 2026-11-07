$CreatedNew = $false
$Global:SkynetMutex = New-Object System.Threading.Mutex($true, "Global\SKYNET_CORE_8080_UNICO", [ref]$CreatedNew)
if (-not $CreatedNew) { exit }

Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class Win11Native {
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
    [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, UIntPtr dwExtraInfo);
}
"@

function Notificar-Windows([string]$Titulo, [string]$Msg) {
    try {
        Add-Type -AssemblyName System.Windows.Forms, System.Drawing
        $N = New-Object System.Windows.Forms.NotifyIcon
        $N.Icon = [System.Drawing.SystemIcons]::Information
        $N.BalloonTipTitle = $Titulo
        $N.BalloonTipText = if ($Msg.Length -gt 200) { $Msg.Substring(0, 200) + "..." } else { $Msg }
        $N.Visible = $true
        $N.ShowBalloonTip(5000)
        Start-Job -ScriptBlock { param($ic) Start-Sleep 6; $ic.Dispose() } -ArgumentList $N | Out-Null
    } catch {}
}

Add-Type -AssemblyName System.Speech
if (-not $Synthesizer) { $Synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer }
$Global:FilaVoz = [System.Collections.Queue]::Synchronized((New-Object System.Collections.Queue))
function Falar-Skynet([string]$Texto) {
    if ([string]::IsNullOrWhiteSpace($Texto) -or -not $Synthesizer) { return }
    if ($Synthesizer.State -eq 'Speaking') { return }
    if ($Global:FilaVoz.Count -gt 0) { $Global:FilaVoz.Clear() }
    try { $Synthesizer.SpeakAsync($Texto) | Out-Null } catch {}
}
Register-ObjectEvent -InputObject $Synthesizer -EventName SpeakCompleted -Action {
    if ($Global:FilaVoz.Count -gt 0) {
        $Prox = $Global:FilaVoz.Dequeue()
        $Event.Sender.SpeakAsync($Prox) | Out-Null
    }
} | Out-Null

# Configura��es Avan�adas Skynet Core v3.6.0 + Deep Network Scan
$Port = 8080
$Url = "http://localhost:$Port/"
$DbDir = "C:\SkynetPowerShell\database"
$OllamaUri = "http://127.0.0.1:11434/api/generate"
$SecretToken = "SKYNET-66827-FUSAO-TOTAL"
$MaxLogs = 100

$global:SystemUpdated = $false

if (-not (Test-Path $DbDir)) { New-Item -ItemType Directory -Path $DbDir | Out-Null }

Add-Type -AssemblyName System.Speech
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$Synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer

function Enviar-Toast ($Titulo, $Mensagem) {
    try {
        $Template = @"
<toast><visual><binding template="ToastGeneric">
    <text>$Titulo</text><text>$Mensagem</text>
</binding></visual></toast>
"@
        $Xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $Xml.LoadXml($Template)
        $Toast = New-Object Windows.UI.Notifications.ToastNotification($Xml)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Skynet Central").Show($Toast)
    } catch {}
}

function Executar-LogRotation {
    try {
        $LogFiles = Get-ChildItem -Path $DbDir -Filter "*.json" | Sort-Object LastWriteTime -Descending
        if ($LogFiles.Count -gt $MaxLogs) {
            $LogFiles | Select-Object -Skip $MaxLogs | Remove-Item -Force -ErrorAction SilentlyContinue
        }
    } catch {}
}

$Listener = New-Object System.Net.HttpListener
$Listener.Prefixes.Add($Url)

try {
    $Listener.Start()
    Falar-Skynet("Sensores de rede profunda ativados. Monitorando conex�es da malha.")
    
    while ($Listener.IsListening) {
        $Context = $Listener.GetContext()
                $Req = $Context.Request
                $Resp = $Context.Response
                if ($Req.Url.AbsolutePath -eq "/falando") {
                    $EstaFalando = ($Synthesizer.State -eq "Speaking") -or ($Global:FilaVoz.Count -gt 0)
                    $JsonOut = @{ falando = $EstaFalando } | ConvertTo-Json
                    $Buf = [System.Text.Encoding]::UTF8.GetBytes($JsonOut)
                    $Resp.ContentType = "application/json"
                    $Resp.Headers.Add("Access-Control-Allow-Origin", "*")
                    $Resp.OutputStream.Write($Buf, 0, $Buf.Length)
                    $Resp.Close()
                    continue
                }
                $Req = $Context.Request
                $Resp = $Context.Response
                
        $Request = $Context.Request
        $Response = $Context.Response

        $Response.ContentType = "application/json; charset=utf-8"
        $Response.Headers.Add("Access-Control-Allow-Origin", "*")
        $Response.Headers.Add("Access-Control-Allow-Headers", "Authorization, Content-Type")
        $Response.Headers.Add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        $ResponseData = ""

        if ($Request.HttpMethod -eq "OPTIONS") { $Response.StatusCode = 200; $Response.Close(); continue }

        if ($Request.Url.AbsolutePath -eq "/status") {
            $Cpu = [math]::Round((Get-CimInstance Win32_Processor).LoadPercentage, 1)
            $RamLivre = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory
            $RamTotal = (Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize
            $RamUso = [math]::Round((($RamTotal - $RamLivre) / $RamTotal) * 100, 1)
            
            $ResponseData = @{ status = "ONLINE"; cpu = $Cpu; ram = $RamUso; versao = "3.6.0"; mutacao_pendente = $global:SystemUpdated } | ConvertTo-Json
            if ($global:SystemUpdated) { $global:SystemUpdated = $false }
            $Response.StatusCode = 200
        }
        else {
            $AuthHeader = $Request.Headers["Authorization"]
            if ($AuthHeader -ne "Bearer $SecretToken") {
                $ResponseData = @{ status = "ERROR"; erro = "Acesso negado." } | ConvertTo-Json
                $Response.StatusCode = 401
                $Buffer = [System.Text.Encoding]::UTF8.GetBytes($ResponseData)
                $Response.ContentLength64 = $Buffer.Length
                $Response.OutputStream.Write($Buffer, 0, $Buffer.Length)
                $Response.Close()
                continue
            }

            switch ($Request.Url.AbsolutePath) {
                "/system/network-audit" {
                    if ($Request.HttpMethod -eq "POST") {
                        $Id = (Get-Date).Ticks
                        $Reader = New-Object System.IO.StreamReader($Request.InputStream)
                        $Body = $Reader.ReadToEnd()
                        Set-Content -Path (Join-Path $DbDir "net_$Id.json") -Value $Body
                        Executar-LogRotation
                        $ResponseData = @{ status = "SUCCESS" } | ConvertTo-Json
                        $Response.StatusCode = 200
                    }
                }
                "/command" {
                    if ($Request.HttpMethod -eq "POST") {
                        $Reader = New-Object System.IO.StreamReader($Request.InputStream)
                        $Body = $Reader.ReadToEnd()
                        $InputData = $Body | ConvertFrom-Json
                        $RawText = if ($InputData.entrada) { $InputData.entrada } else { $InputData.comando; $InputData.prompt }
                        $LogId = (Get-Date).Ticks
                        
                        if ($RawText -match "^shell-ajuda$") {
                            $Lista = "COMANDOS MODO SHELL: shell-explorer (Pastas) | shell-wifi (Rede) | shell-som (Audio) | shell-ram (Limpar Memoria) | shell-reiniciar | shell-desligar | modo-shell-windows (Voltar ao Windows)"
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Shell"; resultado = $Lista } | ConvertTo-Json -Compress
                        } elseif ($RawText -match "^shell-explorer$") {
                            Start-Process "explorer.exe"
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Shell"; resultado = "Explorador de Arquivos aberto." } | ConvertTo-Json -Compress
                        } elseif ($RawText -match "^shell-wifi$") {
                            Start-Process "ms-settings:network-wifi"
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Shell"; resultado = "Configuracoes de Wi-Fi abertas." } | ConvertTo-Json -Compress
                        } elseif ($RawText -match "^shell-som$") {
                            Start-Process "ms-settings:sound"
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Shell"; resultado = "Configuracoes de Audio abertas." } | ConvertTo-Json -Compress
                        } elseif ($RawText -match "^shell-ram$") {
                            [System.GC]::Collect()
                            $Os = Get-CimInstance Win32_OperatingSystem
                            $RamPct = [math]::Round((($Os.TotalVisibleMemorySize - $Os.FreePhysicalMemory) / $Os.TotalVisibleMemorySize) * 100, 1)
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Shell"; resultado = "Memoria otimizada. Uso atual de RAM: $RamPct%" } | ConvertTo-Json -Compress
                        } elseif ($RawText -match "^shell-reiniciar$") {
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Shell"; resultado = "Reiniciando Windows em 3 segundos..." } | ConvertTo-Json -Compress
                            Start-Process "shutdown.exe" -ArgumentList "/r /t 3"
                        } elseif ($RawText -match "^shell-desligar$") {
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Shell"; resultado = "Desligando Windows em 3 segundos..." } | ConvertTo-Json -Compress
                            Start-Process "shutdown.exe" -ArgumentList "/s /t 3"
                        } elseif ($RawText -match "^modo-shell-skynet$") {
                            Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" -Name "Shell" -Value 'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\SkynetPowerShell\skynet_os_shell.ps1"' -Force
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Shell"; resultado = "=== MODO SHELL SKYNET ATIVADO === Encerre a sessao (logoff) ou reinicie o PC para a Interface 66827 assumir a tela." } | ConvertTo-Json -Compress
                        } elseif ($RawText -match "^modo-shell-windows$") {
                            Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" -Name "Shell" -ErrorAction SilentlyContinue
                            Start-Process "explorer.exe"
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Shell"; resultado = "=== MODO SHELL WINDOWS 11 RESTAURADO === Area de Trabalho padrao reativada." } | ConvertTo-Json -Compress
                        } elseif ($RawText -match "^(get-|set-|stop-|start-|restart-|mkdir|dir|task|ipconfig)") {
                            $TerminalOutput = Invoke-Expression $RawText Out-String
                            $ResponseData = @{ status = "SUCCESS"; decisao = "Terminal"; resultado = $TerminalOutput.Trim() } | ConvertTo-Json
                            $CmdPayload = @{ id = $LogId; data = (Get-Date -Format "yyyy-MM-dd HH:mm:ss"); tipo = "Terminal"; entrada = $RawText } | ConvertTo-Json
                            Set-Content -Path (Join-Path $DbDir "cmd_$LogId.json") -Value $CmdPayload
                        } else {
                            $Model = if ($InputData.modelo) { $InputData.modelo } else { "skynet:final" }
                            $OllamaPayload = @{ model = $Model; prompt = $RawText; stream = $false } | ConvertTo-Json
                            $OllamaResponse = Invoke-RestMethod -Uri $OllamaUri -Method Post -Body $OllamaPayload -ContentType "application/json" -TimeoutSec 60
                            Falar-Skynet($OllamaResponse.response)
                            $Resumo = if ($OllamaResponse.response.Length -gt 120) { $OllamaResponse.response.Substring(0, 117) + "..." } else { $OllamaResponse.response }
                            Enviar-Toast -Titulo "RESPOSTA DA IA" -Mensagem $Resumo
                            $ResponseData = @{ status = "SUCCESS"; decisao = "IA Local"; resultado = $OllamaResponse.response } | ConvertTo-Json
                            $IaPayload = @{ id = $LogId; data = (Get-Date -Format "yyyy-MM-dd HH:mm:ss"); tipo = "Intelig�ncia Artificial"; entrada = $RawText } | ConvertTo-Json
                            Set-Content -Path (Join-Path $DbDir "cmd_$LogId.json") -Value $IaPayload
                        }
                        Executar-LogRotation
                        $Response.StatusCode = 200
                    }
                }
                "/logs" {
                    $Logs = Get-ChildItem -Path $DbDir -Filter "*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 10
                    $LogList = foreach ($File in $Logs) { Get-Content -Path $File.FullName | ConvertFrom-Json }
                    $ResponseData = $LogList | ConvertTo-Json
                    $Response.StatusCode = 200
                }
            }
        }

        $Buffer = [System.Text.Encoding]::UTF8.GetBytes($ResponseData)
        $Response.ContentLength64 = $Buffer.Length
        $Response.OutputStream.Write($Buffer, 0, $Buffer.Length)
        $Response.Close()
    }
} catch { Write-Host "[ERRO CORE]: $_" -ForegroundColor Red } finally { try { if ($Listener.IsListening) { $Listener.Stop() } } catch {} }



