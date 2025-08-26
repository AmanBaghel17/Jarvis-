import os
import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key():
    # Create a fixed test key for debugging purposes
    test_string = "JarvisAssistant2025"
    # Use SHA-256 to generate a 32-byte key
    key = hashlib.sha256(test_string.encode()).digest()
    # Fernet requires 32 url-safe base64-encoded bytes
    encoded_key = base64.urlsafe_b64encode(key)
    print(f"Generated key: {encoded_key}")
    print(f"Key length: {len(encoded_key)}")
    return encoded_key

def test_encryption():
    try:
        # Generate a key
        key = generate_key()
        
        # Create a Fernet cipher
        cipher = Fernet(key)
        
        # Test password
        test_pwd = "asdfghjkl;'"
        
        # Encrypt
        encrypted = cipher.encrypt(test_pwd.encode())
        print(f"Encrypted: {encrypted}")
        
        # Decrypt
        decrypted = cipher.decrypt(encrypted).decode()
        print(f"Decrypted: {decrypted}")
        
        # Verify
        if decrypted == test_pwd:
            print("Success! Encryption and decryption working correctly.")
        else:
            print("Error: Decrypted text doesn't match original.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing Fernet encryption...")
    test_encryption()
    
    print("\nPress Enter to exit...")
    input()
