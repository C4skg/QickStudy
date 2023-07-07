from flask import request,current_app
from flask import render_template,url_for
from flask_login import login_required
from flask_login import current_user

from . import main

@main.route('/',methods=['GET','POST'])
@login_required
def index():
    datas = {
        'user': current_user,
        'context' : {
            'Inner文章内容内容内容内容':{
                'type': 'article',
                'author': 'C4skg',
                'time': '2023-06-01',
                'level': '0',
                'readme': open(f'WorkSpace/Test.md','r',encoding='utf-8').read()
            },
            '紧急公告':{
                'type': 'notice',
                'author': 'Admin',
                'time': '2023-06-01',
                'level': 99,
                'context': open(f'WorkSpace/notice.md','r',encoding='utf-8').read()
            },
            '紧急公告2':{
                'type': 'notice',
                'author': 'Admin',
                'time': '2023-06-01',
                'level': 2,
                'context': open(f'WorkSpace/notice.md','r',encoding='utf-8').read()
            }
        }
    }
    

    return render_template('index.html',**datas);


@main.route('/about')
def about():
    data = {
        'title': '关于 QickStudy',
        'context': open('WorkSpace/about.md',encoding='utf-8').read()
    }
    return render_template('about.html',**data);