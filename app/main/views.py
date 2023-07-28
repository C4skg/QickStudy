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
    
    data = {
        'user': User.query.filter_by(id=article.userId).first(),
        'article': article,
        'tips': {
            'enable': False,
            'type': ArticleStatus.Desc[article.status]['color'],
            'context': ArticleStatus.Desc[article.status]['desc']
        }
    }

    if article.status == ArticleStatus.NORMAL:
        pass;
    
    elif (
        article.status == ArticleStatus.DRAFT
        or
        article.status == ArticleStatus.PRIVATE
    ):
        if current_user.is_authenticated:
            if current_user.id == article.userId:
                data['tips']['enable'] = True
            else:
                abort(404)
        else:
            abort(404);
    elif (
        article.status == ArticleStatus.WAIT
        or 
        article.status == ArticleStatus.NOTPASS
    ):
        if current_user.is_authenticated:
            if(
                current_user.permission >= Permission.CONTROL
                or
                current_user.id == article.userId
            ):
                data['tips']['enable'] = True
            else:
                abort(404);
        else:
            abort(404);

    
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