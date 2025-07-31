# Script to start Frontend and Backend for MeliProductDetail
# Verifies Python, creates virtual environment and installs dependencies

Write-Host "Starting MeliProductDetail setup..." -ForegroundColor Green

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment if it doesn't exist
$venvPath = ".\venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Could not create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Virtual environment created successfully" -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$activateScript = ".\venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "ERROR: Virtual environment activation script not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Verify pip works
Write-Host "Verifying pip..." -ForegroundColor Yellow
pip --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pip is not working correctly" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install Backend dependencies
Write-Host "Installing Backend dependencies..." -ForegroundColor Yellow
if (-not (Test-Path "backend\requirements.txt")) {
    Write-Host "ERROR: Backend requirements.txt file not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Set-Location backend
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Could not install Backend dependencies" -ForegroundColor Red
    Set-Location ..
    Read-Host "Press Enter to exit"
    exit 1
}
Set-Location ..
Write-Host "Backend dependencies installed successfully" -ForegroundColor Green

# Install Frontend dependencies
Write-Host "Installing Frontend dependencies..." -ForegroundColor Yellow
if (-not (Test-Path "frontend\requirements.txt")) {
    Write-Host "ERROR: Frontend requirements.txt file not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Set-Location frontend
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Could not install Frontend dependencies" -ForegroundColor Red
    Set-Location ..
    Read-Host "Press Enter to exit"
    exit 1
}
Set-Location ..
Write-Host "Frontend dependencies installed successfully" -ForegroundColor Green

Write-Host "All dependencies installed successfully" -ForegroundColor Green

# Verify required files
Write-Host "Verifying required files..." -ForegroundColor Yellow
if (-not (Test-Path "backend\run.py")) {
    Write-Host "ERROR: backend\run.py file not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
if (-not (Test-Path "frontend\app.py")) {
    Write-Host "ERROR: frontend\app.py file not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Start Backend in background
Write-Host "Starting Backend..." -ForegroundColor Yellow
Set-Location backend
$backendProcess = Start-Process -FilePath "python" -ArgumentList "run.py" -WindowStyle Minimized -PassThru
Set-Location ..

if ($backendProcess -eq $null) {
    Write-Host "ERROR: Could not start Backend" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Waiting for Backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verify Backend is running
Write-Host "Verifying Backend..." -ForegroundColor Yellow
$backendOk = $false
for ($i = 1; $i -le 3; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        $backendOk = $true
        break
    } catch {
        Write-Host "Attempt $i/3: Backend not responding yet, waiting..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }
}

if ($backendOk) {
    Write-Host "Backend started successfully at http://localhost:8000" -ForegroundColor Green
    Write-Host "Documentation available at http://localhost:8000/docs" -ForegroundColor Cyan
} else {
    Write-Host "Warning: Backend not responding on expected port" -ForegroundColor Yellow
    Write-Host "Checking if process is still running..." -ForegroundColor Yellow
    if ($backendProcess.HasExited) {
        Write-Host "ERROR: Backend process has closed unexpectedly" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    } else {
        Write-Host "Backend process is still running, continuing..." -ForegroundColor Yellow
    }
}

# Start Frontend
Write-Host "Starting Frontend..." -ForegroundColor Yellow
Set-Location frontend
Write-Host "Frontend will start at http://localhost:8501" -ForegroundColor Green
Write-Host "Backend running at http://localhost:8000" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "=== SERVICES STARTED ===" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:8501" -ForegroundColor White
Write-Host "Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "Press Ctrl+C to stop both services" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Cyan

try {
    streamlit run app.py
} finally {
    # Clean up processes on exit
    Write-Host "" -ForegroundColor White
    Write-Host "Stopping services..." -ForegroundColor Yellow
    if ($backendProcess -and -not $backendProcess.HasExited) {
        $backendProcess.Kill()
        Write-Host "Backend stopped" -ForegroundColor Green
    }
    # Stop any other related python processes
    Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.CommandLine -like "*run.py*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "Services stopped successfully" -ForegroundColor Green
}