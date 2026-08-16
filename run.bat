@echo off
title SearchIt - Campus Lost and Found Platform
echo ===================================================
echo   SearchIt - Campus Lost ^& Found Platform
echo ===================================================
echo.

if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat

echo [INFO] Starting SearchIt local server...
echo [INFO] App will automatically open in browser at http://127.0.0.1:5000
echo.

python run.py

pause
