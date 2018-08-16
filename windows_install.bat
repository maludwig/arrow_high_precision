@echo off

REM echo %PYTHON%
REM goto :theend

%PYTHON%\python.exe --version 2>&1 | find "2.6" && goto :getpip
echo %PYTHON%\python.exe -m pip install arrow
goto :theend

:getpip
echo Python 2.6 detected
curl https://bootstrap.pypa.io/2.6/get-pip.py -o get-pip.py
%PYTHON%\python.exe get-pip.py
echo %PYTHON%\pip.exe install arrow

:theend