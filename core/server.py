from flask import Flask,render_template,url_for,session,redirect,request;
from Crypto.Cipher import AES
import uuid;

from core.config import safe_load;

template_folder = "../templates"

static_folder = "../static"

app = Flask(__name__,template_folder=template_folder,static_folder=static_folder)
KEY = str( uuid.uuid4() ).replace('-','');
app.config['SECRET_KEY'] = KEY;


@app.route('/')
def main():
    data = safe_load('config');
    user = session.get('user')
    if user== None or user != data.get('user'):
        location = url_for('login')
        return redirect(location)
    if session.get('dark') == None:
        session['dark'] = '0'
    data = {
        'darkMode':  "dark" if session.get('dark') else ""
    }
    return render_template('index.html',**data);

@app.route('/login',endpoint='login')
def login():
    data = {

    }
    return render_template('login.html',**data)

@app.route('/api',methods=['GET','POST'])
def api():
    if request.args.get('style'):
        style = request.args.get('style');
        if style == 'dark':
            session['dark'] = True;
        else:
            session['dark'] = False;
        return 'mode changed';
    return '';

@app.errorhandler(404)
def error_404(error_info):
    file = open("templates/404.html",'r',encoding='utf-8').read();
    return render_template("index.html",page=file),404;

def run(port=8080,debug:bool = False):
    app.run('127.0.0.1',port,debug=debug);