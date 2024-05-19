@echo off
setlocal
set "args="
:loop
if "%~1"=="" goto done
set "args=%args% "%~1""
shift
goto loop
:done
python "C:\path\to\context_menu_improved.py" %args%
endlocal
