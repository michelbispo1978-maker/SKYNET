# Define o caminho do arquivo HTML e o local da Área de Trabalho
$HtmlPath = "C:\SkynetPowerShell\index.html"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Skynet Control Panel.lnk"

# Inicializa o objeto de automação de shell do Windows
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Configura o destino para abrir o HTML usando o navegador padrão do Windows
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c start `"`" `"$HtmlPath`""
$Shortcut.WindowStyle = 7 # Abre o prompt de comando minimizado (escondido)

# Injeta um ícone clássico do sistema (Ícone de terminal/rede do shell32.dll)
$Shortcut.IconLocation = "shell32.dll, 13"
$Shortcut.Description = "Painel de Controle Central Skynet - Interface 66827"

# Salva as modificações e consolida o atalho no desktop
$Shortcut.Save()

Write-Host "[OK] Atalho 'Skynet Control Panel' gerado com sucesso na Área de Trabalho!" -ForegroundColor Green
