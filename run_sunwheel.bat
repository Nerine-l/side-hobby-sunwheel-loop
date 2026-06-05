@echo off
setlocal

cd /d "%~dp0"

set "VENV_PY=.venv\Scripts\python.exe"

if not exist "%VENV_PY%" (
    echo Creating local Python environment...
    py -3.12 -m venv .venv
    if errorlevel 1 (
        echo Could not create .venv with py -3.12. Trying python...
        python -m venv .venv
    )
)

if not exist "%VENV_PY%" (
    echo.
    echo Python 3.12 is required.
    echo Install Python 3.12, then run this file again.
    echo.
    pause
    exit /b 1
)

"%VENV_PY%" -c "import pygame" >nul 2>nul
if errorlevel 1 (
    echo Installing required packages. This is needed only the first time...
    "%VENV_PY%" -m pip install --upgrade pip setuptools wheel
    if errorlevel 1 goto error
    "%VENV_PY%" -m pip install -r requirements.txt
    if errorlevel 1 goto error
)

if /i "%~1"=="--setup-only" (
    echo Setup is ready.
    exit /b 0
)

"%VENV_PY%" main.py
if errorlevel 1 goto error

exit /b 0

:error
echo.
echo Failed to start side-hobby-sunwheel-loop.
echo Check the message above, then try again.
echo.
pause
exit /b 1
