python --version | find "2.6" && goto :getpip
echo %PYTHON%\python.exe -m pip install arrow
goto :theend

:getpip
echo Python 2.6 detected
echo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
echo %PYTHON%\python.exe get-pip.py
echo %PYTHON%\pip.exe install arrow

:theend