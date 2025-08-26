import main
import time
import sys

def test_unlock():
    print("Testing screen unlock functionality...")
    print("This script will:")
    print("1. Retrieve the stored password")
    print("2. Try to wake the screen")
    print("3. Type the password")
    print("4. Press Enter")
    
    # Wait for user confirmation
    input("\nPress Enter to continue...")
    
    try:
        # First check if password is available
        password = main.get_stored_password()
        if not password:
            password = main.DEFAULT_PASSWORD
            print(f"Using default password: {password}")
        else:
            print("Using stored password")
        
        # Simulate unlock command
        print("\nSimulating unlock command...")
        result = main.processCommand("unlock screen")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, '__traceback__'):
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)
    
    print("\nTest completed. Check if the screen unlock worked correctly.")
    print("If it didn't work, you can try installing required packages:")
    print("pip install pyautogui")
    
if __name__ == "__main__":
    test_unlock()
    
    print("\nPress Enter to exit...")
    input()
