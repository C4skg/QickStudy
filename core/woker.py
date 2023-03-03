import core.basic as Basic
from core.config import *


class workInit:
    def __init__(self,dir:str,name:str) -> None:
        self.dir = dir
        self.name = name
        if not useableDir(dir):
            Basic.createDir(dir);
        elif not Basic.isCleanDir(dir):
            Basic.qcWarning('dir not clean');
            exit(0);
        
        

class createInfo:
    def __init__(self,type:int,path:str,name) -> None:
        self.type = type
        self.path = path
        self.name = name

class WorkSpaceDataAllocate:
    '''
        以文件形式存放万物
        目录: 单纯目录，可读取 readme.md
        工具: 也是目录形式，但是目录中多了个 .type 文件用于识别属于工具栏目
    '''
    def __init__(self,workDir:str) -> None:
        if Basic.useableDir(workDir):
            self.space = workDir;

    def createDir(
            
    ) -> int:
        return False;

    def createTools(
            toolName:str,
            
    ) -> bool:
        
        return 0;