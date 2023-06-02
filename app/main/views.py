from flask import request,current_app
from flask import render_template
from flask_login import login_required
from flask_login import current_user

from . import main

@main.route('/',methods=['GET','POST'])
@login_required
def index():
    datas = {
        'permission' : current_user.permission,
        'context' : {
            'Test': {
                'type': 'dir',
                'keys': ['CTF','Python','测试'],
                'link': '/editor'
            },
            'Inner文章内容内容内容内容':{
                'type': 'article',
                'keys': ['Web','Math','code','markdown'],
                'author': 'C4skg',
                'time': '2023-06-01',
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            }
        }
    }

    return render_template('index.html',**datas);