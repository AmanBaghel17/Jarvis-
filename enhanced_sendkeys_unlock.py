"""
Enhanced SendKeys utility for screen unlock
This focuses on making the SendKeys method as reliable as possible
"""

import os
import sys
import time
import subprocess
import json
import base64
import hashlib

def get_password():
    """Get the stored password from Jarvis configuration"""
    try:
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        config_file = os.path.join(config_dir, 'config.json')
        
        if not os.path.exists(config_file):
            print("Config file not found. Using default password.")
            return "test123"
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        encrypted_pwd = config.get('screen_password')
        if not encrypted_pwd:
            print("No password stored in config. Using default password.")
            return "test123"
            
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
        return "test123"  # Default fallback

def unlock_with_sendkeys():
    """Use SendKeys method to unlock the screen"""
    try:
        import win32com.client
        
        # Get the password
        password = get_password()
        print(f"Retrieved password (masked): {'*' * len(password)}")
        
        # Create the shell object
        print("Creating Shell object...")
        shell = win32com.client.Dispatch("WScript.Shell")
        
        # Wake the screen first with multiple methods
        print("Waking the screen...")
        
        # Method 1: Simulate keypresses to wake
        print("Sending Shift key to wake screen...")
        shell.SendKeys("+")  # Shift key
        time.sleep(0.5)
        
        # Method 2: Try to activate the login window
        print("Trying to activate login window...")
        attempts = ["Windows Login", "Windows", "Sign in to", "Windows Sign In", ""]
        for window_title in attempts:
            try:
                shell.AppActivate(window_title)
                print(f"Activated window: {window_title}")
                break
            except:
                print(f"Could not activate: {window_title}")
        
        # Give time for the screen to fully wake
        print("Waiting for screen to wake completely...")
        time.sleep(2)
        
        # Clear any existing input with backspace
        print("Clearing any existing input...")
        for i in range(10):
            shell.SendKeys("{BACKSPACE}")
            time.sleep(0.1)
        
        # Type the password with enhanced typing method
        print("Now typing password with enhanced method...")
        
        # Try two different typing methods
        
        # Method 1: Type all at once with formatting for special chars
        formatted_password = ""
        for char in password:
            if char in '+^%~(){}[]':
                formatted_password += '{' + char + '}'
            else:
                formatted_password += char
                
        print("Typing full password at once...")
        shell.SendKeys(formatted_password)
        time.sleep(1)
        
        # Method 2: Type character by character with delay
        print("Now typing character by character as backup...")
        for i, char in enumerate(password):
            if char in '+^%~(){}[]':
                shell.SendKeys('{' + char + '}')
            else:
                shell.SendKeys(char)
            print(f"Typed character {i+1}/{len(password)}")
            time.sleep(0.3)
        
        # Wait before pressing Enter
        print("Waiting before pressing Enter...")
        time.sleep(1)
        
        # Press Enter key
        print("Pressing Enter key...")
        shell.SendKeys("{ENTER}")
        
        print("SendKeys unlock sequence completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error in SendKeys method: {e}")
        return False

if __name__ == "__main__":
    print("=== Enhanced SendKeys Screen Unlock Utility ===")
    print("This utility uses the Windows SendKeys method to unlock your screen.")
    print("You have 5 seconds to switch to the lock screen...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    if unlock_with_sendkeys():
        print("Unlock sequence completed successfully. Your screen should be unlocked.")
    else:
        print("Unlock attempt failed. Please check the error messages above.")
