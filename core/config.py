import yaml;

from core.basic import *

PATH = 'config/';

def file_init(fileName:str) -> bool:
    fileName = yamlFill(fileName);
    conf = open(pathJoin(PATH , fileName),'w',encoding='UTF-8')
    n_data = {
        'work_space': '',
        'time': getTime()
    }
    yaml.dump(n_data,conf);
    conf.close();

def w2Config(fileName:str,key,value):
    '''
        追加 + 覆盖
    '''
    fileName = yamlFill(fileName);
    path = pathJoin(PATH , fileName);
    data = safe_load(fileName);
    data[key] = value;
    file = open(path,'w',encoding='UTF-8');
    yaml.dump(data,file,allow_unicode=True);
    file.close();

def safe_load(fileName:str):
    fileName = yamlFill(fileName);
    conf = open(pathJoin(PATH , fileName),'r',encoding='UTF-8');
    return yaml.safe_load(conf);

def yamlFill(fileName:str)-> str:
    if not fileName.endswith('.yaml'):
        return fileName + '.yaml'
    else:
        return fileName;