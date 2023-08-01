from flask import request,current_app
from flask import abort,render_template,redirect,url_for
from flask import json
from flask_login import current_user
from flask_login import login_required

from copy import deepcopy

from .. import db
from ..responseData import articleResponse
from ..models import User,Article,Art_types
from ..models import ArticleStatus,Permission,EventID
from ..func import getLocalNumber

from . import server

@server.route('/article/create')
@login_required
def create():
    '''
        This api is to create a new draft
        if your draft's number is more than 3,
        we will back the last draft you created
        else, we will create for you a new one
    '''
    if current_user.permission < Permission.USER:
        abort(403);

    draft = current_user.article.filter_by(status=ArticleStatus.DRAFT).all();
    if len(draft) >= 3:
        data = {
            'status': 'error',
            'message': '你的草稿容量已达上限，请删除一篇草稿或发布草稿后再试',
            'route': url_for("server.editor",id=draft[-1].id)
        }
        return render_template('info.html',**data);
    else:
        return redirect(
            url_for("server.editor")
        )



@server.route('/article/editor/<id>')
@server.route('/article/editor')
@login_required
def editor(id:int=None):
    '''
        @param: <id:int>
        @desc: id is article's id
    '''
    if current_user.permission < Permission.USER:
        abort(403);
    
    #* if id is None,we will create a new article as draft
    if  id == None:
        draft = current_user.article.filter_by(status=ArticleStatus.DRAFT).all();
        if len(draft) >= 3:
            return redirect(
                url_for("server.editor",id=draft[-1].id)
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
                url_for("server.editor",id=article.id)
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
        "ArticleStatus": ArticleStatus,
        "Permission": Permission,
        "ArticleType": Art_types.query.all()
    }

    return render_template('article/create.html',**data);


@server.route('/article/save',methods=['POST'])
@login_required
def save():
    '''
        This api is save article
        @param: id - article's id
        @param: title - article's title
        @param: context - article's context
        @param: tId - article's status
        @param: typeId - article's typeId
    '''
    if current_user.permission < Permission.USER:
        return articleResponse['7003']

    id = request.form.get('id',None,type=int)
    if id:
        article = current_user.article.filter_by(id=id).first();
        if not article:
            return articleResponse['7002'];
    else:
        return articleResponse['7002']

    title = request.form.get('title',None,type=str);
    if not title or title == '':
        return articleResponse['7002']

    context = request.form.get('context',None,type=str);
    if not context or context == '':
        return articleResponse['7002']

    tId = request.form.get('tId',None,type=int);
    if not tId:
        return articleResponse['7002']
    
    typeId = request.form.get('typeId')
    if not typeId:
        return articleResponse['7002'] 

    if current_user.permission >= Permission.CONTROL:
        if (
            current_user.id != article.userId
            and
            tId == ArticleStatus.PRIVATE
        ):
            return articleResponse['7003']
    else:
        if tId == ArticleStatus.NORMAL or tId == ArticleStatus.NOTPASS:
            return articleResponse['7003']
        if article.status == ArticleStatus.WAIT:
            _clone = deepcopy(articleResponse['7001'])
            _clone['message'] = "目前状态为审核,暂无法修改状态"
            return _clone

    titleUpdate = article.updateTitle(title);
    contextUpdate = article.updateContext(context);
    statusUpdate = article.updateStatus(tId);
    typeUpdate = article.updateType(typeId);
    print(typeUpdate)
    if (
        titleUpdate and
        contextUpdate and 
        statusUpdate and
        typeUpdate
    ):
        print('commit')
        db.session.commit();
        _clone = deepcopy(articleResponse['7000'])
        _clone['route'] = url_for('main.detail',id=article.id);
        return _clone;

    else:
        pass;
    
    return articleResponse['7001']


@server.route('/article/c_status',methods=['POST'])
@login_required
def changeStatus():
    '''
        This api could change the article state
        
        @param: id - article's id
        @param: tId - target state id
    '''
    if current_user.permission < Permission.USER:
        return articleResponse['7003'];

    id = request.form.get('id',None,type=int);
    tId = request.form.get('tId',None,type=int);
    if not tId or not id:
        return articleResponse['7002']
    
    if current_user.permission >= Permission.CONTROL:
        if tId == ArticleStatus.PRIVATE:
            return articleResponse['7003']
            
        article = Article.query.filter_by(id=id).first();
    
    else:
        if tId == ArticleStatus.NORMAL or tId == ArticleStatus.NOTPASS:
            return articleResponse['7003']
        
        article = current_user.filter_by(id=id).first();

    if article:
        t = article.updateStatus()
        if t:
            db.session.commit();
            return articleResponse['7000'];
    else:
        pass;

    return articleResponse['7001'];

    


@server.route('/article/getArticle')
def getArticle():
    page = request.args.get('page',1,type=int);
    page = 1 if page <= 0 else page;
    articleList = Article.query.filter_by(status=ArticleStatus.NORMAL).order_by(Article.id.desc()).offset((page-1)*10).limit(10).all()
    data = {
        'length': len(articleList),
        'articles':{}
    }
    for i in articleList:
        user = User.query.filter_by(id=i.userId).first();
        temp = {
            'id': i.id,
            'cover': url_for('themes.upload',path=i.cover) if i.cover else None,
            'title': i.title,
            'context': i.context[:300]+'...',
            'auth':{
                'url': url_for('auth.userInfo',id=user.id),
                'username': user.username,
                'logo': url_for('server.logo',id=user.id)
            },
            'lasttime': i.lastTime.strftime("%Y/%m/%d"),
            'agree': getLocalNumber(i.agree),
            'watch': getLocalNumber(i.watch),
            'detailPath': url_for('main.detail',id=i.id)
        }

        data['articles'][i.id] = temp;
    
    return json.dumps(data);