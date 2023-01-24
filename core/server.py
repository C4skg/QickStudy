import uuid;

from flask import Flask,render_template,url_for,session,redirect,request;

from core.basic import md5Enc_
from core.config import *;


template_folder = "../templates"
static_folder = "../static"

app = Flask(__name__,template_folder=template_folder,static_folder=static_folder)
KEY = str( uuid.uuid4() ).replace('-','');
app.config['SECRET_KEY'] = KEY;

@app.errorhandler(404)
def error_404(error_info):
    file = open("templates/404.html",'r',encoding='utf-8').read();
    return render_template("index.html",page=file),404;

@app.before_request
def accessFilter():
    url_filter = [
        '' # route = '/'
    ]
    router = request.url.split('/')[3];
    #登录验证
    for url in url_filter:
        if router == url:
            if not is_login():
                return redirect(url_for('login'));
    
@app.route('/',endpoint='/')
def main():
    datas = {
        
    }
    return render_template('index.html',**datas);

@app.route('/login',endpoint='login',methods=['POST','GET'])
def login():
    if is_login():
        return redirect(url_for('/'));
    datas = {

    }
    return render_template('login.html',**datas)


@app.route('/api',methods=['GET','POST'])
def api():
    response = {
        
    }
    '''
        login
    '''
    if request.form.get('login'):
        response['loginStatus'] = False;
        username = request.form.get('username');
        password = request.form.get('password');
        if username and password:
            if login_verify(username,password):
                response['loginStatus'] = True;

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
    app.run(ip,port,debug=debug);
