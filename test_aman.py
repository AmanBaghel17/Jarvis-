import main
import time
import sys

def test_aman_command():
    print("Testing 'Aman' command for screen unlock functionality...")
    print("This script will:")
    print("1. Simulate the 'Aman' command")
    print("2. Retrieve the stored password")
    print("3. Try to wake the screen")
    print("4. Type the password")
    print("5. Press Enter")
    
    # Wait for user confirmation
    input("\nPress Enter to continue...")
    
    try:
        # Simulate the Aman command
        print("\nSimulating 'Aman' command...")
        result = main.processCommand("Aman")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, '__traceback__'):
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)
    
    print("\nTest completed. Check if the screen unlock worked correctly.")
    print("If it didn't work, try running the direct unlock script: 'aman.bat'")
    
if __name__ == "__main__":
    test_aman_command()
    
    print("\nPress Enter to exit...")
    input()
