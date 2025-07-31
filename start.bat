@echo off
echo Starting MeliProductDetail setup...

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
echo Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Could not create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Backend dependencies
echo Installing Backend dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Could not install Backend dependencies
    pause
    exit /b 1
)
cd ..

REM Install Frontend dependencies
echo Installing Frontend dependencies...
cd frontend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Could not install Frontend dependencies
    pause
    exit /b 1
)
cd ..

echo All dependencies installed successfully

REM Start Backend in background
echo Starting Backend...
cd backend
start /min python run.py
timeout /t 3 /nobreak >nul
cd ..

echo Backend started at http://localhost:8000

REM Start Frontend
echo Starting Frontend...
cd frontend
echo Frontend will start at http://localhost:8501
echo Press Ctrl+C to stop both services
streamlit run app.py
