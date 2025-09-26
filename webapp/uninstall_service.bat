@echo off
REM Uninstall Flask App Windows Service
REM Run this file as Administrator

echo Uninstalling Resume Tailor AI Windows Service...
echo.

REM Change to the webapp directory
cd /d "%~dp0"

REM Set the Python executable path for virtual environment
set PYTHON_EXE=C:\Users\ajinf\Documents\PycharmProjects\tailor-resume-ai\.venv\Scripts\python.exe

REM Stop the service first
echo Stopping service...
"%PYTHON_EXE%" flask_service.py stop

REM Remove the service
echo Removing service...
"%PYTHON_EXE%" flask_service.py remove

echo Service uninstallation complete!
echo.
pause
