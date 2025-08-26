@echo off
echo This batch file will help unlock your screen using AutoHotkey
echo.
echo First, we need to ensure AutoHotkey is installed...
echo.

REM Check if AutoHotkey is installed
where /q autohotkey.exe
if %ERRORLEVEL% NEQ 0 (
    echo AutoHotkey is not installed or not in PATH.
    echo.
    echo Please install AutoHotkey from: https://www.autohotkey.com/download/
    echo After installing, run this batch file again.
    pause
    exit /b 1
)

echo AutoHotkey is installed!
echo.
echo Running the unlock script...
echo.

REM Run the AutoHotkey script
start "" "autohotkey.exe" "%~dp0unlock_screen.ahk"

exit /b 0
