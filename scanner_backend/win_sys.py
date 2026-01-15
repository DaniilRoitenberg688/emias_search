import sys
import os
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import time
import logging
import signal
import psutil
from pathlib import Path

class ScannerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ScannerBackendService"
    _svc_display_name_ = "Scanner Backend Service"
    _svc_description_ = "Service for document scanning backend"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None
        self.is_running = True
        self.logger = None
        
    def SvcStop(self):
        """Остановка службы - вызывается Windows"""
        self.log_message("Received stop signal from Windows...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        
        # Останавливаем дочерние процессы
        self.stop_application()
        
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.log_message("Service stopped successfully")
        
    def SvcDoRun(self):
        """Основной метод запуска службы"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        self.setup_logging()
        self.log_message("Service starting...")
        
        try:
            self.main()
        except Exception as e:
            self.log_message(f"Service error: {str(e)}")
            import traceback
            self.log_message(traceback.format_exc())
        
    def setup_logging(self):
        """Настройка логгирования"""
        log_dir = Path("C:/ScannerServiceLogs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "scanner_service.log"),
                logging.StreamHandler()  # Для отладки
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def log_message(self, message):
        """Логирование сообщений"""
        if self.logger:
            self.logger.info(message)
        else:
            print(message)
    
    def stop_application(self):
        """Остановка приложения и всех дочерних процессов"""
        self.log_message("Stopping application...")
        
        if self.process:
            try:
                # Получаем PID основного процесса
                pid = self.process.pid
                self.log_message(f"Main process PID: {pid}")
                
                # Находим и останавливаем все дочерние процессы
                try:
                    parent = psutil.Process(pid)
                    children = parent.children(recursive=True)
                    
                    self.log_message(f"Found {len(children)} child processes")
                    
                    # Останавливаем дочерние процессы
                    for child in children:
                        try:
                            self.log_message(f"Stopping child process: {child.pid} - {child.name()}")
                            child.terminate()
                        except:
                            try:
                                child.kill()
                            except:
                                pass
                    
                    # Ждем завершения дочерних процессов
                    gone, alive = psutil.wait_procs(children, timeout=3)
                    
                    # Останавливаем родительский процесс
                    self.log_message(f"Stopping main process: {pid}")
                    parent.terminate()
                    
                    # Ждем завершения
                    parent.wait(timeout=5)
                    
                except psutil.NoSuchProcess:
                    self.log_message("Process already terminated")
                
                # Дополнительно: останавливаем по имени
                self.kill_process_by_name("app.exe")
                self.kill_process_by_name("NAPS2.Console.exe")
                self.kill_process_by_name("uvicorn.exe")
                
            except Exception as e:
                self.log_message(f"Error stopping process: {e}")
        else:
            self.log_message("No process to stop")
    
    def kill_process_by_name(self, process_name):
        """Убить процесс по имени"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                    self.log_message(f"Killing process by name: {process_name} (PID: {proc.info['pid']})")
                    try:
                        proc.terminate()
                        proc.wait(timeout=3)
                    except:
                        try:
                            proc.kill()
                        except:
                            pass
        except Exception as e:
            self.log_message(f"Error killing process {process_name}: {e}")
        
    def main(self):
        """Основная логика службы"""
        # Определяем путь к app.exe
        if getattr(sys, 'frozen', False):
            exe_dir = Path(sys.executable).parent
        else:
            exe_dir = Path(__file__).parent
            
        app_path = exe_dir / "app.exe"
        
        self.log_message(f"Application path: {app_path}")
        
        if not app_path.exists():
            self.log_message(f"ERROR: {app_path} not found!")
            return
        
        os.chdir(str(exe_dir))
        
        # Основной цикл службы
        while self.is_running:
            try:
                self.log_message(f"Starting application: {app_path.name}")
                
                # Запускаем процесс с отдельной консолью
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                
                self.process = subprocess.Popen(
                    [str(app_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    bufsize=1,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # Для корректного завершения
                )
                
                self.log_message(f"Process started with PID: {self.process.pid}")
                
                # Мониторим вывод
                self.monitor_process()
                
                # Если служба еще работает, перезапускаем
                if self.is_running:
                    self.log_message("Application stopped. Restarting in 3 seconds...")
                    for i in range(3):
                        if not self.is_running:
                            break
                        time.sleep(1)
                        
            except Exception as e:
                self.log_message(f"Error in main loop: {e}")
                if self.is_running:
                    time.sleep(5)
    
    def monitor_process(self):
        """Мониторинг вывода процесса"""
        if self.process and self.process.stdout:
            try:
                # Читаем вывод в реальном времени
                for line in iter(self.process.stdout.readline, ''):
                    if not self.is_running:
                        break
                    if line.strip():
                        self.log_message(f"[APP] {line.strip()}")
                
                # Ждем завершения процесса с таймаутом
                while self.is_running:
                    try:
                        return_code = self.process.wait(timeout=1)
                        self.log_message(f"Application exited with code: {return_code}")
                        break
                    except subprocess.TimeoutExpired:
                        continue
                        
            except Exception as e:
                self.log_message(f"Error monitoring process: {e}")

if __name__ == '__main__':
    # Устанавливаем обработчик Ctrl+C
    import signal as py_signal
    def signal_handler(sig, frame):
        print("Ctrl+C pressed, stopping...")
        sys.exit(0)
    
    py_signal.signal(py_signal.SIGINT, signal_handler)
    
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ScannerService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ScannerService)