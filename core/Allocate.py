import argparse;

from core.basic import *;
from core.config import *;
import core.server as Web;

class Allocate:
    def __init__(self,args:argparse.Namespace) -> None:
        self.args = vars(args);
    
    def start(self):
        showInfos();
        if self.args.get('init'):
            if self.args['work']:
                dirs = self.args['work'];
                '''
                    生成用户
                '''
                user = input(WARNING_TXT + 'input your username:');
                pwd = input(WARNING_TXT + 'and input your password:');
                pwd1 = input(WARNING_TXT + 'repeat your password:');
                if pwd == pwd1:
                    w2Config('config','Username',user);
                    w2Config('config','Password',pwd1);
                else:
                    qcWarning('pwd error!');
                    exit(0);

                if not useableDir(dirs):
                    os.mkdir(dirs);
                w2Config('config','work_space',dirs)
                qcInfo('create ok!');
            else:
                qcWarning('plz input your work dir!');
                return 0;
        else:
            mode = self.args.get('mode');
            if mode == 'server':
                port = self.args.get('port')
                if port:
                    Web.run(port);
                else:
                    Web.run();
                pass;
            elif mode == 'console':
                pass;

