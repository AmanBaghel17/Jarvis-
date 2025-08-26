# AutoHotkey Screen Unlock Integration

This folder contains a new, reliable solution for unlocking your Windows screen using AutoHotkey.

## Why AutoHotkey Works Better

AutoHotkey has special privileges for typing on the Windows lock screen that regular Python libraries like PyAutoGUI don't have. It's specifically designed for Windows automation and can reliably type even in secure contexts.

## How to Use This Solution

1. Install AutoHotkey from https://www.autohotkey.com/download/
2. Make sure your password is set in Jarvis (say "set screen password to YOUR_PASSWORD")
3. When you say "unlock screen" or similar commands, Jarvis will now try to use AutoHotkey

## Files in this Solution

- `unlock_screen.ahk` - The main AutoHotkey script for screen unlocking
- `run_unlock.bat` - Batch file to run the unlock script (also checks if AutoHotkey is installed)
- `prepare_password.py` - Prepares your password for AutoHotkey to use
- `ahk_unlock.py` - Python wrapper to run the AutoHotkey script
- `update_instructions.py` - Instructions for integrating this solution into main.py

## Manual Screen Unlock

If you want to manually unlock your screen (without voice):

1. Double-click `run_unlock.bat`
2. Follow the prompts on screen

## Security Note

This solution stores your password in an encrypted format, but temporarily creates a plaintext file when unlocking. This file is stored in your user directory (`.jarvis` folder) and should be kept secure.
