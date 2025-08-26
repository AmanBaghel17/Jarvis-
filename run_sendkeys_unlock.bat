@echo off
echo ===============================================
echo Enhanced SendKeys Screen Unlock Utility
echo ===============================================
echo.
echo This utility focuses specifically on the SendKeys method,
echo which is often the most reliable way to unlock Windows screens.
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

python "%~dp0enhanced_sendkeys_unlock.py"

echo.
echo ===============================================
echo If your screen did not unlock, try these alternatives:
echo.
echo 1. Run master_unlock.bat to try all available methods
echo 2. Check your password with test_password_system.py
echo 3. Try setting a simpler password with:
echo    "set screen password to simple123"
echo ===============================================
echo.
pause
