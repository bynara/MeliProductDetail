# Script to stop MeliProductDetail services

Write-Host "Stopping MeliProductDetail services..." -ForegroundColor Yellow

# Stop Python processes related to the project
$processes = Get-Process | Where-Object {
    $_.ProcessName -eq "python" -and 
    ($_.CommandLine -like "*run.py*" -or $_.CommandLine -like "*streamlit*")
}

if ($processes) {
    Write-Host "Stopping found processes..." -ForegroundColor Yellow
    $processes | Stop-Process -Force
    Write-Host "Services stopped successfully" -ForegroundColor Green
} else {
    Write-Host "No active processes found" -ForegroundColor Yellow
}

# Clean up Streamlit processes
try {
    taskkill /F /IM "streamlit.exe" 2>$null
} catch {
    # Ignore errors if no streamlit processes exist
}

Write-Host "Cleanup completed" -ForegroundColor Green
