import time,os;
import pyfiglet;
from termcolor import colored;
from colorama import *
from random import randint;
from hashlib import md5;
from socket import gethostbyname,gethostname;
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
            return False;

def pathJoin(path,fileName) -> str:
    return os.path.abspath(os.path.join(path+"/"+fileName));

def qcInfo(arg,end:str=''):
    Info = Fore.GREEN;            # 提示信息颜色
    print(Info + str(arg),end=end);

def qcWarning(arg,end:str=''):
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
    print(colored("Welcome use \n\n" + f.renderText(render) + '\n' + infos,'blue', 'on_grey', ['bold', 'blink']));

def getIp():
    return  gethostbyname(gethostname());