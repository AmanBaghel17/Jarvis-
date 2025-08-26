"""
Simplified screen unlock solution that doesn't require AutoHotkey
"""

import os
import time
import sys
import ctypes
from ctypes import wintypes
import subprocess

def read_password():
    """Read the password from the plain text file"""
    try:
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        password_file = os.path.join(config_dir, 'plain_password.txt')
        
        if not os.path.exists(password_file):
            print("Password file doesn't exist, trying to create it...")
            # Try to run prepare_password.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            prepare_script = os.path.join(script_dir, "prepare_password.py")
            if os.path.exists(prepare_script):
                subprocess.run([sys.executable, prepare_script], check=True)
                
            if not os.path.exists(password_file):
                print("Failed to create password file.")
                return None
        
        with open(password_file, 'r') as f:
            password = f.read().strip()
        
        if not password:
            print("Password file is empty")
            return None
            
        return password
    except Exception as e:
        print(f"Error reading password: {e}")
        return None

def unlock_screen():
    """Attempt to unlock the screen with all available methods"""
    password = read_password()
    if not password:
        print("No password available. Please set one first.")
        return False
        
    print(f"Using password: {password}")
    
    # Wake the screen
    user32 = ctypes.windll.User32
    print("Waking screen...")
    
    # Using multiple wake methods for reliability
    # Method 1: Shift key
    user32.keybd_event(0xA0, 0, 0, 0)  # SHIFT key down
    user32.keybd_event(0xA0, 0, 2, 0)  # SHIFT key up
    time.sleep(0.5)
    
    # Method 2: Space key
    user32.keybd_event(0x20, 0, 0, 0)  # SPACE key down
    user32.keybd_event(0x20, 0, 2, 0)  # SPACE key up
    time.sleep(0.5)
    
    # Method 3: Mouse movement
    try:
        import pyautogui
        pyautogui.FAILSAFE = False  # Disable failsafe
        pyautogui.moveTo(100, 100, duration=0.2)
        pyautogui.moveTo(200, 200, duration=0.2)
        print("Mouse moved to wake screen")
    except:
        print("Could not use mouse movement")
    
    # Give the screen time to wake up
    print("Waiting for screen to wake up...")
    time.sleep(2)
    
    # Try all available methods to type the password
    success = False
    
    # Method 1: Windows SendKeys (most reliable)
    try:
        print("\nTrying Windows SendKeys method...")
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.AppActivate("Windows")
        
        # Type each character with a delay
        for char in password:
            shell.SendKeys(char)
            time.sleep(0.2)
        
        # Press Enter
        time.sleep(0.5)
        shell.SendKeys("{ENTER}")
        print("Sent password using Windows SendKeys")
        success = True
    except Exception as e:
        print(f"SendKeys method failed: {e}")
    
    # Method 2: PyAutoGUI
    if not success:
        try:
            print("\nTrying PyAutoGUI method...")
            import pyautogui
            pyautogui.FAILSAFE = False  # Disable failsafe
            
            # Type the password
            pyautogui.typewrite(password, interval=0.2)
            time.sleep(0.5)
            pyautogui.press('enter')
            print("Sent password using PyAutoGUI")
            success = True
        except Exception as e:
            print(f"PyAutoGUI method failed: {e}")
    
    # Method 3: Windows API keybd_event
    if not success:
        try:
            print("\nTrying Windows API keybd_event method...")
            # Type each character
            for char in password:
                # Convert character to virtual key code
                vk = ord(char.upper())
                user32.keybd_event(vk, 0, 0, 0)  # Key down
                user32.keybd_event(vk, 0, 2, 0)  # Key up
                time.sleep(0.2)  # Longer delay between keys
            
            # Press Enter
            time.sleep(0.5)
            user32.keybd_event(0x0D, 0, 0, 0)  # ENTER key down
            user32.keybd_event(0x0D, 0, 2, 0)  # ENTER key up
            print("Sent password using Windows API")
            success = True
        except Exception as e:
            print(f"Windows API method failed: {e}")
    
    # Method 4: Clipboard method (may work on lock screens that allow paste)
    if not success:
        try:
            print("\nTrying clipboard method...")
            # Import needed for clipboard
            import win32clipboard
            
            # Save current clipboard content
            win32clipboard.OpenClipboard()
            try:
                old_clipboard = win32clipboard.GetClipboardData()
            except:
                old_clipboard = None
                
            # Set password to clipboard
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(password)
            win32clipboard.CloseClipboard()
            
            # Try to paste with Ctrl+V
            time.sleep(0.5)
            user32.keybd_event(0x11, 0, 0, 0)  # Ctrl key down
            user32.keybd_event(0x56, 0, 0, 0)  # V key down
            time.sleep(0.1)
            user32.keybd_event(0x56, 0, 2, 0)  # V key up
            user32.keybd_event(0x11, 0, 2, 0)  # Ctrl key up
            time.sleep(0.5)
            
            # Press Enter
            user32.keybd_event(0x0D, 0, 0, 0)  # ENTER key down
            user32.keybd_event(0x0D, 0, 2, 0)  # ENTER key up
            
            # Restore clipboard
            if old_clipboard:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(old_clipboard)
                win32clipboard.CloseClipboard()
                
            print("Sent password using clipboard")
            success = True
        except Exception as e:
            print(f"Clipboard method failed: {e}")
    
    if success:
        print("\nPassword has been sent to the screen. Screen should unlock shortly.")
    else:
        print("\nFailed to send password with any available method.")
        
    return success

if __name__ == "__main__":
    print("=== Simple Screen Unlock Utility ===")
    print("This will attempt to unlock your Windows screen.")
    print("You have 3 seconds to switch to the lock screen...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    if unlock_screen():
        print("Unlock attempt completed successfully!")
    else:
        print("Unlock attempt failed!")
