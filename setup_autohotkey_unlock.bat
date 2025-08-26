@echo off
echo ===============================================
echo Jarvis AutoHotkey Screen Unlock Setup
echo ===============================================
echo.
echo This script will set up AutoHotkey for reliable screen unlocking
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Check if AutoHotkey is installed
where autohotkey >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo AutoHotkey is not installed or not in PATH.
    echo.
    echo Please install AutoHotkey from: https://www.autohotkey.com/download/
    echo After installing, run this batch file again.
    pause
    exit /b 1
)

echo Installing required Python packages...
python -m pip install cryptography pywin32

echo.
echo Setting up password for AutoHotkey...
python prepare_password.py

echo.
echo ===============================================
echo Setup complete!
echo.
echo You can now use the "unlock screen" command with Jarvis
echo or run "run_unlock.bat" to manually unlock your screen.
echo ===============================================
echo.

pause
