@echo off
title NetSage AI - First Time Setup
cd /d "%~dp0"

echo ==========================================
echo        NETSAGE AI - FIRST TIME SETUP
echo ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
  echo Python is not installed or not available in PATH.
  echo Install Python from https://www.python.org/downloads/windows/
  pause
  exit /b 1
)

echo Installing required packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Package installation failed.
  pause
  exit /b 1
)

echo.
echo Enter your Gemini API key.
echo IMPORTANT: The key will be stored only in this PC's .env file.
set /p GEMKEY=Gemini API Key: 

if "%GEMKEY%"=="" (
  echo No key entered. Setup cancelled.
  pause
  exit /b 1
)

(
echo GEMINI_API_KEY=%GEMKEY%
echo NETSAGE_MODEL=gemini-3.5-flash-lite
) > .env

echo.
echo Setup complete.
echo You can now double-click START_NETSAGE.bat every time.
echo.
pause
