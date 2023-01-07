from flask import Flask,render_template,url_for,session;
import darkdetect
import uuid;

template_folder = "../templates"

static_folder = "../static"

app = Flask(__name__,template_folder=template_folder,static_folder=static_folder)

app.config['SECRET_KEY'] = str( uuid.uuid4() ).replace('-','');



@app.route('/')
def main():
    if darkdetect.isDark():
        session['dark'] = "1";
    else:
        session['dark'] = "0";
    data = {
        'darkMode':  "dark" if session.get('dark') == "1" else ""
    }
    return render_template('index.html',**data);


@app.errorhandler(404)
def error_404(error_info):
    file = open("templates/404.html",'r',encoding='utf-8').read();
    return render_template("index.html",page=file),404;

def run(port=8080,debug:bool = False):
    app.run('127.0.0.1',port,debug=debug);