"""
Physical Keyboard Simulator for Screen Unlock
--------------------------------------------
This script uses direct keyboard hardware simulation via Windows API 
at the lowest level possible to overcome typing issues on lock screens.
"""

import ctypes
import time
import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet

# Import SendInput function and input_type
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Define constants
INPUT_KEYBOARD = 1
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

# Define input structure
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT_union(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("padding", ctypes.c_ubyte * 8)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", INPUT_union)
    ]

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

def wake_screen():
    """Wake the screen using multiple key presses"""
    print("Waking screen with multiple methods...")
    
    # Method 1: Shift key
    input_shift_down = INPUT(type=INPUT_KEYBOARD, 
                         ii=INPUT_union(ki=KEYBDINPUT(wVk=0xA0, wScan=0, 
                                               dwFlags=KEYEVENTF_KEYDOWN, 
                                               time=0, dwExtraInfo=None)))
    input_shift_up = INPUT(type=INPUT_KEYBOARD, 
                       ii=INPUT_union(ki=KEYBDINPUT(wVk=0xA0, wScan=0, 
                                             dwFlags=KEYEVENTF_KEYUP, 
                                             time=0, dwExtraInfo=None)))
    
    user32.SendInput(1, ctypes.byref(input_shift_down), ctypes.sizeof(INPUT))
    time.sleep(0.1)
    user32.SendInput(1, ctypes.byref(input_shift_up), ctypes.sizeof(INPUT))
    time.sleep(0.5)
    
    # Method 2: Space key
    input_space_down = INPUT(type=INPUT_KEYBOARD, 
                         ii=INPUT_union(ki=KEYBDINPUT(wVk=0x20, wScan=0, 
                                               dwFlags=KEYEVENTF_KEYDOWN, 
                                               time=0, dwExtraInfo=None)))
    input_space_up = INPUT(type=INPUT_KEYBOARD, 
                       ii=INPUT_union(ki=KEYBDINPUT(wVk=0x20, wScan=0, 
                                             dwFlags=KEYEVENTF_KEYUP, 
                                             time=0, dwExtraInfo=None)))
    
    user32.SendInput(1, ctypes.byref(input_space_down), ctypes.sizeof(INPUT))
    time.sleep(0.1)
    user32.SendInput(1, ctypes.byref(input_space_up), ctypes.sizeof(INPUT))
    
    # Wait for screen to wake up
    print("Waiting for screen to wake up...")
    time.sleep(2)

def type_key(key_code):
    """Type a single key using SendInput"""
    # Key down
    input_down = INPUT(type=INPUT_KEYBOARD, 
                      ii=INPUT_union(ki=KEYBDINPUT(wVk=key_code, wScan=0, 
                                            dwFlags=KEYEVENTF_KEYDOWN, 
                                            time=0, dwExtraInfo=None)))
    # Key up
    input_up = INPUT(type=INPUT_KEYBOARD, 
                    ii=INPUT_union(ki=KEYBDINPUT(wVk=key_code, wScan=0, 
                                          dwFlags=KEYEVENTF_KEYUP, 
                                          time=0, dwExtraInfo=None)))
    
    user32.SendInput(1, ctypes.byref(input_down), ctypes.sizeof(INPUT))
    time.sleep(0.1)  # Short delay between down and up
    user32.SendInput(1, ctypes.byref(input_up), ctypes.sizeof(INPUT))
    time.sleep(0.2)  # Delay between keys

def type_character(char):
    """Type a character using the appropriate virtual key code"""
    # Handle special characters and convert to virtual key code
    if char == ';':
        vk = 0xBA  # VK_OEM_1 (semicolon)
    elif char == "'":
        vk = 0xDE  # VK_OEM_7 (single quote)
    elif char.isalpha():
        # Convert to uppercase for VK codes
        vk = ord(char.upper())
    elif char.isdigit():
        vk = ord(char)
    elif char == ' ':
        vk = 0x20  # VK_SPACE
    else:
        # For other special characters, we'd need additional mappings
        print(f"Warning: Character '{char}' may not be mapped correctly")
        vk = ord(char.upper()) if char.isalpha() else ord(char)
    
    # Type the key
    type_key(vk)

def unlock_screen_with_direct_input():
    """Unlock the screen using direct keyboard hardware simulation"""
    try:
        print("\nStarting unlock sequence with direct keyboard simulation...")
        password = get_stored_password()
        
        # Wake the screen first
        wake_screen()
        
        # Type each character in the password
        print("Typing password with direct keyboard simulation...")
        for char in password:
            try:
                type_character(char)
                # Print a dot to indicate progress without revealing password
                print(".", end="", flush=True)
            except Exception as e:
                print(f"\nError typing character: {e}")
        
        print("\nPassword typed, pressing Enter...")
        
        # Press Enter
        type_key(0x0D)  # VK_RETURN
        
        print("\n✓ Unlock sequence completed!")
        return True
    except Exception as e:
        print(f"\n✗ Error during unlock: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== DIRECT KEYBOARD SIMULATION UNLOCK ===")
    print("This utility uses low-level keyboard simulation")
    print("that may work when other methods fail.")
    print()
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        result = unlock_screen_with_direct_input()
        
        if result:
            print("\nUnlock attempt completed successfully!")
        else:
            print("\nUnlock attempt encountered errors.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    
    print("\nPress Enter to exit...")
    input()
