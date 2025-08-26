@echo off
echo Installing pip...
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
echo.
echo Now installing Jarvis dependencies...
python install_dependencies.py
echo.
echo Installation complete!
pause
