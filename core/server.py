from flask import Flask,render_template,url_for;

app = Flask(__name__,template_folder='../templates',static_folder='../static')

@app.route('/')
def main():
    return render_template('index.html');

def run(port=8080,debug:bool = False):
    app.run('127.0.0.1',port,debug=debug);