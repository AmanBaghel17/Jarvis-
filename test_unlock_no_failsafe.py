"""
Failsafe-disabled Screen Unlock Test
This script tests unlocking the screen with PyAutoGUI failsafe disabled.
"""

import pyautogui
import time

# Disable failsafe - necessary for screen unlock
print("Disabling PyAutoGUI failsafe...")
pyautogui.FAILSAFE = False

def test_unlock():
    print("\nTesting screen unlock without failsafe protection...")
    
    # Default password if not specified
    password = "asdfghjkl;'"
    
    try:
        # Wake screen with mouse movement (safe pattern)
        print("1. Moving mouse to center of screen (safer approach)...")
        # Move to center, not corners
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        # Move in a small pattern near center
        pyautogui.moveTo(center_x - 100, center_y, duration=0.2)
        pyautogui.moveTo(center_x + 100, center_y, duration=0.2)
        pyautogui.moveTo(center_x, center_y - 100, duration=0.2)
        pyautogui.moveTo(center_x, center_y + 100, duration=0.2)
        pyautogui.moveTo(center_x, center_y, duration=0.2)
        
        time.sleep(1)
        
        # Type password
        print("2. Typing password...")
        pyautogui.typewrite(password, interval=0.15)
        time.sleep(0.5)
        
        # Press Enter
        print("3. Pressing Enter...")
        pyautogui.press('enter')
        
        print("\n✓ Unlock sequence completed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error during unlock: {e}")
        return False

if __name__ == "__main__":
    print("=== FAILSAFE-DISABLED UNLOCK TEST ===")
    print("WARNING: PyAutoGUI failsafe is disabled, which removes the")
    print("emergency stop feature (moving mouse to corner of screen).")
    print("This is necessary for screen unlock functionality.")
    print("\nPress Enter to continue with test or Ctrl+C to cancel...")
    
    try:
        input()
        test_unlock()
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
    
    print("\nPress Enter to exit...")
    input()
