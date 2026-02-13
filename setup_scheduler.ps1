$Action = New-ScheduledTaskAction -Execute "c:\Users\mabia\OneDrive\Desktop\Projet voltaire\projet_voltaire_tests\run_tests.bat"
$Trigger = New-ScheduledTaskTrigger -Daily -At 9am
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -TaskName "ProjetVoltaireAutoTests" -Description "Daily automation test for Projet Voltaire"
Write-Host "Task 'ProjetVoltaireAutoTests' created successfully."
