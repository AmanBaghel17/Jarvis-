
# Quick File Explorer using Tkinter
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def open_file_explorer():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select a file to open")
    if file_path:
        try:
            os.startfile(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

def open_folder_explorer():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a folder to open")
    if folder_path:
        try:
            os.startfile(folder_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")

# Example usage:
if __name__ == "__main__":
    print("1. Open File\n2. Open Folder")
    choice = input("Choose an option (1/2): ")
    if choice == '1':
        open_file_explorer()
    elif choice == '2':
        open_folder_explorer()
    else:
        print("Invalid choice.")
try:
    import cv2
except ImportError:
    cv2 = None
# Gemini API key
gemini_api_key = "Your API KEY"

import os
from openai import OpenAI
import speech_recognition as sr
import webbrowser
import requests
import pyttsx3
import musicLibrary
from gtts import gTTS
import os
import sys
import pygame  # Move import to top
import subprocess
import glob
import random
import urllib.parse
import ctypes
try:
    import win32api
    import win32con
except ImportError:
    win32api = None
    win32con = None
try:
    from screen_brightness_control import set_brightness, get_brightness
except ImportError:
    set_brightness = None
    get_brightness = None
try:
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
except ImportError:
    AudioUtilities = None
    IAudioEndpointVolume = None
import datetime
import threading
import tkinter as tk
from PIL import Image, ImageTk
import base64
import hashlib
from cryptography.fernet import Fernet
import json
import time

# For Gemini (Google Generative AI)
genai = None

# For YouTube Data API (pip install google-api-python-client)
try:
    from googleapiclient.discovery import build
except ImportError:
    build = None

# YouTube Data API key (replace with your own key)
youtube_api_key = "Your Youtube API KEY"

# pip install pocketsphinx

newsapi = "Your News API KEY"
tts_engine = pyttsx3.init()

# Password encryption/decryption functions
def get_encryption_key():
    # Generate a consistent encryption key based on the machine
    machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    # Use SHA-256 to generate a 32-byte key
    key = hashlib.sha256(machine_id.encode()).digest()
    # Properly format for Fernet (must be 32 url-safe base64-encoded bytes)
    return base64.urlsafe_b64encode(key)
    
# Set default screen unlock password (added directly in the code)
DEFAULT_PASSWORD = "asdfghjkl;'"

# Ensure the default password is set on startup
def ensure_default_password():
    try:
        if get_stored_password() is None:
            print("Setting default unlock password...")
            set_stored_password(DEFAULT_PASSWORD)
            return True
        return False
    except Exception as e:
        print(f"Error setting default password: {e}")
        return False

def set_stored_password(password):
    try:
        key = get_encryption_key()
        # Make sure the key is properly formatted
        if len(key) != 44:  # Base64 encoding of 32 bytes is 44 characters
            print("Warning: Key length incorrect, generating fixed key")
            # Use a fixed key as fallback
            test_string = "JarvisAssistant2025"
            key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
        
        cipher_suite = Fernet(key)
        encrypted_pwd = cipher_suite.encrypt(password.encode())
        
        # Store the encrypted password
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        os.makedirs(config_dir, exist_ok=True)
        
        with open(os.path.join(config_dir, 'config.json'), 'w') as f:
            json.dump({'screen_password': encrypted_pwd.decode()}, f)
        
        return True
    except Exception as e:
        print(f"Error setting password: {e}")
        return False

def get_stored_password():
    try:
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        config_file = os.path.join(config_dir, 'config.json')
        
        if not os.path.exists(config_file):
            return None
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        encrypted_pwd = config.get('screen_password')
        if not encrypted_pwd:
            return None
            
        key = get_encryption_key()
        # Make sure the key is properly formatted
        if len(key) != 44:  # Base64 encoding of 32 bytes is 44 characters
            print("Warning: Key length incorrect, generating fixed key")
            # Use a fixed key as fallback
            test_string = "JarvisAssistant2025"
            key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
            
        cipher_suite = Fernet(key)
        decrypted_pwd = cipher_suite.decrypt(encrypted_pwd.encode()).decode()
        
        return decrypted_pwd
    except Exception as e:
        print(f"Error getting password: {e}")
        return None

def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("temp.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")


def aiProcess(command):
    try:
        client = OpenAI(
            api_key="Your OpenAI API KEY",
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google cloud. give short responses."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"AI error: {e}")
        return "I'm having trouble connecting to my AI services right now."

def geminiProcess(command):
    return "Gemini API client is not installed."



apps = {
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
    "paint": r"C:\Windows\System32\mspaint.exe",
    "cmd": r"C:\Windows\System32\cmd.exe",
    "explorer": r"C:\Windows\explorer.exe",
    "microsoft store": "ms-windows-store:",
    "settings": "ms-settings:",
    "photos": "ms-photos:",
    "spotify": os.path.expandvars(r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe"),
    "word": "ms-word:",
    "excel": "ms-excel:",
    "powerpoint": "ms-powerpoint:",
    "onenote": "onenote:",
    "outlook": "outlookmail:",
    "edge": "microsoft-edge:",
    "github desktop": r"C:\Users\%USERNAME%\AppData\Local\GitHubDesktop\GitHubDesktop.exe",
    "coursera": "https://www.coursera.org",           # <-- Add this line
    "tutedude": "https://www.tutedude.com",            # <-- Add this line
    "google drive": "https://drive.google.com",        # <-- Add this line
    # Add more Microsoft app URIs as needed
}

def find_app_shortcut(app_name):
    # Common Start Menu paths
    start_menu_paths = [
        os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs'),
        os.path.expandvars(r'%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs')
    ]
    app_name = app_name.lower()
    for path in start_menu_paths:
        for shortcut in glob.glob(os.path.join(path, '**', '*.lnk'), recursive=True):
            if app_name in os.path.basename(shortcut).lower():
                return shortcut
    return None

def processCommand(c):
    # Lock screen command
    if any(phrase in c.lower() for phrase in ["lock screen", "lock my screen", "lock computer", "lock my computer", "lock pc", "lock my pc"]):
        try:
            # Import necessary Windows API components
            import ctypes
            user32 = ctypes.windll.User32
            speak("Locking your screen now.")
            # Use Windows API to lock the workstation
            user32.LockWorkStation()
            return "Screen locked successfully."
        except Exception as e:
            speak("Sorry, I couldn't lock your screen.")
            return f"Error locking screen: {str(e)}"
            
    # Unlock screen command - with multiple command options
    if any(phrase in c.lower() for phrase in ["aman", "unlock scree", "unlock screen", "unlock my screen", "my comman", "on lock", "open lock"]):
        try:
            # Import necessary modules for simulating input
            import ctypes
            from ctypes import wintypes
            from time import sleep
            import os
            import sys
            import subprocess
            user32 = ctypes.windll.User32
            
            speak("Attempting to unlock your screen.")
            
            # Method 0 (BEST): Advanced unlock method - try this first as it's most reliable
            try:
                print("Trying Advanced Unlock method (most reliable)...")
                advanced_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "advanced_unlock.py")
                if os.path.exists(advanced_script):
                    subprocess.Popen([sys.executable, advanced_script])
                    speak("Using advanced method to unlock your screen.")
                    return "Attempting to unlock your screen with advanced method."
                else:
                    print("Advanced unlock script not found, trying other methods")
            except Exception as adv_error:
                print(f"Advanced method failed: {adv_error}")
                
            # Method 0.5: AutoHotkey method - try this next if installed
            try:
                print("Trying AutoHotkey method...")
                ahk_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ahk_unlock.py")
                if os.path.exists(ahk_script):
                    subprocess.Popen([sys.executable, ahk_script])
                    speak("Using AutoHotkey to unlock your screen.")
                    return "Attempting to unlock your screen with AutoHotkey."
                else:
                    print("AutoHotkey script not found, trying other methods")
            except Exception as ahk_error:
                print(f"AutoHotkey method failed: {ahk_error}")
            
            # First, wake the screen with multiple methods for reliability
            print("Waking screen...")
            # Method 1: Shift key
            user32.keybd_event(0xA0, 0, 0, 0)  # SHIFT key down
            user32.keybd_event(0xA0, 0, 2, 0)  # SHIFT key up
            sleep(0.5)
            # Method 2: Space key
            user32.keybd_event(0x20, 0, 0, 0)  # SPACE key down
            user32.keybd_event(0x20, 0, 2, 0)  # SPACE key up
            sleep(0.5)
            # Method 3: Mouse movement
            try:
                import pyautogui
                pyautogui.moveTo(100, 100, duration=0.2)
                pyautogui.moveTo(200, 200, duration=0.2)
                print("Mouse moved to wake screen")
            except:
                print("Could not use mouse movement")
            
            # Give the screen time to wake up
            sleep(2)
            
            # Check if a password is stored
            print("Getting stored password...")
            password = get_stored_password()
            if not password:
                # Use default password if none is stored
                password = DEFAULT_PASSWORD
                print(f"Using default password: {DEFAULT_PASSWORD}")
            else:
                print("Using stored password")
            
            # Try to type the password using different methods
            print("Attempting to type password...")
            
            # Try multiple methods in sequence for better reliability
            
            # Method 1: SendKeys (most reliable on Windows)
            try:
                print("Trying Enhanced SendKeys method (most reliable)...")
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                
                # First activate the login screen to ensure it has focus
                print("Activating login window...")
                shell.AppActivate("Windows")
                sleep(0.5)
                
                # Clear any existing input first with backspace
                print("Clearing any existing input...")
                for i in range(10):  # Press backspace multiple times to clear any text
                    shell.SendKeys("{BACKSPACE}")
                    sleep(0.1)
                    
                print(f"Typing password: {'*' * len(password)}")
                
                # Type each character with a delay
                for i, char in enumerate(password):
                    # Special handling for special characters that need escaping in SendKeys
                    if char in '+^%~(){}[]':
                        shell.SendKeys('{' + char + '}')
                    else:
                        shell.SendKeys(char)
                    print(f"Typed character {i+1}/{len(password)}")
                    sleep(0.3)  # Slightly longer delay for reliability
                
                # Wait briefly before pressing Enter
                print("Waiting before pressing Enter...")
                sleep(1.0)  # Longer wait before Enter
                
                # Press Enter
                print("Pressing Enter key...")
                shell.SendKeys("{ENTER}")
                
                speak("I've entered your password to unlock the screen.")
                return "Attempting to unlock your screen with Enhanced Windows SendKeys."
            except ImportError:
                print("SendKeys not available, trying PyAutoGUI")
                
            # Method 2: PyAutoGUI
            try:
                print("Trying PyAutoGUI method...")
                import pyautogui
                # Disable failsafe for screen unlock scenario
                pyautogui.FAILSAFE = False
                # Type the password with a longer interval
                pyautogui.typewrite(password, interval=0.2)
                sleep(0.5)
                # Press Enter
                pyautogui.press('enter')
                
                speak("I've entered your password using PyAutoGUI.")
                return "Attempting to unlock your screen with PyAutoGUI."
            except ImportError:
                print("PyAutoGUI not available, trying Windows API method")
                
            # Method 3: Windows API keybd_event
            try:
                print("Trying Windows API method...")
                # Fall back to Windows API method
                for char in password:
                    # Convert character to virtual key code
                    vk = ord(char.upper())
                    user32.keybd_event(vk, 0, 0, 0)  # Key down
                    user32.keybd_event(vk, 0, 2, 0)  # Key up
                    sleep(0.2)  # Longer delay between keys
                
                # Press Enter
                user32.keybd_event(0x0D, 0, 0, 0)  # ENTER key down
                user32.keybd_event(0x0D, 0, 2, 0)  # ENTER key up
                
                speak("I've tried to enter your password using Windows API.")
                return "Attempting to unlock your screen with Windows API."
            except Exception as method_error:
                print(f"All typing methods failed: {method_error}")
                speak("I couldn't type your password with any available method.")
                return "All password typing methods failed."
            except Exception as inner_e:
                speak("I couldn't type your password. You may need to enter it manually.")
                print(f"Error typing password: {str(inner_e)}")
                return f"Error typing password: {str(inner_e)}"
        except Exception as e:
            speak("Sorry, I couldn't unlock your screen.")
            print(f"Error unlocking screen: {str(e)}")
            return f"Error unlocking screen: {str(e)}"
            
    # Set screen password command
    if c.lower().startswith("set screen password") or c.lower().startswith("set my screen password"):
        try:
            # Extract password from command
            password_parts = c.lower().split("to", 1)
            if len(password_parts) < 2:
                speak("Please specify your password by saying 'set screen password to YOUR_PASSWORD'")
                return "Password format incorrect. Use 'set screen password to YOUR_PASSWORD'"
            
            password = password_parts[1].strip()
            if set_stored_password(password):
                speak("Your screen unlock password has been securely stored.")
                return "Password saved successfully."
            else:
                speak("There was an error storing your password.")
                return "Failed to save password."
        except Exception as e:
            speak("Sorry, I couldn't set your screen password.")
            return f"Error setting password: {str(e)}"
            
    # Install PyAutoGUI command
    if c.lower() == "install pyautogui":
        try:
            speak("Installing PyAutoGUI, please wait...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
            speak("PyAutoGUI has been installed successfully.")
            return "PyAutoGUI installed. You can now use the unlock screen feature."
        except Exception as e:
            speak("There was an error installing PyAutoGUI.")
            return f"Error installing PyAutoGUI: {str(e)}"
            
    # Stop or exit command
    if c.strip().lower() in ["stop", "exit", "quit", "goodbye", "bye"]:
        speak("Goodbye!")
        return "Goodbye! Closing the session."
        
    # Generic open app command
    if c.lower().startswith("open ") and not any(x in c.lower() for x in ["google", "whatsapp", "file explorer", "youtube", "facebook", "twitter", "instagram", "github", "linkedin", "gmail", "camera"]):
        app_name = c[5:].strip().lower()
        if app_name in apps:
            try:
                if apps[app_name].startswith("http"):
                    webbrowser.open(apps[app_name])
                else:
                    os.startfile(apps[app_name])
                speak(f"Opening {app_name}")
                return f"Opening {app_name}"
            except Exception as e:
                speak(f"Sorry, I couldn't open {app_name}.")
                print(f"Error opening {app_name}: {e}")
                return f"Failed to open {app_name}: {str(e)}"
        else:
            # Check if the app is in the Start Menu shortcuts
            shortcut = find_app_shortcut(app_name)
            if shortcut:
                try:
                    subprocess.Popen([shortcut])
                    speak(f"Opening {app_name}")
                    return f"Opening {app_name}"
                except Exception as e:
                    speak(f"Sorry, I couldn't open {app_name}.")
                    print(f"Error opening {app_name}: {e}")
                    return f"Failed to open {app_name}: {str(e)}"
            else:
                speak(f"Sorry, I couldn't find {app_name} in your app list.")
                return f"Application '{app_name}' not found"
                
    # Amazon search command
    if c.lower().startswith("search amazon for "):
        query = c[18:].strip()
        url = f"https://www.amazon.in/s?k={urllib.parse.quote(query)}"
        webbrowser.open(url)
        speak(f"Searching Amazon for {query}.")
        return f"Searching Amazon for {query}: <a href='{url}' target='_blank'>{url}</a>"
    # Flipkart search command
    if c.lower().startswith("search flipkart for "):
        query = c[20:].strip()
        url = f"https://www.flipkart.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        speak(f"Searching Flipkart for {query}.")
        return f"Searching Flipkart for {query}: <a href='{url}' target='_blank'>{url}</a>"
    # Search this to Chrome command
    if c.lower().startswith("search this to chrome"):
        query = c[21:].strip()
        if not query:
            speak("Please specify what you want to search in Chrome.")
            return
        # Try to find Chrome path
        chrome_paths = [
            r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        chrome_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_path = path
                break
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        if chrome_path:
            try:
                subprocess.Popen([chrome_path, url])
                speak(f"Searching {query} in Chrome.")
            except Exception:
                webbrowser.open(url)
                speak(f"Searching {query} in your default browser.")
        else:
            webbrowser.open(url)
            speak(f"Searching {query} in your default browser.")
        return
    # Click photo command
    if c.lower().startswith("click photo"):
        if cv2 is None:
            speak("OpenCV is not installed.")
            return
        speak("Say cheese! Capturing photo.")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            speak("Could not open camera.")
            return
        ret, frame = cap.read()
        if ret:
            filename = f"photo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(filename, frame)
            speak(f"Photo clicked and saved as {filename}.")
        else:
            speak("Failed to capture photo.")
        cap.release()
        return
    # Open camera command
    if c.lower().startswith("open camera"):
        if cv2 is None:
            speak("OpenCV is not installed.")
            return
        speak("Opening camera.")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            speak("Could not open camera.")
            return
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Camera - Press Q to close', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        return
    # Gemini (Google Generative AI) command
    if c.lower().startswith("gemini "):
        prompt = c[7:].strip()
        response = geminiProcess(prompt)
        speak(response)
        return
    # YouTube search command
    if c.lower().startswith("search youtube for "):
        query = c[18:].strip()
        return search_youtube_and_play(query)
    if c.lower().startswith("youtube "):
        query = c[8:].strip()
        return search_youtube_and_play(query)
    # Volume control
    if "volume up" in c.lower() or "increase volume" in c.lower():
        if AudioUtilities and IAudioEndpointVolume:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
            speak("Volume increased.")
        else:
            speak("Volume control is not available. Please install pycaw.")
        return
    if "volume down" in c.lower() or "decrease volume" in c.lower():
        if AudioUtilities and IAudioEndpointVolume:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
            speak("Volume decreased.")
        else:
            speak("Volume control is not available. Please install pycaw.")
        return
    if "mute" in c.lower():
        if AudioUtilities and IAudioEndpointVolume:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)
            speak("Volume muted.")
        else:
            speak("Mute is not available. Please install pycaw.")
        return
    if "unmute" in c.lower():
        if AudioUtilities and IAudioEndpointVolume:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            volume.SetMute(0, None)
            speak("Volume unmuted.")
        else:
            speak("Unmute is not available. Please install pycaw.")
        return
    # Brightness control
    if "brightness up" in c.lower() or "increase brightness" in c.lower():
        if set_brightness and get_brightness:
            try:
                current = get_brightness()[0]
                set_brightness(min(current + 10, 100))
                speak("Brightness increased.")
            except Exception:
                speak("Could not change brightness.")
        else:
            speak("Brightness control is not available. Please install screen-brightness-control.")
        return
    if "brightness down" in c.lower() or "decrease brightness" in c.lower():
        if set_brightness and get_brightness:
            try:
                current = get_brightness()[0]
                set_brightness(max(current - 10, 0))
                speak("Brightness decreased.")
            except Exception:
                speak("Could not change brightness.")
        else:
            speak("Brightness control is not available. Please install screen-brightness-control.")
        return
    if "date" in c.lower() or "time" in c.lower():
        now = datetime.datetime.now()
        date_str = now.strftime('%A, %d %B %Y')
        time_str = now.strftime('%I:%M %p')
        if "date" in c.lower() and "time" in c.lower():
            speak(f"Today is {date_str} and the time is {time_str}.")
            return
        elif "date" in c.lower():
            speak(f"Today's date is {date_str}.")
            return
        elif "time" in c.lower():
            speak(f"The time is {time_str}.")
            return
    if "stop song" in c.lower() or "stop music" in c.lower():
        try:
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                speak("Stopped the song.")
            else:
                speak("No song is currently playing.")
        except Exception as e:
            speak("Sorry, I couldn't stop the song.")
            print(f"Error stopping song: {e}")
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp Web")
    elif "open file explorer" in c.lower():
        try:
            os.startfile(os.path.expandvars(r"%SystemRoot%\explorer.exe"))
            speak("Opening File Explorer")
        except Exception as e:
            speak("Sorry, I couldn't open File Explorer.")
            print(f"Error opening File Explorer: {e}")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook")
    elif "open twitter" in c.lower():
        webbrowser.open("https://www.twitter.com")
        speak("Opening Twitter")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram")
    elif "open github" in c.lower():
        webbrowser.open("https://www.github.com")
        speak("Opening GitHub")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
        speak("Opening LinkedIn")
    elif "open gmail" in c.lower():
        webbrowser.open("https://www.gmail.com")
        speak("Opening Gmail")
    elif c.lower().startswith("play"):
        
        # Try to find the song name anywhere in the command
        song = None
        for key in musicLibrary.music.keys():
            if key in c.lower():
                song = key
                break
        if song:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak("Sorry, I couldn't find that song in your music library.")
    elif "news" in c.lower():
        # Change country to 'us' and use your API key
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                speak("Here are the top news headlines.")
                for article in articles[:3]:
                    title = article.get("title")
                    if title:
                        speak(title)
            else:
                speak("Sorry, I couldn't find any news headlines.")
        else:
            speak("Sorry, I couldn't fetch the news right now.")
    # (Removed stray elif and nested function definition that caused syntax error)
    if "play random song on youtube" in c.lower():
        # List of random song search queries or URLs
        random_songs = [
            "https://www.youtube.com/watch?v=3JZ4pnNtyxQ",  # Example: Alan Walker - Faded
            "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Example: Luis Fonsi - Despacito
            "https://www.youtube.com/watch?v=2Vv-BfVoq4g",  # Example: Ed Sheeran - Perfect
            "https://www.youtube.com/watch?v=RgKAFK5djSk",  # Example: Wiz Khalifa - See You Again
            "https://www.youtube.com/watch?v=JGwWNGJdvx8",  # Example: Ed Sheeran - Shape of You
            # Add more song URLs as you like
        ]
        song_url = random.choice(random_songs)
        webbrowser.open(song_url)
        speak("Playing a random song on YouTube")
    elif "send message to" in c.lower() and "on whatsapp" in c.lower():
        try:
            # Example command: "send message to 919876543210 on whatsapp"
            parts = c.lower().split("send message to")[1].split("on whatsapp")[0].strip()
            # You can enhance this to extract both number and message
            number = ''.join(filter(str.isdigit, parts))
            message = "Hello from Jarvis!"  # Default message, or extract from command
            url = f"https://wa.me/{number}?text={urllib.parse.quote(message)}"
            webbrowser.open(url)
            speak(f"Opening WhatsApp chat with {number}")
        except Exception as e:
            speak("Sorry, I couldn't process the WhatsApp message.")
            print(f"Error sending WhatsApp message: {e}")
    # Thank you handler
    elif any(phrase in c.lower() for phrase in ["thank you", "thanks", "thank"]):
        responses = ["You're welcome!", "Happy to help!", "Anytime!", "My pleasure!", "No problem!", "Glad I could help!"]
        response = random.choice(responses)
        speak(response)
        return response
    else:
        response = aiProcess(c)
        speak(response)

def start_assistant():
    speak("Initializing Jarvis.....")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                print(f"Recognized word: {word}")
                if word.lower() == "jarvis":
                    speak("Yes Boss")
                    break
            except Exception as e:
                print(f"error: {e}")

    # Now continuously listen for commands
    while True:
        try:
            print("Listening for command...")
            with sr.Microphone() as source:
                # Adjust for ambient noise to improve recognition
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Increase the energy threshold to detect speech better
                recognizer.energy_threshold = 4000
                # Increase phrase_time_limit for longer commands
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio)
                print(f"Recognized command: {command}")
                if command.strip().lower() == "stop":
                    speak("Goodbye!")
                    break
                
                # Special handling for unlock commands
                if "unlock" in command.lower() or "wake" in command.lower():
                    print("Potential unlock command detected")
                
                processCommand(command)
        except Exception as e:
            print(f"error: {e}")



def launch_interface():
    root = tk.Tk()
    root.title("Jarvis Assistant")
    root.geometry("400x400")
    root.resizable(False, False)

    # Load and set Earth background
    try:
        earth_img = Image.open("earth.jpg")
        earth_img = earth_img.resize((400, 400), Image.ANTIALIAS)
        bg_img = ImageTk.PhotoImage(earth_img)
        bg_label = tk.Label(root, image=bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        bg_label = tk.Label(root, bg="#000000")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Overlay frame for widgets (transparent background)
    overlay = tk.Frame(root, bg='#000000', bd=0)
    overlay.place(relx=0.5, rely=0.5, anchor='center')

    label = tk.Label(overlay, text="🌍 Welcome to Jarvis! 🌍", font=("Arial", 18, "bold"), fg="#00ffea", bg="#000000")
    label.pack(pady=(30, 20))

    def on_start():
        root.destroy()
        threading.Thread(target=start_assistant).start()

    start_btn = tk.Button(overlay, text="Start Listening", font=("Arial", 14, "bold"), fg="#ffffff", bg="#1a237e", activebackground="#3949ab", activeforeground="#00ffea", command=on_start, width=18, height=2, bd=0, relief='ridge')
    start_btn.pack(pady=10)

    exit_btn = tk.Button(overlay, text="Exit", font=("Arial", 12), fg="#ffffff", bg="#b71c1c", activebackground="#e53935", command=root.destroy, width=18, height=1, bd=0, relief='ridge')
    exit_btn.pack(pady=5)

    root.mainloop()


def search_youtube_and_play(query):
    if build is None:
        return "YouTube API client is not installed."
    try:
        youtube = build("youtube", "v3", developerKey=youtube_api_key)
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=1
        )
        response = request.execute()
        items = response.get("items", [])
        if items:
            video_id = items[0]["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            webbrowser.open(url)
            speak(f"Playing {query} on YouTube.")
            return f"Playing {query} on YouTube: <a href='{url}' target='_blank'>{url}</a>"
        else:
            speak("No results found on YouTube.")
            return "No results found on YouTube."
    except Exception as e:
        speak("There was an error searching YouTube.")
        return f"YouTube search error: {e}"


def list_gemini_models():
    print("Gemini API client is not installed.")
    return


def setup_autohotkey_unlock():
    """Set up the AutoHotkey unlock feature"""
    import os
    import sys
    import subprocess
    
    try:
        # Check if AutoHotkey integration files exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        files_needed = [
            "unlock_screen.ahk",
            "run_unlock.bat",
            "prepare_password.py",
            "ahk_unlock.py"
        ]
        
        missing_files = []
        for file in files_needed:
            if not os.path.exists(os.path.join(script_dir, file)):
                missing_files.append(file)
        
        if missing_files:
            print(f"Missing AutoHotkey integration files: {', '.join(missing_files)}")
            print("Please ensure all files are present for screen unlock functionality.")
            return False
            
        # Create the required directories
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        os.makedirs(config_dir, exist_ok=True)
        
        # Try to pre-generate the plain password file
        try:
            subprocess.run([sys.executable, os.path.join(script_dir, "prepare_password.py")])
            print("Password prepared for AutoHotkey unlock")
        except Exception as e:
            print(f"Warning: Could not prepare password for AutoHotkey: {e}")
        
        print("AutoHotkey screen unlock module setup completed!")
        return True
        
    except Exception as e:
        print(f"Error setting up AutoHotkey screen unlock module: {e}")
        return False

if __name__ == "__main__":
    # Ensure default password is set
    ensure_default_password()
    
    # Set up AutoHotkey unlock feature
    setup_autohotkey_unlock()
    
    # Launch the interface
    launch_interface()
