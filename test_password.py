import main

# Test if password is properly stored
print("Setting default password...")
main.ensure_default_password()

# Get the stored password
print("Getting stored password...")
password = main.get_stored_password()

if password:
    print(f"Password is stored successfully: {password}")
    print("Ready to use screen unlock feature!")
else:
    print("Failed to store password. Please check the error messages above.")
    
input("Press Enter to exit...")
