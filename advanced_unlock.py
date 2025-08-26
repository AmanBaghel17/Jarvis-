"""
Special password typing utility that uses the Windows SendInput API
This is a low-level approach that can work on secure screens
"""

import os
import sys
import time
import ctypes
from ctypes import wintypes

# Define Windows API constants and structures
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

INPUT_KEYBOARD = 1

# Virtual key codes
VK_RETURN = 0x0D
VK_SHIFT = 0x10

# Define the input structures
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)))

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT_UNION(ctypes.Union):
    _fields_ = (("mi", MOUSEINPUT),
                ("ki", KEYBDINPUT),
                ("hi", HARDWAREINPUT))

class INPUT(ctypes.Structure):
    _fields_ = (("type", wintypes.DWORD),
                ("union", INPUT_UNION))

def read_password():
    """Read the password from the Jarvis configuration"""
    try:
        # First try to read the plain text file if it exists
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        password_file = os.path.join(config_dir, 'plain_password.txt')
        
        if os.path.exists(password_file):
            with open(password_file, 'r') as f:
                password = f.read().strip()
                if password:
                    return password
        
        # If that fails, try to read from the encrypted config
        try:
            import json
            import base64
            import hashlib
            from cryptography.fernet import Fernet
            
            config_file = os.path.join(config_dir, 'config.json')
            if not os.path.exists(config_file):
                return "test123"  # Default fallback password
                
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            encrypted_pwd = config.get('screen_password')
            if not encrypted_pwd:
                return "test123"  # Default fallback password
                
            # Get the encryption key using the same method as in main.py
            def get_encryption_key():
                import subprocess
                try:
                    machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
                    # Use SHA-256 to generate a 32-byte key
                    key = hashlib.sha256(machine_id.encode()).digest()
                    # Properly format for Fernet (must be 32 url-safe base64-encoded bytes)
                    return base64.urlsafe_b64encode(key)
                except:
                    # Use a fixed key as fallback
                    test_string = "JarvisAssistant2025"
                    return base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
            
            key = get_encryption_key()
            cipher_suite = Fernet(key)
            decrypted_pwd = cipher_suite.decrypt(encrypted_pwd.encode()).decode()
            
            return decrypted_pwd
        except Exception as e:
            print(f"Error decrypting password: {e}")
            return "test123"  # Default fallback password
    
    except Exception as e:
        print(f"Error reading password: {e}")
        return "test123"  # Default fallback password

def send_unicode_char(char):
    """Send a single Unicode character using SendInput API"""
    extra = ctypes.POINTER(wintypes.ULONG)()
    
    # Create a keyboard input structure for the character
    kb_input = KEYBDINPUT(0, ord(char), KEYEVENTF_UNICODE, 0, extra)
    
    # Create the input structure
    inp = INPUT(INPUT_KEYBOARD, INPUT_UNION(ki=kb_input))
    
    # Send the input
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
    
    # Small delay between keystrokes
    time.sleep(0.05)

def send_vk(vk, down=True):
    """Send a virtual key code"""
    extra = ctypes.POINTER(wintypes.ULONG)()
    flags = KEYEVENTF_KEYDOWN if down else KEYEVENTF_KEYUP
    
    # Create a keyboard input structure for the key
    kb_input = KEYBDINPUT(vk, 0, flags, 0, extra)
    
    # Create the input structure
    inp = INPUT(INPUT_KEYBOARD, INPUT_UNION(ki=kb_input))
    
    # Send the input
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

def wake_screen():
    """Wake up the screen using multiple methods"""
    user32 = ctypes.windll.user32
    
    print("Waking screen...")
    
    # Method 1: Shift key
    send_vk(VK_SHIFT, down=True)
    time.sleep(0.1)
    send_vk(VK_SHIFT, down=False)
    time.sleep(0.5)
    
    # Method 2: Move the mouse
    user32.SetCursorPos(100, 100)
    time.sleep(0.1)
    user32.SetCursorPos(200, 200)
    time.sleep(0.5)
    
    # Wait for screen to wake up
    print("Waiting for screen to wake up...")
    time.sleep(2)

def type_password():
    """Type the password using SendInput API"""
    # Get the password
    password = read_password()
    if not password:
        print("No password available")
        return False
    
    print(f"Using password: {password}")
    
    # Wake up the screen first
    wake_screen()
    
    # Type the password character by character using Unicode method
    print("Typing password...")
    for char in password:
        send_unicode_char(char)
    
    # Small delay before pressing Enter
    time.sleep(0.5)
    
    # Press Enter
    print("Pressing Enter...")
    send_vk(VK_RETURN, down=True)
    time.sleep(0.1)
    send_vk(VK_RETURN, down=False)
    
    print("Password typed successfully")
    return True

if __name__ == "__main__":
    print("=== Advanced Screen Unlock Utility ===")
    print("This will attempt to unlock your Windows screen using low-level keyboard input.")
    print("You have 3 seconds to switch to the lock screen...")
    
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    if type_password():
        print("Unlock attempt completed. Your screen should now be unlocked.")
    else:
        print("Unlock attempt failed!")
