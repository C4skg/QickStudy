from flask import request,current_app
from flask import abort,render_template,redirect,url_for
from flask_login import current_user
from flask_login import login_required

from base64 import b64encode

from .. import db
from ..models import User,Article
from ..models import ArticleStatus,Permission,EventID

from . import server


@server.route('/create/<id>')
@server.route('/create')
@login_required
def create(id:int=None):
    '''
        @param: <id:int>
        @desc:id is article's id
    '''
    if current_user.permission < Permission.USER:
        abort(403);
    
    #* if id is None,we will create a new article as draft
    if  id == None:
        draft = current_user.article.filter_by(status=ArticleStatus.DRAFT).all();
        if len(draft) >= 10:
            return redirect(
                url_for("server.create",id=draft[-1].id)
            )
        else:
            article = Article(
                title = "",
                context = '''%s''' % open('app/static/context/first.md',encoding='utf-8').read()
            )
            current_user.article.append(article);
            db.session.merge(current_user)
            db.session.commit();
            return redirect(
                url_for("server.create",id=article.id)
            )
        
    #* if article id matches
    article = Article.query.filter_by(id=id).first();
    if article:
        if current_user.id != article.userId:
            abort(403);
    else:
        abort(404)

    data = {
        'user': current_user,
        "article": article,
        "ArticleStatus": ArticleStatus
    }

    return render_template('create.html',**data);