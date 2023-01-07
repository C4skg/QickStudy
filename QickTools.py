import os;
from core.argv import Argv;
from core.basic import *;
from core.Allocate import Allocate;
from core.config import *;
import random
def main():
    if not usableFile("config/config.yaml"):
        file_init('config.yaml');
    datas = safe_load('config.yaml')

    if datas != None and datas.get('work_space') and datas['work_space'] != '':
        create = Argv(__file__,datas['work_space'])
    else:
        create = Argv(__file__,None);

    userIn = create.start();
    
    factory = Allocate(userIn);
    print(userIn)
    factory.start();

if __name__ == '__main__':
    main();