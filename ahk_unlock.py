# Integration for the AutoHotkey unlock method in main.py

import subprocess
import os
import sys
import time
import pathlib

def run_autohotkey_unlock():
    """Run the AutoHotkey screen unlock script"""
    try:
        print("Starting AutoHotkey screen unlock process")
        
        # First, prepare the password for AutoHotkey
        prepare_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prepare_password.py")
        subprocess.run([sys.executable, prepare_script], check=True)
        
        # Now run the AutoHotkey script
        ahk_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unlock_screen.ahk")
        
        # Check if AutoHotkey is installed
        try:
            # Try to find AutoHotkey executable
            ahk_executable = "autohotkey.exe"
            result = subprocess.run(["where", ahk_executable], capture_output=True, text=True)
            
            if result.returncode == 0:
                ahk_path = result.stdout.strip().split("\n")[0]
                print(f"Found AutoHotkey at: {ahk_path}")
                subprocess.Popen([ahk_path, ahk_script])
                print("AutoHotkey unlock script started")
                return True
            else:
                print("AutoHotkey not found in PATH. Looking for common install locations...")
                
                # Try common install locations
                common_paths = [
                    os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "AutoHotkey", "AutoHotkey.exe"),
                    os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "AutoHotkey", "AutoHotkey.exe")
                ]
                
                for path in common_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path, ahk_script])
                        print(f"Found AutoHotkey at {path} and launched unlock script")
                        return True
                
                # If we get here, we couldn't find AutoHotkey
                print("AutoHotkey not found. Please install it from https://www.autohotkey.com/")
                # Run the batch file instead which will guide the user
                batch_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_unlock.bat")
                subprocess.Popen([batch_file], shell=True)
                return False
                
        except Exception as e:
            print(f"Error trying to locate AutoHotkey: {e}")
            # Run the batch file instead which will guide the user
            batch_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_unlock.bat")
            subprocess.Popen([batch_file], shell=True)
            return False
            
    except Exception as e:
        print(f"Error running AutoHotkey unlock: {e}")
        return False

if __name__ == "__main__":
    run_autohotkey_unlock()
