from flask import Flask,render_template,url_for;
import uuid;
app = Flask(__name__,template_folder='../templates',static_folder='../static')

@app.route('/')
def main():
    return render_template('index.html');


@app.errorhandler(404)
def error_404(error_info):
    return render_template("404.html",id=uuid.uuid4()),404;

def run(port=8080,debug:bool = False):
    app.run('127.0.0.1',port,debug=debug);