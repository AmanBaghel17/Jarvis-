import sys
import os
import base64
import hashlib
from cryptography.fernet import Fernet
import json

# Define the default password
DEFAULT_PASSWORD = "asdfghjkl;'"

def get_encryption_key():
    # Generate a fixed key for testing
    test_string = "JarvisAssistant2025"
    # Use SHA-256 to generate a 32-byte key
    key = hashlib.sha256(test_string.encode()).digest()
    # Fernet requires 32 url-safe base64-encoded bytes
    return base64.urlsafe_b64encode(key)

def set_stored_password(password):
    try:
        key = get_encryption_key()
        print(f"Key for encryption: {key}")
        
        cipher_suite = Fernet(key)
        encrypted_pwd = cipher_suite.encrypt(password.encode())
        
        # Store the encrypted password
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, 'config.json')
        print(f"Saving to: {config_file}")
        
        with open(config_file, 'w') as f:
            json.dump({'screen_password': encrypted_pwd.decode()}, f)
        
        print("Password saved successfully!")
        return True
    except Exception as e:
        print(f"Error setting password: {e}")
        return False

def get_stored_password():
    try:
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        config_file = os.path.join(config_dir, 'config.json')
        
        if not os.path.exists(config_file):
            print(f"Config file not found: {config_file}")
            return None
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        encrypted_pwd = config.get('screen_password')
        if not encrypted_pwd:
            print("No password found in config")
            return None
            
        key = get_encryption_key()
        cipher_suite = Fernet(key)
        decrypted_pwd = cipher_suite.decrypt(encrypted_pwd.encode()).decode()
        
        return decrypted_pwd
    except Exception as e:
        print(f"Error getting password: {e}")
        return None

def main():
    print("Testing password storage...")
    
    # Set the password
    print(f"Setting password to: {DEFAULT_PASSWORD}")
    if set_stored_password(DEFAULT_PASSWORD):
        print("Password set successfully.")
    else:
        print("Failed to set password.")
        return
    
    # Retrieve the password
    print("\nTrying to retrieve password...")
    retrieved_pwd = get_stored_password()
    
    if retrieved_pwd:
        print(f"Retrieved password: {retrieved_pwd}")
        if retrieved_pwd == DEFAULT_PASSWORD:
            print("SUCCESS! Password correctly stored and retrieved.")
        else:
            print("ERROR: Retrieved password doesn't match what was stored!")
    else:
        print("Failed to retrieve password.")

if __name__ == "__main__":
    main()
    
    print("\nPress Enter to exit...")
    input()
