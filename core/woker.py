import core.basic as Basic
from core.config import *


class createInfo:
    def __init__(self,type:int,path:str,name) -> None:
        self.type = type
        self.path = path
        self.name = name

class WokeSpaceDataAllocate:
    '''
        以文件形式存放万物
        目录: 单纯目录，可读取 readme.md
        工具: 也是目录形式，但是目录中多了个 .type 文件用于识别属于工具栏目
    '''
    def __init__(self,name:str,path:str) -> None:
        self.name = name;
        if useableDir(path):
            self.path = path;
        else:
            self.path = '/';

    

    def createTools(
            toolName:str,
            
    ) -> bool:
        
        return 0;