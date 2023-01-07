import argparse,os;
class Argv:
    def __init__(self,_file_:str,pwd:str) -> None:
        self.parser = argparse.ArgumentParser(os.path.basename(_file_));
        '''
            是否有工作目录
        '''
        self.pwd = pwd;
    def start(self) -> argparse.Namespace:
        '''
            若无工作目录初始化 init
        '''
        if not self.pwd:
            self.parser.add_argument('init',default='init',type=all)
            self.parser.add_argument('-w','--work',type=str,help='work directory')

        '''
            startup mode
             - server
             - console
        '''
        self.parser.add_argument('-m','--mode',type=str,help='startup mode')

        '''
            run in browser
        '''
        self.parser.add_argument('-p','--port',type=int,help="web server port")

        # export file handle
        '''
            export info
        '''
        self.parser.add_argument('-e','--export',type=str,help='export your info in info.qc, -e <filename=info.qc>');
        '''
            load info
        '''
        self.parser.add_argument('-l','--load',type=str,help='load your info file, -l <filename>');

        arg = self.parser.parse_args();


        return arg;