from flask import request,current_app
from flask import render_template,url_for,abort,render_template_string
from flask_login import login_required
from flask_login import current_user

from . import main
from ..models import Article,User
from ..models import Permission,ArticleStatus,UserExperience

@main.route('/',methods=['GET','POST'])
@login_required
def index():
    datas = {
        'user': current_user,
        'level': {
            'now': UserExperience.getLevel(current_user.userInfo[0].experience),
            'value': current_user.userInfo[0].experience
        },
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
        },
        'ArticleStatus': ArticleStatus
    }
    datas['level']['nextV'] = UserExperience.getNextValue(datas['level']['now'])
    datas['level']['length'] = (datas['level']['value'] / (1 if datas['level']['nextV'] == 0 else datas['level']['nextV'])) * 100
    


    return render_template('index.html',**datas);


@main.route('/detail/<id>')
def detail(id:None):
    article = Article.query.filter_by(id=id).first();
    if not article:
        abort(404);
    
    if article.status == ArticleStatus.NORMAL:
        pass;
    
    elif (
        article.status == ArticleStatus.DRAFT
        or
        article.status == ArticleStatus.PRIVATE
    ):
        if current_user.is_authenticated:
            if current_user.id == article.userId:
                pass;
            else:
                abort(404)
        else:
            abort(404);
    elif article.status == ArticleStatus.WAIT:
        if current_user.is_authenticated:
            if(
                current_user.permission >= Permission.CONTROL
                or
                current_user.id == article.userId
            ):
                pass;
            else:
                abort(404);
        else:
            abort(404);

    data = {
        'user': User.query.filter_by(id=article.userId).first(),
        'article': article
    }
    return render_template('article/detail.html',**data);

@main.route('/about')
def about():
    data = {
        'title': '关于 QickStudy',
        'context': open('WorkSpace/about.md',encoding='utf-8').read()
    }
    return render_template('about.html',**data);


@main.route('/help')
def help():
    data = {
        'title': '帮助中心',
        'context': ''''''
    }
    return render_template('about.html',**data);