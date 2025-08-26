@echo off
echo ===========================================
echo Simple Screen Unlock Utility
echo ===========================================
echo.
echo This utility will attempt to unlock your Windows screen
echo using your stored password.
echo.
echo 1. Make sure you've set your password with Jarvis
echo 2. Lock your screen (Win+L)
echo 3. Run this batch file
echo.
echo Press any key to begin unlock sequence...
pause >nul

echo.
echo Starting unlock process in 3 seconds...
echo Switch to your lock screen now!
timeout /t 3 >nul

python "%~dp0simple_unlock.py"

echo.
echo ===========================================
echo If your screen did not unlock, try these solutions:
echo.
echo 1. Install AutoHotkey from https://www.autohotkey.com/
echo 2. Run setup_autohotkey_unlock.bat
echo 3. Try again with "run_unlock.bat"
echo ===========================================
echo.
pause
