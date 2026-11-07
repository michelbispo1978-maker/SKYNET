# Rotina de Backup Semanal Skynet - Interface 66827
$DbDir = "C:\SkynetPowerShell\database"
$BackupDir = "C:\SkynetPowerShell\backups"
$MaxBackups = 4 # Mantém apenas as últimas 4 semanas (1 mês) para poupar disco

if (Test-Path $DbDir) {
    $Files = Get-ChildItem -Path $DbDir -Filter "*.json"
    if ($Files.Count -gt 0) {
        $DataAtual = Get-Date -Format "yyyy-MM-dd_HH-mm"
        $ZipPath = Join-Path $BackupDir "skynet_db_backup_$DataAtual.zip"
        
        # Compacta todos os registros do banco NoSQL
        Compress-Archive -Path "$DbDir\*" -DestinationPath $ZipPath -Force
        
        # Rotação de Backups: apaga arquivos .zip mais antigos que 4 semanas
        $OldZips = Get-ChildItem -Path $BackupDir -Filter "*.zip" | Sort-Object LastWriteTime -Descending
        if ($OldZips.Count -gt $MaxBackups) {
            $OldZips | Select-Object -Skip $MaxBackups | Remove-Item -Force -ErrorAction SilentlyContinue
        }
    }
}
