import time,os;
from colorama import *
init(autoreset=True)
def getTime()-> str:
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());

def usableFile(path) -> bool:
    return os.access(path,os.R_OK);

def useableDir(path) -> bool:
    path = os.path.abspath(path);
    return os.access(path,os.F_OK);

def createDir(path,dirName) -> bool:
    if useableDir(path):
        try:
            os.mkdir(pathJoin(path,dirName));
            return True;
        except:
            return False;

def pathJoin(path,fileName) -> str:
    return os.path.abspath(os.path.join(path+"/"+fileName));

def qcInfo(arg,end:str=''):
    Info = Fore.GREEN;            # 提示信息颜色
    print(Info + str(arg),end=end);

def qcWarning(arg,end:str=''):
    Warning = Fore.RED;            # 提示信息颜色
    print(Warning + str(arg),end=end);
        