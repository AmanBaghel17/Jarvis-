import os
import sys
import json

# Create the necessary directory for storing password in plaintext 
# (temporary solution for AutoHotkey to read)
def save_password_for_autohotkey():
    try:
        # Get the path to the stored encrypted password config
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        config_file = os.path.join(config_dir, 'config.json')
        
        if not os.path.exists(config_file):
            print("No password configuration found!")
            return False
        
        # Read the stored password
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        from cryptography.fernet import Fernet
        import hashlib
        import base64
        
        # Get the encryption key using the same method as in main.py
        def get_encryption_key():
            import subprocess
            # Generate a consistent encryption key based on the machine
            machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
            # Use SHA-256 to generate a 32-byte key
            key = hashlib.sha256(machine_id.encode()).digest()
            # Properly format for Fernet (must be 32 url-safe base64-encoded bytes)
            return base64.urlsafe_b64encode(key)
        
        key = get_encryption_key()
        # Make sure the key is properly formatted
        if len(key) != 44:  # Base64 encoding of 32 bytes is 44 characters
            print("Warning: Key length incorrect, generating fixed key")
            # Use a fixed key as fallback
            test_string = "JarvisAssistant2025"
            key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
            
        cipher_suite = Fernet(key)
        encrypted_pwd = config.get('screen_password')
        if not encrypted_pwd:
            print("No password stored in config!")
            return False
            
        # Decrypt the password
        decrypted_pwd = cipher_suite.decrypt(encrypted_pwd.encode()).decode()
        
        # Save the decrypted password to a plain text file for AutoHotkey to read
        # NOTE: This is a security risk but necessary for AutoHotkey to work
        os.makedirs(config_dir, exist_ok=True)
        with open(os.path.join(config_dir, 'plain_password.txt'), 'w') as f:
            f.write(decrypted_pwd)
        
        print(f"Password saved for AutoHotkey use in: {os.path.join(config_dir, 'plain_password.txt')}")
        return True
        
    except Exception as e:
        print(f"Error preparing password for AutoHotkey: {e}")
        return False

if __name__ == "__main__":
    print("Preparing password for AutoHotkey unlock script...")
    if save_password_for_autohotkey():
        print("Successfully prepared password for AutoHotkey")
    else:
        print("Failed to prepare password")
