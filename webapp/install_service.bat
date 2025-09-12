@echo off
REM Install Flask App as Windows Service
REM Run this file as Administrator

echo Installing Resume Tailor AI as Windows Service...
echo.

REM Change to the webapp directory
cd /d "%~dp0"

REM Remove existing service if it exists
echo Removing existing service (if any)...
python flask_service.py remove
echo.

REM Install the service
echo Installing new service...
python flask_service.py install --startup auto
echo.

REM Start the service
echo Starting the service...
python flask_service.py start
echo.

echo Service installation complete!
echo.
echo You can now:
echo 1. Check service status: python flask_service.py debug
echo 2. Stop service: python flask_service.py stop
echo 3. Start service: python flask_service.py start
echo 4. Remove service: python flask_service.py remove
echo.
echo The web app should be available at: http://localhost:5000
echo.
pause
