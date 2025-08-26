import pyautogui
import time
import os
import sys
import json
import base64
import hashlib
from cryptography.fernet import Fernet

# Disable PyAutoGUI failsafe - necessary for screen unlock functionality
pyautogui.FAILSAFE = False

# Default password (backup if stored password can't be retrieved)
DEFAULT_PASSWORD = "asdfghjkl;'"

def get_encryption_key():
    # Use a fixed key that we know works
    test_string = "JarvisAssistant2025"
    key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
    return key

def get_stored_password():
    try:
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        config_file = os.path.join(config_dir, 'config.json')
        
        if not os.path.exists(config_file):
            print("Config file not found, using default password")
            return DEFAULT_PASSWORD
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        encrypted_pwd = config.get('screen_password')
        if not encrypted_pwd:
            print("No password in config, using default password")
            return DEFAULT_PASSWORD
            
        key = get_encryption_key()
        cipher_suite = Fernet(key)
        decrypted_pwd = cipher_suite.decrypt(encrypted_pwd.encode()).decode()
        
        return decrypted_pwd
    except Exception as e:
        print(f"Error getting password: {e}")
        print("Using default password as fallback")
        return DEFAULT_PASSWORD

def unlock_screen():
    try:
        print("Starting screen unlock...")
        
        # Get the password
        password = get_stored_password()
        print(f"Retrieved password (first character): {password[0]}***")
        
        # Wake the screen with mouse movement
        print("Moving mouse to wake screen...")
        pyautogui.moveTo(100, 100, duration=0.25)
        pyautogui.moveTo(200, 100, duration=0.25)
        pyautogui.moveTo(100, 200, duration=0.25)
        
        # Give the screen time to wake up
        print("Waiting for screen to wake up...")
        time.sleep(2)
        
        # Type the password
        print("Typing password...")
        pyautogui.typewrite(password, interval=0.2)
        time.sleep(0.5)
        
        # Press Enter
        print("Pressing Enter...")
        pyautogui.press('enter')
        
        print("Unlock attempt completed!")
        return True
    except Exception as e:
        print(f"Error during unlock: {e}")
        if hasattr(e, '__traceback__'):
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)
        return False

if __name__ == "__main__":
    print("Aman - Direct Screen Unlock Utility")
    print("--------------------------")
    print("This script will attempt to unlock your screen by:")
    print("1. Moving the mouse to wake the screen")
    print("2. Typing your stored password")
    print("3. Pressing Enter")
    print()
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    result = unlock_screen()
    
    if result:
        print("\nUnlock attempt completed successfully!")
    else:
        print("\nUnlock attempt encountered errors.")
        
    print("\nPress Enter to exit...")
    input()
