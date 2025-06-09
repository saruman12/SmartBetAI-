@echo off
pip install -r requirements.txt
pyinstaller --onefile --windowed main.py --add-data "assets\logo.png;assets"
echo.
echo *** Build completada. EXE en dist\main.exe ***
pause
