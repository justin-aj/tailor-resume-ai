@echo off
REM Uninstall Flask App Windows Service
REM Run this file as Administrator

echo Uninstalling Resume Tailor AI Windows Service...
echo.

REM Change to the webapp directory
cd /d "%~dp0"

REM Stop the service first
echo Stopping service...
python flask_service.py stop

REM Remove the service
echo Removing service...
python flask_service.py remove

echo Service uninstallation complete!
echo.
pause
