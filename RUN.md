# Startup Scripts - MeliProductDetail

This directory contains automated scripts to facilitate the setup and startup of the MeliProductDetail project.

## Available Files

- **`launch.bat`** - Simple script for Windows users (recommended)
- **`start.ps1`** - Main PowerShell script (more complete)
- **`start.bat`** - Basic batch alternative
- **`stop.ps1`** - Script to stop all services

## Quick Usage

### Option 1: Simple Start (Recommended)
```cmd
launch.bat
```
Just double-click on `launch.bat` or run it from the command line.

### Option 2: Direct PowerShell
```powershell
powershell -ExecutionPolicy Bypass -File "start.ps1"
```

### Option 3: PowerShell (requires permissions)
```powershell
.\start.ps1
```

### Stop Services
```powershell
.\stop.ps1
```

## What the script does

1. **Verifies Python**: Confirms that Python 3.8+ is installed and accessible
2. **Creates virtual environment**: Generates a local `venv` if it doesn't exist
3. **Verifies files**: Confirms that all necessary files exist
4. **Installs dependencies**: Automatically installs all dependencies:
   - Backend: FastAPI, uvicorn, pydantic, python-jose, passlib, requests, pytest
   - Frontend: streamlit, requests, Pillow, streamlit-carousel, pydantic, pytest
5. **Starts Backend**: Runs the FastAPI server on port 8000
6. **Verifies Backend**: Confirms that the server responds correctly
7. **Starts Frontend**: Runs Streamlit on port 8501
8. **Automatic management**: Cleans up processes on exit

## Access URLs

Once started, you'll have access to:

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs
- **Network URL**: A local network URL will be shown for access from other devices

## Requirements

- **Python 3.8 or higher** installed on the system
- **Internet connection** to download dependencies (first time only)
- **Ports 8000 and 8501 available**
- **Windows PowerShell** (included in Windows by default)

## Enhanced Script Features

- ✅ **Complete verification** of dependencies and files
- ✅ **Silent installation** of packages (no log spam)
- ✅ **Automatic verification** of Backend status
- ✅ **Robust error handling** with clear messages
- ✅ **Automatic cleanup** of processes on exit
- ✅ **Clear information** about URLs and service status
- ✅ **Compatibility** with Windows execution policies

## Troubleshooting

### PowerShell Permission Error
If you get a permission error when running `start.ps1` directly:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Or simply use `launch.bat` which automatically bypasses this issue.

### Python Not Found
- Make sure Python is installed from https://python.org
- During installation, check "Add Python to PATH"
- Restart the terminal after installation

### Ports Already in Use
- If ports 8000 or 8501 are in use, stop other services using them
- Use `netstat -ano | findstr :8000` to see which process is using the port
- Use `taskkill /PID [number] /F` to terminate the process

### Dependencies Won't Install
- Verify internet connection
- If behind a corporate proxy, configure pip appropriately
- Run `pip install --upgrade pip` in the virtual environment

## Additional Notes

- Dependencies are only downloaded the first time
- The virtual environment is created automatically and reused
- Services stop automatically when closing the script (Ctrl+C)
- The script verifies Backend health before continuing
