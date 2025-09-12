@echo off
REM Test the Flask App before installing as service
echo Testing Resume Tailor AI Flask App...
echo.
echo Starting Flask app in test mode...
echo Press Ctrl+C to stop the test
echo.
echo If this works, you can install as service using install_service.bat (run as Administrator)
echo.

cd /d "%~dp0"
python run.py
