@echo off
echo ===============================================
echo Set Simple Password for Testing
echo ===============================================
echo.
echo This will set a very simple password for testing the unlock feature.
echo The password will be set to: simple123
echo.
echo Press any key to continue...
pause >nul

echo.
echo Setting simple password...

python -c "import os, sys, json, base64, hashlib; from cryptography.fernet import Fernet; config_dir = os.path.join(os.path.expanduser('~'), '.jarvis'); os.makedirs(config_dir, exist_ok=True); test_string = 'JarvisAssistant2025'; key = base64.urlsafe_b64encode(hashlib.sha256(test_string.encode()).digest()); cipher_suite = Fernet(key); encrypted_pwd = cipher_suite.encrypt('simple123'.encode()); config_file = os.path.join(config_dir, 'config.json'); config = {'screen_password': encrypted_pwd.decode()}; open(config_file, 'w').write(json.dumps(config)); print('Password set to: simple123'); open(os.path.join(config_dir, 'plain_password.txt'), 'w').write('simple123');"

echo.
echo ===============================================
echo Password has been set to: simple123
echo.
echo Now try these unlock methods:
echo 1. run_sendkeys_unlock.bat
echo 2. run_advanced_unlock.bat 
echo 3. master_unlock.bat
echo ===============================================
echo.
pause
