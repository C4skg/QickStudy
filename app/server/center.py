from flask import request,current_app
from flask import render_template,url_for,redirect
from flask_login import current_user
from flask_login import login_required

from ..models import User,Article,Art_types
from ..models import ArticleStatus,Permission,EventID

from . import server


# 创作中心视图
@server.route('/article/center')
@login_required
def center():
    data = {
        "user": current_user,
        "ArticleStatus": ArticleStatus,
        "args": request.args.to_dict()
    }

    gettype = request.args.get("type","all");
    if gettype == "all":
        articles =  Article.query.order_by(Article.id.desc()).all()
    elif gettype == "wait":
        articles =  Article.query.filter_by(status=ArticleStatus.WAIT).order_by(Article.id.desc()).all()
    elif gettype == "private":
        articles =  Article.query.filter_by(status=ArticleStatus.PRIVATE).order_by(Article.id.desc()).all()
    elif gettype == "draft":
        articles =  Article.query.filter_by(status=ArticleStatus.DRAFT).order_by(Article.id.desc()).all()
    else:
        return redirect(
            url_for(
                "server.center",
                type="all"
            )
        )
    
    data["articles"] = articles;

    return render_template(
        "article/center.html",
        **data
    );