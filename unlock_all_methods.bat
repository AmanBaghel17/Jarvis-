@echo off
echo ================================================
echo          SCREEN UNLOCK - ALL METHODS
echo ================================================
echo.
echo This utility will try ALL available unlock methods
echo in sequence until one works.
echo.
echo Methods that will be attempted:
echo 1. Windows SendKeys (most reliable)
echo 2. Clipboard Paste (works well with most keyboards)
echo 3. Simple Windows API (works without dependencies)
echo 4. PyAutoGUI (if installed)
echo.
echo Press any key to begin the unlock process...
pause > nul

echo.
echo Trying Method 1: Windows SendKeys...
python "c:\Shukla Ji\windows_sendkeys_unlock.py"

echo.
echo If that didn't work, trying Method 2: Clipboard Paste...
python "c:\Shukla Ji\clipboard_unlock.py"

echo.
echo If that didn't work, trying Method 3: Simple Windows API...
python "c:\Shukla Ji\simple_api_unlock.py"

echo.
echo If that didn't work, trying Method 4: PyAutoGUI...
python "c:\Shukla Ji\easy_unlock.py"

echo.
echo All methods have been attempted.
echo.
pause
