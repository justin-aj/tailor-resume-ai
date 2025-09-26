@echo off
REM Install Flask App as Windows Service
REM Run this file as Administrator

REM Check for administrator privileges
net session >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Administrator privileges required!
    echo.
    echo Please right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo Installing Resume Tailor AI as Windows Service...
echo Running with Administrator privileges...
echo.

REM Change to the webapp directory
cd /d "%~dp0"

REM Remove existing service if it exists
echo Removing existing service (if any)...
python flask_service.py remove 2>nul

REM Stop any running instances
echo Stopping any running service instances...
sc stop FlaskAppService >nul 2>&1
timeout /t 3 >nul

REM Force delete the service if it exists
echo Cleaning up service registration...
sc delete FlaskAppService >nul 2>&1
timeout /t 2 >nul

echo.

REM Install the service
echo Installing new service...
python flask_service.py install
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Failed to install service!
    echo.
    echo If you see "marked for deletion" error, please:
    echo 1. Reboot your computer to clear the service registry
    echo 2. Run this installer again
    echo.
    echo Alternatively, try running: sc delete FlaskAppService
    echo Then reboot and try again.
    echo.
    pause
    exit /b 1
)

echo Service installed successfully!
echo.

REM Set service to auto-start
echo Configuring service to start automatically...
sc config FlaskAppService start= auto
echo.

REM Start the service
echo Starting the service...
python flask_service.py start
if %ERRORLEVEL% neq 0 (
    echo.
    echo WARNING: Service installed but failed to start.
    echo Checking service status...
    python flask_service.py debug
    echo.
    echo You can try starting manually with: python flask_service.py start
    echo.
) else (
    echo Service started successfully!
    echo.
)

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