# Install pip first
Write-Host "Installing pip..." -ForegroundColor Cyan
Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
python get-pip.py

# Install all dependencies
Write-Host "`nInstalling all dependencies for Jarvis Assistant..." -ForegroundColor Green

$packages = @(
    "opencv-python",
    "openai",
    "SpeechRecognition",
    "requests",
    "pyttsx3",
    "gTTS",
    "pygame",
    "pywin32",
    "screen-brightness-control",
    "comtypes",
    "pycaw",
    "pillow",
    "pyautogui",
    "google-api-python-client",
    "cryptography",
    "flask"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Yellow
    try {
        python -m pip install $package
        Write-Host "Successfully installed $package" -ForegroundColor Green
    } catch {
        Write-Host "Error installing $package" -ForegroundColor Red
    }
}

Write-Host "`nAll dependencies installed!" -ForegroundColor Cyan
Write-Host "`nOptional: If you want to use the wake word detection feature, you may also need to install:" -ForegroundColor Magenta
Write-Host "- pocketsphinx (requires Visual C++ build tools)" -ForegroundColor Magenta

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
