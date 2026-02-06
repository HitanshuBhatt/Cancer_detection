@echo off
REM Run server from root directory - automatically changes to backend
echo ========================================
echo AI Lung Cancer Detection Server
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Change to backend directory
cd /d "%SCRIPT_DIR%backend"
if errorlevel 1 (
    echo ERROR: Could not find backend directory!
    echo Make sure you're running this from the project root.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "..\venv\Scripts\activate.bat" (
    echo WARNING: Virtual environment not found!
    echo Please activate your virtual environment first.
    echo.
)

echo Starting server from backend directory...
echo Server will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
