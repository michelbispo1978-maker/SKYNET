# Define o caminho do arquivo HTML e o local da rea de Trabalho
$HtmlPath = "C:\SkynetPowerShell\index.html"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Skynet Control Panel.lnk"

# Inicializa o objeto de automao de shell do Windows
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Configura o destino para abrir o HTML usando o navegador padro do Windows
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c start `"`" `"$HtmlPath`""
$Shortcut.WindowStyle = 7 # Abre o prompt de comando minimizado (escondido)

# Injeta um cone clssico do sistema (cone de terminal/rede do shell32.dll)
$Shortcut.IconLocation = "shell32.dll, 13"
$Shortcut.Description = "Painel de Controle Central Skynet - Interface 66827"

# Salva as modificaes e consolida o atalho no desktop
$Shortcut.Save()

Write-Host "[OK] Atalho 'Skynet Control Panel' gerado com sucesso na rea de Trabalho!" -ForegroundColor Green
