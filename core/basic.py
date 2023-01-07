import time,os;

def getTime()-> str:
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());

def usableFile(path) -> bool:
    return os.access(path,os.R_OK);

def useableDir(path) -> bool:
    path = os.path.abspath(path);
    return os.access(path,os.F_OK);