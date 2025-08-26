"""
Direct Screen Unlock Utility
----------------------------
This script attempts to unlock a Windows screen by typing a stored password.
"""

import pyautogui
import time
import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet

# Disable PyAutoGUI failsafe - this prevents errors when mouse moves to screen corner
# Note: This is normally not recommended, but is necessary for screen unlock scenarios
pyautogui.FAILSAFE = False

# Default password if no stored password is found
DEFAULT_PASSWORD = "asdfghjkl;'"

def get_stored_password():
    """Retrieves the stored password or returns the default password if not found"""
    try:
        # Fixed encryption key for consistent decryption
        key = base64.urlsafe_b64encode(hashlib.sha256("JarvisAssistant2025".encode()).digest())
        
        # Check for stored password
        config_path = os.path.join(os.path.expanduser('~'), '.jarvis', 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            encrypted_pwd = config.get('screen_password')
            if encrypted_pwd:
                cipher = Fernet(key)
                password = cipher.decrypt(encrypted_pwd.encode()).decode()
                print("✓ Found stored password")
                return password
    
        print("! No stored password found, using default")
        return DEFAULT_PASSWORD
    except Exception as e:
        print(f"! Error retrieving password: {e}")
        return DEFAULT_PASSWORD

def unlock_screen():
    """Performs the screen unlock sequence"""
    try:
        print("\nStarting unlock sequence...")
        password = get_stored_password()
        
        # Wake screen with mouse movement
        print("1. Moving mouse to wake screen...")
        pyautogui.moveTo(100, 100, duration=0.2)
        pyautogui.moveTo(200, 200, duration=0.2)
        time.sleep(1)
        
        # Type password with delay between keys
        print("2. Typing password...")
        pyautogui.typewrite(password, interval=0.15)
        time.sleep(0.5)
        
        # Press Enter
        print("3. Pressing Enter...")
        pyautogui.press('enter')
        
        print("\n✓ Unlock sequence completed!")
        return True
    except Exception as e:
        print(f"\n✗ Error during unlock: {e}")
        return False

if __name__ == "__main__":
    print("=== SCREEN UNLOCK UTILITY ===")
    unlock_screen()
    
    print("\nPress Enter to exit...")
    input()
