@echo off
echo Setting screen unlock password...

python -c "import main; main.set_stored_password('asdfghjkl;\'')"

echo Password set successfully!
echo.
echo You can now use the "unlock screen" command with Jarvis.
pause
