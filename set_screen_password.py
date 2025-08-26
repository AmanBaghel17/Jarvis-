import os
import sys
import json
import base64
import hashlib
from cryptography.fernet import Fernet

def get_encryption_key():
    # Use a fixed key that we know works
    test_string = "JarvisAssistant2025"
    key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
    return key

def set_password(password):
    try:
        key = get_encryption_key()
        cipher_suite = Fernet(key)
        encrypted_pwd = cipher_suite.encrypt(password.encode())
        
        # Store the encrypted password
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        os.makedirs(config_dir, exist_ok=True)
        
        with open(os.path.join(config_dir, 'config.json'), 'w') as f:
            json.dump({'screen_password': encrypted_pwd.decode()}, f)
        
        print(f"Password '{password}' saved successfully!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    password = "asdfghjkl;'"
    print(f"Setting password to: {password}")
    set_password(password)
    
    print("\nPress Enter to continue...")
    input()
