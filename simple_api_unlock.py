"""
Simple Direct Windows API Screen Unlock
--------------------------------------
This script uses the most basic Windows API approach
without any dependencies except ctypes (built into Python).
"""

import ctypes
import time
import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet

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

def unlock_with_windows_api():
    """Performs the screen unlock sequence using only Windows API"""
    try:
        print("\nStarting unlock sequence with Windows API...")
        password = get_stored_password()
        
        # Get Windows API functions
        user32 = ctypes.windll.User32
        
        # Wake the screen
        print("1. Waking the screen...")
        # Method 1: Shift key
        user32.keybd_event(0xA0, 0, 0, 0)  # SHIFT key down
        user32.keybd_event(0xA0, 0, 2, 0)  # SHIFT key up
        time.sleep(0.5)
        
        # Method 2: Alt key
        user32.keybd_event(0x12, 0, 0, 0)  # ALT key down
        user32.keybd_event(0x12, 0, 2, 0)  # ALT key up
        time.sleep(0.5)
        
        # Wait for screen to wake up
        print("Waiting for screen to wake up...")
        time.sleep(2)
        
        # Type the password using keybd_event
        print("2. Typing password with Windows API...")
        for char in password:
            try:
                # Convert character to virtual key code
                # This handles special characters better
                vk = ctypes.windll.user32.VkKeyScanA(ord(char)) & 0xFF
                
                # Press and release the key
                user32.keybd_event(vk, 0, 0, 0)  # Key down
                time.sleep(0.1)
                user32.keybd_event(vk, 0, 2, 0)  # Key up
                time.sleep(0.2)  # Longer delay between keys
            except Exception as e:
                print(f"Error with character '{char}': {e}")
        
        # Wait briefly before pressing Enter
        time.sleep(1)
        
        # Press Enter
        print("3. Pressing Enter...")
        user32.keybd_event(0x0D, 0, 0, 0)  # ENTER key down
        time.sleep(0.1)
        user32.keybd_event(0x0D, 0, 2, 0)  # ENTER key up
        
        print("\n✓ Unlock sequence completed!")
        return True
    except Exception as e:
        print(f"\n✗ Error during unlock: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== SIMPLE WINDOWS API UNLOCK UTILITY ===")
    print("This utility uses only Windows API functions")
    print("without any extra dependencies.")
    print()
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        result = unlock_with_windows_api()
        
        if result:
            print("\nUnlock attempt completed successfully!")
        else:
            print("\nUnlock attempt encountered errors.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    
    print("\nPress Enter to exit...")
    input()
