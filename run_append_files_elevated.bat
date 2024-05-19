@echo off
:: Request elevated privileges
powershell -Command "Start-Process cmd -ArgumentList '/c C:\Users\Yuriy\Documents\GitHub\FileAppender\run_append_files.bat' -Verb RunAs"
