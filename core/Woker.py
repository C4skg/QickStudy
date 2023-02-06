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
        absPath = pathJoin(self.path,dirName);
        '''
            @return:{
                -1: 失败
                 0: 目录存在
                 1: 成功
            }
        '''
        status = -1;
        if useableDir(absPath):
            status = 0;
        else:
            # ^ confirm not tools dir
            if self.typeDistinguish(absPath) == 0:
                status = int(Basic.createDir(self.path,dirName));
        return status;
    

    def createTools(
        self,
        toolsName:str,
        toolsPath:str,
        desc:str,
        toolsType:int=0,
        openWith:str=''
    )->bool:
        pass;

    def createDotType(self,path:str) -> bool:
        if useableDir(path):
            typed = pathJoin(path,'.type');
            try:
                file = open(typed,'rw');
                file.write("type:Tools");
                file.close();
                return True;
            except:
                pass;
        return False;

    def typeDistinguish(self,path:str) -> int:
        '''
            return: int{
                -1: require Failed
                0:  dir
                1:  tools
            }
        '''
        if useableDir(path):
            typed = pathJoin(path,'.type');
            if usableFile(typed):
                try:
                    data = open(typed,'rb').read().decode();
                    if 'Tools' in data:
                        return 1;
                except:
                    pass;
            else:
                return 0;
            
        return -1;

    # def createTools()