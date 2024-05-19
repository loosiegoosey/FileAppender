@echo off
:: Check if running with elevated privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~0' -Verb RunAs"
    exit /b
)

:: Run the Python script to register the context menu
python "C:\Users\Yuriy\Documents\GitHub\FileAppender\register_context_menu.py"
pause
