# Resume Tailor AI - Windows Service Installation

This guide helps you install Resume Tailor AI as a Windows service so it runs automatically on system startup.

## ✅ QUICK START (TESTED & WORKING)

**The simplest way to install:**

1. **Right-click on `install_service.bat`**
2. **Select "Run as administrator"**
3. **Wait for completion**
4. **Access your app at http://localhost:5000**

**Done!** Your Resume Tailor AI is now running as a Windows service and will start automatically with Windows.

## Prerequisites

✅ Python 3.7+ installed
✅ Flask app working (test with `python run.py`)
✅ pywin32 package installed (`pip install pywin32`)

## Quick Installation

### Option 1: Using Batch File (✅ RECOMMENDED - WORKS!)

**This is the easiest and most reliable method:**

1. **Right-click on `install_service.bat`** in the webapp folder
2. **Select "Run as administrator"**
3. **Wait for the installation to complete**
4. **Press any key when prompted**

**That's it!** The service will be installed and started automatically.

## ✅ Verify Installation Success

After running the batch file, verify everything is working:

1. **Open your web browser**
2. **Go to http://localhost:5000**
3. **You should see the Resume Tailor AI interface**
4. **Check Windows Services** (optional):
   - Press `Win + R`, type `services.msc`, press Enter
   - Look for "Flask App Service" - it should show "Running"

## Alternative Installation Methods

### Option 2: Using PowerShell Script
   - Right-click on PowerShell icon
   - Select "Run as administrator"

2. **Navigate to the webapp directory**
   ```powershell
   cd "C:\Users\ajinf\Documents\PycharmProjects\tailor-resume-ai\webapp"
   ```

3. **Run the installation script**
   ```powershell
   powershell -ExecutionPolicy Bypass -File install_service.ps1
   ```

### Option 3: Manual Installation

1. **Open Command Prompt as Administrator**

2. **Navigate to webapp directory**
   ```cmd
   cd "C:\Users\ajinf\Documents\PycharmProjects\tailor-resume-ai\webapp"
   ```

3. **Install the service**
   ```cmd
   python flask_service.py install --startup auto
   ```

4. **Start the service**
   ```cmd
   python flask_service.py start
   ```

## Service Management Commands

```cmd
# Check service status
python flask_service.py debug

# Start the service
python flask_service.py start

# Stop the service  
python flask_service.py stop

# Restart the service
python flask_service.py stop
python flask_service.py start

# Remove the service
python flask_service.py remove
```

## Accessing the Web Application

Once the service is running:

- **Local access**: http://localhost:5000
- **Network access**: http://YOUR_IP_ADDRESS:5000
- **All interfaces**: http://0.0.0.0:5000

## Troubleshooting

### Service Won't Install
- **Solution**: Run PowerShell/Command Prompt as Administrator
- **Check**: Ensure pywin32 is installed: `pip install pywin32`

### Service Won't Start
- **Check logs**: Look at `flask_service.log` in the webapp directory
- **Test manually**: Run `python run.py` to test the app
- **Check paths**: Ensure all file paths are correct

### Can't Access Web App
- **Check firewall**: Windows Firewall might be blocking port 5000
- **Check service status**: Run `python flask_service.py debug`
- **Check logs**: Look at `flask_service.log`

### Windows Firewall Configuration

If you can't access the app from other computers:

1. **Open Windows Defender Firewall**
2. **Click "Advanced settings"**
3. **Create new Inbound Rule**
   - Rule Type: Port
   - Protocol: TCP
   - Port: 5000
   - Action: Allow the connection
   - Profile: All profiles
   - Name: "Resume Tailor AI"

## Service Configuration

The service is configured to:
- ✅ **Auto-start** with Windows
- ✅ **Run in background** without user login
- ✅ **Listen on all interfaces** (0.0.0.0:5000)
- ✅ **Log to file** (flask_service.log)
- ✅ **Production mode** (debug=False)

## Files Overview

- `flask_service.py` - Windows service implementation
- `run.py` - Flask application runner
- `app.py` - Main Flask application
- `install_service.ps1` - PowerShell installation script
- `install_service.bat` - Batch installation script
- `uninstall_service.bat` - Batch uninstallation script
- `test_app.bat` - Test script for manual testing

## Uninstalling the Service

### Quick Uninstall
- **Right-click on `uninstall_service.bat`**
- **Select "Run as administrator"**

### Manual Uninstall
```cmd
python flask_service.py stop
python flask_service.py remove
```

## Success Indicators

✅ Service installs without errors
✅ Service starts successfully
✅ Web app accessible at http://localhost:5000
✅ Service appears in Windows Services (services.msc)
✅ Service shows as "Running" status
✅ Log file shows successful startup messages

## Next Steps

Once installed as a service:
1. ✅ Test the web interface
2. ✅ Configure Windows Firewall if needed
3. ✅ Set up any network access requirements
4. ✅ Monitor the service logs periodically

The Resume Tailor AI will now start automatically with Windows and be available 24/7!
