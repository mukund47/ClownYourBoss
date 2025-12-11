# Self-elevate if not admin
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Requesting Administrator privileges..."
    Start-Process PowerShell -Verb RunAs "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

Write-Host "Starting Trackpad Restoration..." -ForegroundColor Cyan

# 0. Clean up Active Prank Elements
Write-Host "Checking for active prank processes..."
$processes = Get-Process -Name "main", "Error", "python" -ErrorAction SilentlyContinue
if ($processes) {
    Write-Host "Found active processes. Stopping them..." -ForegroundColor Yellow
    Stop-Process -Name "main", "Error", "python" -Force -ErrorAction SilentlyContinue
    Write-Host "Processes stopped." -ForegroundColor Green
}
else {
    Write-Host "No active prank processes found."
}

Write-Host "Checking for startup persistence..."
if (Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'FakeErrorApp' -ErrorAction SilentlyContinue) {
    Write-Host "Found startup registry key. Removing..." -ForegroundColor Yellow
    Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'FakeErrorApp' -ErrorAction SilentlyContinue
    Write-Host "Startup key removed." -ForegroundColor Green
}
else {
    Write-Host "No startup persistence found."
}

# 1. Scan for hardware changes
Write-Host "Scanning for hardware changes..."
pnputil /scan-devices | Out-Null

# 2. Enable ALL disabled devices
Write-Host "Enabling disabled Pnp devices..."
$disabled = Get-PnpDevice | Where-Object { $_.Status -eq 'Error' }
if ($disabled) {
    foreach ($d in $disabled) {
        Write-Host "Enabling $($d.FriendlyName)"
        try {
            Enable-PnpDevice -InstanceId $d.InstanceId -Confirm:$false -ErrorAction Continue
        }
        catch {
            Write-Host "Failed to enable $($d.FriendlyName): $_"
        }
    }
}
else {
    Write-Host "No disabled devices found."
}

# 3. Re-enable HID/Mouse specifically if they are not in Error state but weird (Toggle)
Write-Host "Toggling HID devices..."
$hids = Get-PnpDevice | Where-Object { $_.Class -eq 'HIDClass' -or $_.Class -eq 'Mouse' }
foreach ($h in $hids) {
    if ($h.FriendlyName -match 'Touch|Track|Pad|Mouse') {
        Write-Host "Resetting $($h.FriendlyName)..."
        try {
            Disable-PnpDevice -InstanceId $h.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 200
            Enable-PnpDevice -InstanceId $h.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
        }
        catch {
            # Ignore errors here, some devices can't be disabled
        }
    }
}

Write-Host "Restoration logic finished."
Write-Host "Restarting PC in 5 seconds to apply changes..." -ForegroundColor Red
Start-Sleep -Seconds 5
Restart-Computer -Force
