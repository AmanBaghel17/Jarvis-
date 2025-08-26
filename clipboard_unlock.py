"""
Clipboard Password Screen Unlock Utility
--------------------------------------
This script copies the password to clipboard and pastes it
into the password field on the login screen.
"""

import ctypes
import time
import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet
import subprocess
import sys

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

def copy_to_clipboard(text):
    """Copy text to clipboard using subprocess"""
    # Windows only
    cmd = 'echo ' + text.strip() + '| clip'
    return subprocess.check_call(cmd, shell=True)

def unlock_with_clipboard():
    """Performs the screen unlock sequence using clipboard paste"""
    try:
        print("\nStarting unlock sequence with clipboard paste...")
        password = get_stored_password()
        
        # Copy password to clipboard
        print("1. Copying password to clipboard...")
        copy_to_clipboard(password)
        
        # Get Windows API functions
        user32 = ctypes.windll.User32
        
        # Wake the screen
        print("2. Waking the screen...")
        user32.keybd_event(0xA0, 0, 0, 0)  # SHIFT key down
        user32.keybd_event(0xA0, 0, 2, 0)  # SHIFT key up
        time.sleep(1)
        
        # Wait for screen to wake up
        time.sleep(2)
        
        # Paste the password using Ctrl+V
        print("3. Pasting password from clipboard...")
        # Press Ctrl+V
        user32.keybd_event(0x11, 0, 0, 0)  # CTRL down
        user32.keybd_event(0x56, 0, 0, 0)  # V down
        time.sleep(0.1)
        user32.keybd_event(0x56, 0, 2, 0)  # V up
        user32.keybd_event(0x11, 0, 2, 0)  # CTRL up
        
        time.sleep(1)
        
        # Press Enter
        print("4. Pressing Enter...")
        user32.keybd_event(0x0D, 0, 0, 0)  # ENTER down
        time.sleep(0.1)
        user32.keybd_event(0x0D, 0, 2, 0)  # ENTER up
        
        # Clear clipboard for security
        time.sleep(1)
        print("5. Clearing clipboard for security...")
        copy_to_clipboard(" ")
        
        print("\n✓ Unlock sequence completed!")
        return True
    except Exception as e:
        print(f"\n✗ Error during unlock: {e}")
        import traceback
        traceback.print_exc()
        # Make sure we clear the clipboard even if there's an error
        try:
            copy_to_clipboard(" ")
        except:
            pass
        return False

if __name__ == "__main__":
    print("=== CLIPBOARD PASTE UNLOCK UTILITY ===")
    print("This utility copies your password to clipboard")
    print("and pastes it into the password field.")
    print()
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        result = unlock_with_clipboard()
        
        if result:
            print("\nUnlock attempt completed successfully!")
        else:
            print("\nUnlock attempt encountered errors.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        # Clear clipboard if cancelled
        try:
            copy_to_clipboard(" ")
        except:
            pass
    
    print("\nPress Enter to exit...")
    input()
