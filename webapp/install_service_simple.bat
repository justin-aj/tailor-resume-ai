@echo off
echo ========================================
echo   Resume Tailor AI - Service Installer
echo ========================================
echo.
echo This will install the web app as a Windows service.
echo The service will start automatically when Windows boots.
echo.
echo IMPORTANT: This batch file must be run as Administrator
echo.
pause

cd /d "%~dp0"

REM Set the Python executable path for virtual environment
set PYTHON_EXE=C:\Users\ajinf\Documents\PycharmProjects\tailor-resume-ai\.venv\Scripts\python.exe

echo.
echo Stopping any existing instances...
taskkill /F /IM python.exe 2>nul

echo.
echo Cleaning up existing service...
"%PYTHON_EXE%" flask_service.py stop 2>nul
"%PYTHON_EXE%" flask_service.py remove 2>nul
sc delete FlaskAppService 2>nul

echo.
echo Waiting for cleanup to complete...
timeout /t 5 /nobreak >nul

echo.
echo Installing the service...
"%PYTHON_EXE%" flask_service.py install
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Failed to install service!
    echo Make sure you are running this as Administrator.
    echo.
    pause
    exit /b 1
)

echo.
echo Configuring auto-start...
sc config FlaskAppService start= auto

echo.
echo Starting the service...
"%PYTHON_EXE%" flask_service.py start
if %ERRORLEVEL% neq 0 (
    echo.
    echo WARNING: Service installed but failed to start.
    echo Checking service status...
    "%PYTHON_EXE%" flask_service.py debug
) else (
    echo.
    echo SUCCESS! Service is now running.
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Your Resume Tailor AI is now available at:
echo http://localhost:5000
echo.
echo The service will start automatically when Windows boots.
echo.
echo Service Management Commands:
echo   Start:  "%PYTHON_EXE%" flask_service.py start
echo   Stop:   "%PYTHON_EXE%" flask_service.py stop
echo   Status: "%PYTHON_EXE%" flask_service.py debug
echo   Remove: "%PYTHON_EXE%" flask_service.py remove
echo.
pause
