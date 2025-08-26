import subprocess
import sys
import os

def install(package):
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
    except Exception as e:
        print(f"✗ Error installing {package}: {e}")

# List of all required packages
packages = [
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
    "flask",               # for web interface
]

def main():
    print("Starting installation of all dependencies for Jarvis Assistant...")
    print("This may take several minutes depending on your internet connection.")
    
    for package in packages:
        install(package)
    
    print("\nAll dependencies installed!")
    print("\nOptional: If you want to use the wake word detection feature, you may also need to install:")
    print("- pocketsphinx (requires Visual C++ build tools)")

if __name__ == "__main__":
    main()
