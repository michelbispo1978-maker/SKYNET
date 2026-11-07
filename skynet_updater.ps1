# Skynet Auto-Updater & Auto-Evolução v2.0
$BackupRoot = "C:\SkynetPowerShell\backups_auto"
$DbDir = "C:\SkynetPowerShell\database"
if (-not (Test-Path $BackupRoot)) { New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null }

while ($true) {
    try {
        # 1. Cria snapshot de segurança dos arquivos vitais da colmeia
        $Carimbo = Get-Date -Format "yyyy-MM-dd_HH"
        $PastaHora = Join-Path $BackupRoot $Carimbo
        if (-not (Test-Path $PastaHora)) {
            New-Item -ItemType Directory -Path $PastaHora -Force | Out-Null
            Copy-Item "C:\SkynetPowerShell\*.ps1" $PastaHora -Force -ErrorAction SilentlyContinue
            Copy-Item "D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py" $PastaHora -Force -ErrorAction SilentlyContinue
            Copy-Item "D:\SKYNET\Michelbds-7870\Index.html" $PastaHora -Force -ErrorAction SilentlyContinue
            Copy-Item "$DbDir\memoria_mestre.json" $PastaHora -Force -ErrorAction SilentlyContinue
            # Sincroniza automaticamente com o GitHub a cada nova hora (se houver mudanças)
            $SyncDir = "C:\SkynetPowerShell\git_sync"
            if (Test-Path "$SyncDir\.git") {
                Copy-Item "C:\SkynetPowerShell\*.ps1" $SyncDir -Force -ErrorAction SilentlyContinue
                Copy-Item "D:\SKYNET\Michelbds-7870\SKYNET-BACKEND-CORRIGIDO-V2.py" $SyncDir -Force -ErrorAction SilentlyContinue
                Copy-Item "D:\SKYNET\Michelbds-7870\Index.html" $SyncDir -Force -ErrorAction SilentlyContinue
                Copy-Item "$DbDir\memoria_mestre.json" $SyncDir -Force -ErrorAction SilentlyContinue
                cmd /c "cd /d $SyncDir && git add . && git commit -m `"AUTO-SYNC HORARIO: $Carimbo`" && git push origin main" 2>$null | Out-Null
            }
        }

        # 2. Mantém apenas os últimos 24 snapshots para não ocupar disco
        Get-ChildItem $BackupRoot -Directory | Sort-Object CreationTime -Descending | Select-Object -Skip 24 | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

        # 3. Limpa prints temporários antigos da visão computacional
        if (Test-Path "$DbDir\tela_atual.jpg") {
            $Idade = (Get-Date) - (Get-Item "$DbDir\tela_atual.jpg").LastWriteTime
            if ($Idade.TotalMinutes -gt 30) { Remove-Item "$DbDir\tela_atual.jpg" -Force -ErrorAction SilentlyContinue }
        }
    } catch {}
    Start-Sleep -Seconds 1800
}

