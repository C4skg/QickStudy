import time,os;
import pyfiglet;
from termcolor import colored;
from colorama import *
from random import randint;
from hashlib import md5;

init(autoreset=True)

INFO_TXT = Fore.GREEN;
WARNING_TXT = Fore.RED; 

def getTime()-> str:
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());

def usableFile(path) -> bool:
    return os.access(path,os.R_OK);

def useableDir(path) -> bool:
    if path == None:
        return False;
    path = os.path.abspath(path);
    return os.access(path,os.F_OK);

def createDir(path,dirName) -> bool:
    if useableDir(path):
        try:
            os.mkdir(pathJoin(path,dirName));
            return True;
        except:
            pass;
    return False;

def isCleanDir(path) -> bool:
    if useableDir(path):
        return True if  os.listdir(path) == 0 else False;

    return False

def pathJoin(path:str,path2:str="") -> str:
    if path2 != "":
        return os.path.abspath(os.path.join(path+"/"+path2));
    else:
        return os.path.abspath(os.path.join(path));

def qcInfo(arg,end:str='\n'):
    Info = Fore.GREEN;            # 提示信息颜色
    print(Info + str(arg),end=end);

def qcWarning(arg,end:str='\n'):
    Warning = Fore.RED;            # 提示信息颜色
    print(Warning + str(arg),end=end);


def getRandInt(start:int,end:int) -> int:
    return randint(start,end);

def md5Enc_(text:str,key:str=''):
    text = text + key;
    return md5(text.encode()).hexdigest();

def showInfos():
    render = "QickTools";
    fonts = pyfiglet.FigletFont.getFonts();
    random = getRandInt(0,len(fonts));
    infos =  INFO_TXT + "[%s] Useage: `python3 QickTools.py -h` to get help" % getTime();
    f = pyfiglet.Figlet(font=fonts[random])
    print(colored("Welcome！ \n\n" + f.renderText(render) + '\n' + infos,'blue', 'on_grey', ['bold']));