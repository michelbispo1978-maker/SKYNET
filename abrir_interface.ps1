schtasks.exe /Run /TN "SkynetWeb5000Imortal" 2>$null | Out-Null
Start-Sleep -Milliseconds 800
$Url = "http" + "://localhost:5000"
Start-Process $Url
