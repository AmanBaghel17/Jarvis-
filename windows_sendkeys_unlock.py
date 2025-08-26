"""
Windows SendKeys Screen Unlock Utility
-------------------------------------
This script uses SendKeys, a Windows-specific method to unlock the screen
that may be more reliable than PyAutoGUI.
"""

import time
import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet
import win32com.client
import ctypes
from ctypes import wintypes

# Default password (backup if stored password can't be retrieved)
DEFAULT_PASSWORD = "asdfghjkl;'"

def get_encryption_key():
    # Use a fixed key that we know works
    test_string = "JarvisAssistant2025"
    key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
    return key

def get_stored_password():
    """Retrieves the stored password or returns the default password if not found"""
    try:
        # Fixed encryption key for consistent decryption
        key = get_encryption_key()
        
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

def unlock_screen_with_sendkeys():
    """Performs the screen unlock sequence using Windows SendKeys"""
    try:
        print("\nStarting unlock sequence with SendKeys...")
        password = get_stored_password()
        
        # Wake the screen first with Windows API
        print("1. Waking the screen...")
        user32 = ctypes.windll.User32
        
        # Press and release multiple keys to ensure screen wakes
        user32.keybd_event(0xA0, 0, 0, 0)  # SHIFT key down
        user32.keybd_event(0xA0, 0, 2, 0)  # SHIFT key up
        time.sleep(0.5)
        
        user32.keybd_event(0x20, 0, 0, 0)  # SPACE key down
        user32.keybd_event(0x20, 0, 2, 0)  # SPACE key up
        time.sleep(0.5)
        
        # Wait for screen to wake up
        time.sleep(2)
        
        # Use SendKeys for more reliable keyboard input
        print("2. Using SendKeys to type password...")
        shell = win32com.client.Dispatch("WScript.Shell")
        
        # Type each character with a delay
        for char in password:
            shell.SendKeys(char)
            time.sleep(0.2)
        
        # Wait briefly before pressing Enter
        time.sleep(0.5)
        
        # Press Enter
        print("3. Pressing Enter...")
        shell.SendKeys("{ENTER}")
        
        print("\n✓ Unlock sequence completed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error during unlock: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== WINDOWS SENDKEYS UNLOCK UTILITY ===")
    print("This utility uses Windows-specific SendKeys to")
    print("unlock your screen, which may be more reliable.")
    print()
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        result = unlock_screen_with_sendkeys()
        
        if result:
            print("\nUnlock attempt completed successfully!")
        else:
            print("\nUnlock attempt encountered errors.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    
    print("\nPress Enter to exit...")
    input()
