import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import subprocess
import sys
import os

class FlaskService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskAppService"       # Service name
    _svc_display_name_ = "Flask App Service"  # Name in Services.msc
    _svc_description_ = "Runs a Flask app as a Windows service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, 'Service stopping'))
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.start_flask()

    def start_flask(self):
        try:
            # Get the directory where this script is located
            service_dir = os.path.dirname(os.path.abspath(__file__))
            python_exe = sys.executable
            app_path = os.path.join(service_dir, "run.py")
            
            # Set environment variables for production
            env = os.environ.copy()
            env['FLASK_DEBUG'] = 'False'
            env['FLASK_HOST'] = '0.0.0.0'
            env['FLASK_PORT'] = '5000'

            log_file = os.path.join(service_dir, "flask_service.log")
            
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STARTED,
                                  (self._svc_name_, f'Starting Flask app from {app_path}'))
            
            with open(log_file, "a") as f:
                f.write(f"\n=== Service started at {__import__('datetime').datetime.now()} ===\n")
                f.write(f"Python executable: {python_exe}\n")
                f.write(f"App path: {app_path}\n")
                f.write(f"Working directory: {service_dir}\n")
                f.flush()
                
                self.process = subprocess.Popen(
                    [python_exe, app_path],
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    cwd=service_dir,
                    env=env
                )

            # Wait for the stop event
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            
            # Terminate the process when stopping
            if self.process:
                self.process.terminate()
                self.process.wait()
                
        except Exception as e:
            servicemanager.LogMsg(servicemanager.EVENTLOG_ERROR_TYPE,
                                  servicemanager.PYS_SERVICE_STOPPED,
                                  (self._svc_name_, f'Error: {str(e)}'))


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(FlaskService)
