from core.argv import Argv;
from core.basic import *;
from core.Allocate import Allocate;
from core.config import *;
# from core.sysControl import 

def main():
    if not usableFile("config/config.yaml"):
        file_init('config.yaml');
    datas = safe_load('config.yaml')
    if datas != None  and useableDir(datas.get('work_space')):
        create = Argv(__file__,datas['work_space'])
    else:
        create = Argv(__file__,None);
    userIn = create.inject();
    
    factory = Allocate(userIn);
    factory.start();

if __name__ == '__main__':
    main();