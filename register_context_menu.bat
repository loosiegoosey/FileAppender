@echo off
:: Request elevated privileges
powershell -Command "Start-Process cmd -ArgumentList '/c python C:\Users\Yuriy\Documents\GitHub\FileAppender\context_menu_improved.py' -Verb RunAs"
pause
