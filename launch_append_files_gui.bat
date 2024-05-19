@echo off
:: Request elevated privileges
powershell -Command "Start-Process python -ArgumentList 'C:\Users\Yuriy\Documents\GitHub\FileAppender\append_files_gui.py \"%cd%\"' -Verb RunAs"
