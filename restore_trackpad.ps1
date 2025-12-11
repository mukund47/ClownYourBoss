# Restore Trackpad Script
# This will re-enable any disabled trackpad/mouse devices

Write-Host "Searching for disabled trackpad devices..." -ForegroundColor Yellow

$disabledDevices = Get-PnpDevice | Where-Object {
    ($_.Class -eq 'Mouse' -or $_.Class -eq 'HIDClass') -and 
    $_.Status -eq 'Error'
}

if ($disabledDevices) {
    Write-Host "Found $($disabledDevices.Count) disabled device(s). Enabling..." -ForegroundColor Green
    
    foreach ($device in $disabledDevices) {
        Write-Host "Enabling: $($device.FriendlyName)" -ForegroundColor Cyan
        Enable-PnpDevice -InstanceId $device.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
    }
    
    Write-Host "`nTrackpad devices have been restored!" -ForegroundColor Green
} else {
    Write-Host "No disabled trackpad devices found." -ForegroundColor Yellow
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
