import os,yaml;
from core.argv import Argv;
from core.basic import *;
from core.userProcess import Processor;


def main():
    if not usableFile("config/config.yaml"):
        conf = open('config/config.yaml','w',encoding='UTF-8')
        n_data = {
            'work_space': '',
            'time': getTime()
        }
        yaml.dump(n_data,conf);
        conf.close();

    conf = open('config/config.yaml','r',encoding='UTF-8')
    datas = yaml.safe_load(conf);

    if datas != None and datas.get('work_space') and datas['work_space'] != '':
        create = Argv(__file__,datas['work_space'])
    else:
        create = Argv(__file__,None);

    userIn = create.start();
    
    factory = Processor(userIn);
    factory.start();

if __name__ == '__main__':
    main();
