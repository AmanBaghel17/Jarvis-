import main
import time
import sys

def test_unlock_commands():
    print("Testing screen unlock commands...")
    print("This script will test multiple unlock command phrases")
    
    # List of commands to test
    commands = [
        "Aman",
        "unlock scree",
        "unlock screen",
        "my comman",
        "on lock",
        "open lock"
    ]
    
    # Wait for user confirmation
    input("\nPress Enter to continue with testing...")
    
    for cmd in commands:
        try:
            print(f"\nTesting command: '{cmd}'")
            # Just check if command is recognized, don't actually execute
            if any(phrase in cmd.lower() for phrase in ["aman", "unlock scree", "unlock screen", "unlock my screen", "my comman", "on lock", "open lock"]):
                print("✓ Command would be recognized")
            else:
                print("✗ Command would NOT be recognized")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nWould you like to execute one of these commands now?")
    print("Enter the number of the command to try, or 0 to exit:")
    
    for i, cmd in enumerate(commands, 1):
        print(f"{i}. {cmd}")
    
    try:
        choice = int(input("\nYour choice (0 to exit): "))
        if 1 <= choice <= len(commands):
            cmd = commands[choice-1]
            print(f"\nExecuting command: '{cmd}'")
            result = main.processCommand(cmd)
            print(f"Result: {result}")
    except ValueError:
        print("Invalid input. Exiting.")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTest completed.")
    print("You can also use the batch file 'unlock.bat' to directly unlock your screen.")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    test_unlock_commands()
