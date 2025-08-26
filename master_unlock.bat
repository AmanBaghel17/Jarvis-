@echo off
echo ===============================================
echo Jarvis Master Unlock Utility
echo ===============================================
echo.
echo This utility will try ALL available screen unlock methods:
echo 1. Enhanced SendKeys method (MOST RELIABLE)
echo 2. Direct Windows API method
echo 3. Advanced Windows API method 
echo 4. AutoHotkey method (if installed)
echo 5. PyAutoGUI method
echo 6. Clipboard method
echo.
echo Instructions:
echo 1. Lock your screen (Win+L)
echo 2. Run this batch file
echo 3. Switch back to the lock screen within 5 seconds
echo.
echo Press any key to start the unlock process...
pause >nul

echo.
echo *** IMPORTANT: Switch to your lock screen NOW! ***
echo Starting unlock sequence in 5 seconds...
timeout /t 5 >nul

echo.
echo === ATTEMPTING UNLOCK METHOD 1: Enhanced SendKeys (MOST RELIABLE) ===
python "%~dp0enhanced_sendkeys_unlock.py"

echo.
echo === ATTEMPTING UNLOCK METHOD 2: Direct Windows API ===
python "%~dp0direct_api_unlock.py"

echo.
echo === ATTEMPTING UNLOCK METHOD 3: Advanced Windows API ===
python "%~dp0advanced_unlock.py"

echo.
echo === ATTEMPTING UNLOCK METHOD 4: AutoHotkey (if installed) ===
if exist "%~dp0unlock_screen.ahk" (
    where /q autohotkey.exe
    if %ERRORLEVEL% EQU 0 (
        start "" autohotkey.exe "%~dp0unlock_screen.ahk"
    ) else (
        echo AutoHotkey not installed. Skipping this method.
    )
) else (
    echo AutoHotkey script not found. Skipping this method.
)

echo.
echo === ATTEMPTING UNLOCK METHOD 5: Simple Unlock ===
python "%~dp0simple_unlock.py"

echo.
echo ===============================================
echo All unlock methods have been attempted!
echo Your screen should now be unlocked.
echo.
echo If your screen is still locked, please check your password
echo by running "python test_password_system.py"
echo ===============================================
echo.
pause
