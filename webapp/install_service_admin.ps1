# Install Flask App as Windows Service (PowerShell)
# This script automatically elevates to Administrator privileges

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Requesting Administrator privileges..." -ForegroundColor Yellow
    
    # Re-launch script with Administrator privileges
    Start-Process PowerShell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

Write-Host "Running with Administrator privileges..." -ForegroundColor Green
Write-Host "Installing Resume Tailor AI as Windows Service..." -ForegroundColor Cyan

# Change to script directory
Set-Location $PSScriptRoot

# Clean up any existing service
Write-Host "Cleaning up existing service..." -ForegroundColor Yellow
try {
    python flask_service.py stop 2>$null
    Start-Sleep -Seconds 2
    python flask_service.py remove 2>$null
    Start-Sleep -Seconds 2
    
    # Force delete from Windows Service Manager
    sc.exe delete FlaskAppService 2>$null
    Start-Sleep -Seconds 3
} catch {
    # Ignore errors during cleanup
}

# Install the service
Write-Host "Installing new service..." -ForegroundColor Yellow
$installResult = python flask_service.py install
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install service!" -ForegroundColor Red
    Write-Host "Exit code: $LASTEXITCODE" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Service installed successfully!" -ForegroundColor Green

# Configure auto-start
Write-Host "Configuring service to start automatically..." -ForegroundColor Yellow
sc.exe config FlaskAppService start= auto

# Start the service
Write-Host "Starting the service..." -ForegroundColor Yellow
$startResult = python flask_service.py start
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Service installed but failed to start." -ForegroundColor Yellow
    Write-Host "Checking service status..." -ForegroundColor Yellow
    python flask_service.py debug
} else {
    Write-Host "Service started successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Service installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  Check status:  python flask_service.py debug" -ForegroundColor White
Write-Host "  Stop service:  python flask_service.py stop" -ForegroundColor White
Write-Host "  Start service: python flask_service.py start" -ForegroundColor White
Write-Host "  Remove:        python flask_service.py remove" -ForegroundColor White
Write-Host ""
Write-Host "Web app should be available at: http://localhost:5000" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to exit"
