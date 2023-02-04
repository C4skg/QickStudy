import core.basic as Basic
from core.config import *

class WokeSpaceDataAllocate:
    '''
        以文件形式存放万物
        目录: 单纯目录，可读取 readme.md
        工具: 也是目录形式，但是目录中多了个 .type 文件用于识别属于工具栏目
    '''
    def __init__(self,name:str,path:str) -> None:
        self.path = name;
        if useableDir(path):
            self.path = path;
        else:
            qcWarning("work path error");
            exit(0);

    def createDir(self,dirName:str) -> int:
        '''
            @return:{
                -1: 失败
                 0: 目录存在
                 1: 成功
            }
        '''
        status = -1;
        if useableDir(dirName):
            status = 0;
        else:
            status = int(Basic.createDir(self.path,dirName));
        return status;
    
    # def createTools()