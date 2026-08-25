@echo off
title NetSage AI
cd /d "%~dp0"

if not exist ".env" (
  echo First-time setup has not been completed.
  echo Starting setup...
  call SETUP_NETSAGE.bat
)

if not exist ".env" (
  echo Setup was cancelled or failed.
  pause
  exit /b 1
)

echo Starting NetSage AI...
python -m streamlit run app.py
pause
