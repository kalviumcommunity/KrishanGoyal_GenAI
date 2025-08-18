@echo off
REM Demo script for starting the application with one-shot prompting

echo ==========================
echo StudyMate One-Shot Prompting Demo
echo ==========================

echo.
echo This script will start the backend and frontend for demonstrating one-shot prompting.
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    goto :eof
)

REM Check if requirements are installed
echo Checking dependencies...
pip show streamlit > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Failed to install requirements.
        goto :eof
    )
)

echo.
echo Starting backend server...
start powershell -NoExit -Command "cd backend && ./run_api.ps1"
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo.
echo Starting frontend...
start powershell -NoExit -Command "cd frontend && ./run_ui.ps1"

echo.
echo Starting one-shot prompting demo...
echo (This will wait for both services to be running)
timeout /t 10 /nobreak > nul

echo.
echo Running demo comparison script...
start powershell -NoExit -Command "python demo_one_shot.py"

echo.
echo ==========================
echo All services started! You can now:
echo 1. Use the demo script to see one-shot prompting comparisons
echo 2. Visit http://localhost:8502 to use the web UI
echo ==========================
