# PowerShell script to install Flask service with admin privileges
# Run this with: powershell -ExecutionPolicy Bypass -File install_service.ps1

$currentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $currentDir

Write-Host "Installing Resume Tailor AI as Windows Service..." -ForegroundColor Green
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "This script requires administrator privileges." -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Right-click on install_service.bat and select 'Run as administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

try {
    # Remove existing service if it exists
    Write-Host "Removing existing service (if any)..." -ForegroundColor Yellow
    & python flask_service.py remove 2>$null
    
    # Install the service
    Write-Host "Installing new service..." -ForegroundColor Yellow
    & python flask_service.py install --startup auto
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Service installed successfully!" -ForegroundColor Green
        
        # Start the service
        Write-Host "Starting the service..." -ForegroundColor Yellow
        & python flask_service.py start
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Service started successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Resume Tailor AI is now running as a Windows service!" -ForegroundColor Green
            Write-Host "Web app is available at: http://localhost:5000" -ForegroundColor Cyan
        } else {
            Write-Host "Failed to start service. Check the logs." -ForegroundColor Red
        }
    } else {
        Write-Host "Failed to install service." -ForegroundColor Red
    }
    
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Service management commands:" -ForegroundColor Yellow
Write-Host "  Check status: python flask_service.py debug" -ForegroundColor Gray
Write-Host "  Stop service: python flask_service.py stop" -ForegroundColor Gray
Write-Host "  Start service: python flask_service.py start" -ForegroundColor Gray
Write-Host "  Remove service: python flask_service.py remove" -ForegroundColor Gray
Write-Host ""
pause
