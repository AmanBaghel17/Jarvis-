"""
Windows API direct keyboard simulation for screen unlock
This uses Windows API functions directly without any intermediate libraries
"""

import os
import sys
import time
import ctypes
from ctypes import wintypes
import subprocess
import json
import base64
import hashlib

# Windows API constants
INPUT_KEYBOARD = 1
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

# Virtual key codes
VK_RETURN = 0x0D
VK_SHIFT = 0x10
VK_BACK = 0x08

# Define input structures
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

def get_password():
    """Get the stored password from Jarvis configuration"""
    try:
        # First try the plain text file if it exists
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        plain_pwd_file = os.path.join(config_dir, 'plain_password.txt')
        
        if os.path.exists(plain_pwd_file):
            with open(plain_pwd_file, 'r') as f:
                pwd = f.read().strip()
                if pwd:
                    return pwd
        
        # If that fails, try the encrypted config
        config_file = os.path.join(config_dir, 'config.json')
        
        if not os.path.exists(config_file):
            print("Config file not found. Using default password.")
            return "simple123"
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        encrypted_pwd = config.get('screen_password')
        if not encrypted_pwd:
            print("No password stored in config. Using default password.")
            return "simple123"
            
        # Get the encryption key
        def get_encryption_key():
            try:
                machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
                key = hashlib.sha256(machine_id.encode()).digest()
                return base64.urlsafe_b64encode(key)
            except:
                # Use a fixed key as fallback
                test_string = "JarvisAssistant2025"
                return base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
        
        # Decrypt the password
        from cryptography.fernet import Fernet
        key = get_encryption_key()
        if len(key) != 44:
            test_string = "JarvisAssistant2025"
            key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
            
        cipher_suite = Fernet(key)
        decrypted_pwd = cipher_suite.decrypt(encrypted_pwd.encode()).decode()
        
        return decrypted_pwd
    except Exception as e:
        print(f"Error getting password: {e}")
        return "simple123"  # Default fallback

def send_key(vk, scan=0, flags=0):
    """Send a key using the Windows API"""
    extra = ctypes.POINTER(wintypes.ULONG)()
    
    kb_input = KEYBDINPUT(vk, scan, flags, 0, extra)
    inp = INPUT(INPUT_KEYBOARD, INPUT_UNION(ki=kb_input))
    
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
    time.sleep(0.05)

def type_key(vk):
    """Type a key (press and release)"""
    send_key(vk, flags=KEYEVENTF_KEYDOWN)
    time.sleep(0.05)
    send_key(vk, flags=KEYEVENTF_KEYUP)
    time.sleep(0.05)

def wake_screen():
    """Wake up the screen using multiple methods"""
    user32 = ctypes.windll.user32
    
    print("Waking screen...")
    
    # Method 1: Shift key
    type_key(VK_SHIFT)
    time.sleep(0.5)
    
    # Method 2: Move the mouse
    user32.SetCursorPos(100, 100)
    time.sleep(0.1)
    user32.SetCursorPos(200, 200)
    time.sleep(0.5)
    
    # Wait for screen to wake up
    print("Waiting for screen to wake up...")
    time.sleep(2)

def unlock_with_direct_api():
    """Unlock the screen using direct Windows API calls"""
    try:
        password = get_password()
        print(f"Retrieved password (masked): {'*' * len(password)}")
        
        # Wake the screen
        wake_screen()
        
        # Clear any existing input with backspace
        print("Clearing any existing input...")
        for i in range(10):
            type_key(VK_BACK)
        
        # Type the password
        print("Typing password...")
        for i, char in enumerate(password):
            # Get virtual key code
            vk = ord(char.upper())
            
            # Check for shift key requirement
            needs_shift = char.isupper() or char in '~!@#$%^&*()_+{}|:"<>?'
            
            if needs_shift:
                # Press shift
                send_key(VK_SHIFT, flags=KEYEVENTF_KEYDOWN)
                
            # Press and release the key
            type_key(vk)
            
            if needs_shift:
                # Release shift
                send_key(VK_SHIFT, flags=KEYEVENTF_KEYUP)
                
            print(f"Typed character {i+1}/{len(password)}")
            time.sleep(0.1)
        
        # Wait before pressing Enter
        print("Waiting before pressing Enter...")
        time.sleep(1)
        
        # Press Enter
        print("Pressing Enter...")
        type_key(VK_RETURN)
        
        print("Direct API unlock sequence completed!")
        return True
        
    except Exception as e:
        print(f"Error in direct API method: {e}")
        return False

if __name__ == "__main__":
    print("=== Direct Windows API Screen Unlock Utility ===")
    print("This utility uses direct Windows API calls to unlock your screen.")
    print("You have 5 seconds to switch to the lock screen...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    if unlock_with_direct_api():
        print("Unlock sequence completed. Your screen should be unlocked.")
    else:
        print("Unlock attempt failed. Please check the error messages above.")
