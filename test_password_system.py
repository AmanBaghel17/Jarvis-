"""
Test password decryption and storage to ensure screen unlock can work
"""

import os
import json
import base64
import hashlib
import subprocess

def get_encryption_key():
    # Generate a consistent encryption key based on the machine
    try:
        machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        # Use SHA-256 to generate a 32-byte key
        key = hashlib.sha256(machine_id.encode()).digest()
        # Properly format for Fernet (must be 32 url-safe base64-encoded bytes)
        return base64.urlsafe_b64encode(key)
    except Exception as e:
        print(f"Error getting encryption key: {e}")
        # Use a fixed key as fallback
        test_string = "JarvisAssistant2025"
        return base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())

def get_stored_password():
    try:
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        config_file = os.path.join(config_dir, 'config.json')
        
        if not os.path.exists(config_file):
            print(f"Config file does not exist: {config_file}")
            return None
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        encrypted_pwd = config.get('screen_password')
        if not encrypted_pwd:
            print("No screen_password entry in config file")
            return None
            
        try:
            from cryptography.fernet import Fernet
        except ImportError:
            print("Cryptography package not installed. Installing now...")
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
            from cryptography.fernet import Fernet
            from cryptography.fernet import Fernet
            
        key = get_encryption_key()
        # Make sure the key is properly formatted
        if len(key) != 44:  # Base64 encoding of 32 bytes is 44 characters
            print("Warning: Key length incorrect, generating fixed key")
            # Use a fixed key as fallback
            test_string = "JarvisAssistant2025"
            key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
            
        cipher_suite = Fernet(key)
        decrypted_pwd = cipher_suite.decrypt(encrypted_pwd.encode()).decode()
        
        return decrypted_pwd
    except Exception as e:
        print(f"Error getting password: {e}")
        return None

def set_test_password(password="test123"):
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        print("Cryptography package not installed. Installing now...")
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
        from cryptography.fernet import Fernet
        
    try:
        key = get_encryption_key()
        # Make sure the key is properly formatted
        if len(key) != 44:  # Base64 encoding of 32 bytes is 44 characters
            print("Warning: Key length incorrect, generating fixed key")
            # Use a fixed key as fallback
            test_string = "JarvisAssistant2025"
            key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest())
        
        cipher_suite = Fernet(key)
        encrypted_pwd = cipher_suite.encrypt(password.encode())
        
        # Store the encrypted password
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, 'config.json')
        
        # Read existing config or create new
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}
            
        # Update config with new password
        config['screen_password'] = encrypted_pwd.decode()
        
        # Write updated config
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        return True
    except Exception as e:
        print(f"Error setting password: {e}")
        return False

def test_password_system():
    print("===== Testing Jarvis Password System =====")
    
    # Check for existing password
    print("\nChecking for existing password...")
    existing_pwd = get_stored_password()
    if existing_pwd:
        print(f"Found existing password: {existing_pwd}")
    else:
        print("No existing password found.")
        
    # Set a test password
    test_pwd = "test123"
    print(f"\nSetting test password to '{test_pwd}'...")
    if set_test_password(test_pwd):
        print("Password set successfully!")
    else:
        print("Failed to set password.")
        
    # Verify the password was set correctly
    print("\nVerifying password was set correctly...")
    stored_pwd = get_stored_password()
    if stored_pwd == test_pwd:
        print("SUCCESS: Password verified correctly!")
    else:
        print(f"ERROR: Password verification failed. Got '{stored_pwd}' instead of '{test_pwd}'")

    # Save as plain text for testing
    try:
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        with open(os.path.join(config_dir, 'plain_password.txt'), 'w') as f:
            f.write(stored_pwd)
        print(f"\nSaved plaintext password to {os.path.join(config_dir, 'plain_password.txt')} for testing")
    except Exception as e:
        print(f"Error saving plaintext password: {e}")
        
    print("\n===== Password System Test Complete =====")

if __name__ == "__main__":
    test_password_system()
