@echo off
echo Installing pip and dependencies...
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install opencv-python openai SpeechRecognition requests pyttsx3 gTTS pygame pywin32 screen-brightness-control comtypes pycaw pillow pyautogui google-api-python-client cryptography flask
echo.
echo Installation complete!
pause
