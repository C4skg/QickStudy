'''
It works in windows
'''
import sys
SYSTEM = sys.platform

if SYSTEM == 'win32':
    import win32api as winapi
    import win32con as wincon
    import ctypes
    import time

    class SystemRunnerImprove():
        def __init__(self) -> None:
            self.code = 0;
            self.run_as_root();
        def Admin(self):
            try:
                return bool(ctypes.windll.shell32.IsUserAnAdmin())
            except:
                return False;
        def run_as_root(self):
            if not self.Admin():
                T = 1;
                code = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1);
                while(T):
                    if code == 42:
                        self.code = code;
                        time.sleep(0.3);
                        break;
            else:
                self.code = 42;