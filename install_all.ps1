# Install pip first
Write-Host "Installing pip..." -ForegroundColor Cyan
Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
python get-pip.py

# Install all dependencies
Write-Host "`nInstalling all dependencies for Jarvis Assistant..." -ForegroundColor Green

$packages = @(
    "opencv-python",       # for cv2
    "openai",              # for OpenAI API
    "SpeechRecognition",   # for speech recognition
    "requests",            # for API calls
    "pyttsx3",             # for text to speech
    "gTTS",                # Google Text to Speech
    "pygame",              # for audio playback
    "pywin32",             # for Windows API access
    "screen-brightness-control",  # for brightness control
    "comtypes",            # for audio control
    "pycaw",               # for volume control
    "pillow",              # for PIL/Image handling
    "pyautogui",           # for keyboard simulation
    "google-api-python-client",  # for YouTube API
    "cryptography",        # for password encryption
    "flask"                # for web interface
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Yellow
    try {
        python -m pip install $package
        Write-Host "✓ Successfully installed $package" -ForegroundColor Green
    } catch {
        Write-Host "✗ Error installing $package: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nAll dependencies installed!" -ForegroundColor Cyan
Write-Host "`nOptional: If you want to use the wake word detection feature, you may also need to install:" -ForegroundColor Magenta
Write-Host "- pocketsphinx (requires Visual C++ build tools)" -ForegroundColor Magenta

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
