from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    session,
    request
)
from core.woker import WorkSpaceDataAllocate;
from core.basic import md5Enc_
from core.config import *;

import uuid;


template_folder = "../templates"
static_folder = "../static"

class ServerPanInfo:
    def __init__(self) -> None:
        self.key = str( uuid.uuid4() ).replace('-','');
        self.root = False;

ServiceInfo = ServerPanInfo();

app = Flask(__name__,template_folder=template_folder,static_folder=static_folder)
app.config['SECRET_KEY'] = ServiceInfo.key;


@app.errorhandler(404)
def error_404(error_info):
    return redirect(url_for('404'));


@app.before_request
def accessFilter():
    url_filter = [
        '', # route = '/'
        'api',
        'editor'
    ]
    if not ServiceInfo.root:
        router = request.url.split('/')[3];
        #登录验证
        for url in url_filter:
            if router == url:
                if not is_login():
                    print(router);
                    return redirect(url_for('login',ori=router));
    
@app.route('/',endpoint='/',methods=['GET'])
def main():
    datas = {
        "root" : ServiceInfo.root,
        'context' : {
            'Test': {
                'type': 'dir',
                'keys': ['CTF','Python','测试'],
                'link': '/editor'
            },
            'Inner':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'zxzcs':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'zxc':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'we':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'qsxc':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'jrt':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'rty':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'usef':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'were':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'wfdvbsefere':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            'gnrtyyd4rtgrdydrfdrgdrgdr':{
                'type': 'tools',
                'keys': ['Web','Math','code','markdown'],
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            }
        }
    }

    return render_template('index.html',**datas);

@app.route('/editor',methods=['GET','POST'])
def editor():
    return render_template('editor.html');


@app.route('/upload',methods=['POST'])
def fileUploaded():
    data = (request.files['file[]'].stream.read());
    filename = request.files['file[]'].filename;

    return 'ok';

@app.route('/login',endpoint='login',methods=['POST','GET'])
def login():
    if is_login():
        return redirect(url_for('/'));

    if request.form.get('login'):
        response = {
        
        }
        '''
            login
        '''
        response['loginStatus'] = False;
        username = request.form.get('username');
        password = request.form.get('password');
        if username and password:
            if login_verify(username,password):
                response['loginStatus'] = True;
                response['router'] = request.args.get('ori','/');
        '''
            return paramter;
        '''
        return response;
    
    datas = {

    }
    return render_template('login.html',**datas)

@app.route('/404',endpoint='404',methods=['GET','POST'])
def error_404():
    return render_template('404.html');

@app.route('/api',methods=['POST'])
def api():
    response = {
        "status" : 'ok'
    }
    # if ServiceInfo.root and 
    
    #*添加新目录

    #*添加新工具

    #*添加目录说明

    '''
        return paramter;
    '''
    return response;

def is_login() -> bool:
    value = session.get('User');
    if not value:
        return False;
    else:
        try:
            value = str(value);
            conf = safe_load('config');
            user = conf.get('Username');
            return user == value;
        except:
            return False;

def login_verify(username:str,password:str) -> bool:
    username = md5Enc_(username.strip());
    password = md5Enc_(password.strip());
    conf = safe_load('config');
    user1 = conf.get('Username');
    pwd1 = conf.get('Password');
    if username == user1 and password == pwd1:
        session['User'] = username;
        # response['loginStatus'] = True;
        return True;
    else:
        # response['loginStatus'] = False;
        return False;

def run(ip:str='127.0.0.1',port:int=8080,debug:bool = False):
    if ip == '127.0.0.1':
        ServiceInfo.root = True;
    
    app.run(ip,port,debug=debug);
    