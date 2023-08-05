choice /C YN /M 是否联网下载最新版本
set r=%errorlevel%
if "%r%"=="1" (
    python setup.py install
) 
if "%r%"=="2" (
    pip3 install allenlib
)