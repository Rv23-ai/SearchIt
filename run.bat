@echo off
title SearchIt - Campus Lost & Found Platform
echo ===================================================
echo   SearchIt - Campus Lost & Found Platform
echo ===================================================
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment (.venv)...
    call .venv\Scripts\activate.bat
) else (
    echo [WARNING] No .venv found. Running using system Python...
)

echo [INFO] Starting SearchIt local server...
echo [INFO] App will automatically open in your default browser at http://127.0.0.1:5000
echo.

python run.py

pause
