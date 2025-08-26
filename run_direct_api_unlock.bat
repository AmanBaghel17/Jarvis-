@echo off
echo ===============================================
echo Direct Windows API Screen Unlock Utility
echo ===============================================
echo.
echo This utility uses direct Windows API calls to type 
echo your password on the lock screen.
echo.
echo Instructions:
echo 1. Lock your screen (Win+L)
echo 2. Run this batch file
echo 3. Switch back to the lock screen within 5 seconds
echo.
echo Press any key to begin...
pause >nul

echo.
echo Starting in 5 seconds...
echo SWITCH TO YOUR LOCK SCREEN NOW!
echo.
timeout /t 5 >nul

python "%~dp0direct_api_unlock.py"

echo.
echo ===============================================
echo If your screen did not unlock, try:
echo.
echo 1. Setting a simple password: set_simple_password.bat
echo 2. Try our other unlock methods: master_unlock.bat
echo ===============================================
echo.
pause
