'''
It works in windows
'''
import sys,ctypes
SYSTEM = sys.platform

if SYSTEM == 'win32':
    import win32api as winapi
    import win32con as wincon

class SystemRunnerImprove():
    def __init__(self) -> None:
        self.run_as_root();
    def Admin(self):
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except:
            return False;
    def run_as_root(self):
        if not self.Admin():
            T = 1;
            while(T):
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:
            pass;