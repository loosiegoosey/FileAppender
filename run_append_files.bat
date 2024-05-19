@echo off
setlocal enabledelayedexpansion

:: Use PowerShell to get all selected files and pass them to the Python script
for /f "delims=" %%I in ('powershell -command "Get-Clipboard -Format FileDropList | ForEach-Object {Write-Output $_}"') do (
    set args=!args! "%%~I"
)

echo Arguments to be passed: !args!
pause

python "C:\Users\Yuriy\Documents\GitHub\FileAppender\context_menu_improved.py" !args!

endlocal
