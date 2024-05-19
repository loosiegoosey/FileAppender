@echo off
:: Request elevated privileges
powershell -Command "Start-Process cmd -ArgumentList '/c python C:\Users\Yuriy\Documents\GitHub\FileAppender\deregister_context_menu.py' -Verb RunAs"
pause
