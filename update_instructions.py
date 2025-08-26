"""
Jarvis Screen Unlock Utility - Update for main.py
"""

# Add this to the imports at the top of main.py if not already present:
# import subprocess
# import os
# import sys
# import pathlib

def install_autohotkey_module():
    """
    Helper function to add screen unlock capability to the existing Jarvis assistant.
    This function sets up the AutoHotkey based screen unlock solution.
    
    Add this function to main.py and call it from the main section.
    """
    import os
    import sys
    import subprocess
    
    try:
        # Check if AutoHotkey integration files exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        files_needed = [
            "unlock_screen.ahk",
            "run_unlock.bat",
            "prepare_password.py",
            "ahk_unlock.py"
        ]
        
        missing_files = []
        for file in files_needed:
            if not os.path.exists(os.path.join(script_dir, file)):
                missing_files.append(file)
        
        if missing_files:
            print(f"Missing AutoHotkey integration files: {', '.join(missing_files)}")
            print("Please ensure all files are present for screen unlock functionality.")
            return False
            
        # Create the required directories
        config_dir = os.path.join(os.path.expanduser('~'), '.jarvis')
        os.makedirs(config_dir, exist_ok=True)
        
        # Check if cryptography package is installed
        try:
            import cryptography
            print("Cryptography package is installed.")
        except ImportError:
            print("Installing cryptography package...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
            print("Cryptography package installed.")
            
        # Pre-generate the plain password file
        subprocess.run([sys.executable, os.path.join(script_dir, "prepare_password.py")])
        
        print("AutoHotkey screen unlock module setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error setting up AutoHotkey screen unlock module: {e}")
        return False

# Add this code to your unlock screen function in main.py:
"""
    # Method 4: AutoHotkey method (most reliable)
    try:
        print("Trying AutoHotkey method (most reliable)...")
        ahk_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ahk_unlock.py")
        if os.path.exists(ahk_script):
            subprocess.Popen([sys.executable, ahk_script])
            speak("I'm using AutoHotkey to unlock your screen.")
            return "Attempting to unlock your screen with AutoHotkey."
        else:
            print("AutoHotkey script not found")
    except Exception as ahk_error:
        print(f"AutoHotkey method failed: {ahk_error}")
"""
