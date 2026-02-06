@echo off
echo ========================================
echo AI Lung Cancer Detection Server
echo ========================================
echo.
echo Changing to backend directory...
cd /d "%~dp0backend"
if errorlevel 1 (
    echo ERROR: Could not change to backend directory!
    pause
    exit /b 1
)
echo Starting server...
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start!
    echo Make sure you are in the virtual environment and all dependencies are installed.
    pause
    exit /b 1
)
pause
