from flask import Flask,render_template,url_for,session,redirect,request;
from Crypto.Cipher import AES
import uuid;

from core.config import safe_load;

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
    user = session.get('user');
    router = request.url.split('/')[3];
    if session.get('dark') == None:
        session['dark'] = False;
    dark = session.get('dark');

@app.route('/')
def main():
    datas = {
        'darkMode':  "dark" if session.get('dark') else ""
    }
    return render_template('index.html',**datas);

@app.route('/login',endpoint='login')
def login():
    datas = {

    }
    return render_template('login.html',**datas)

@app.route('/api',methods=['GET','POST'])
def api():
    response = {
        
    }

    if request.form.get('style'):
        style = request.form.get('style');
        if style == 'dark':
            session['dark'] = True;
            response['mode'] = 'dark';
        else:
            session['dark'] = False;
            response['mode'] = 'light';

    return response;



def run(port=8080,debug:bool = False):
    app.run('127.0.0.1',port,debug=debug);