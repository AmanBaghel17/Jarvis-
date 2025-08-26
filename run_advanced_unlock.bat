@echo off
echo ===============================================
echo Jarvis Advanced Screen Unlock Utility
echo ===============================================
echo.
echo This utility uses low-level Windows APIs to type
echo your password on the lock screen.
echo.
echo Instructions:
echo 1. Lock your screen (Win+L)
echo 2. Run this batch file
echo 3. Switch back to the lock screen within 3 seconds
echo.
echo Press any key to continue...
pause >nul

echo.
echo Starting unlock process in 3 seconds...
echo SWITCH TO YOUR LOCK SCREEN NOW!
timeout /t 3 >nul

python "%~dp0advanced_unlock.py"

echo.
echo If your screen did not unlock, please try the following:
echo 1. Make sure your password is set correctly
echo 2. Run test_password_system.py to verify your password
echo.
pause
