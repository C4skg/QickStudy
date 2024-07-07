from flask import render_template,abort,url_for,redirect
from flask import session,request
from flask_login import current_user
from flask_login import login_required

from ..models import Permission,ArticleStatus
from ..models import User,Article

from . import admin


@admin.route('/')
@login_required
def index():
    
    if current_user.permission < Permission.ADVENCE:
        abort(404);

    data = {
        "user": current_user,
        "ArticleStatus": ArticleStatus,
        "Permission": Permission,
        "args": request.args.to_dict(),
        "userlist": None,
        "Articles": Article,
    }

    getaction = request.args.get("action");
    gettype = request.args.get("type");
    if getaction == "articles":
        status = ArticleStatus.NORMAL;
        if gettype == "release":
            pass;
        elif gettype == "wait":
            status = ArticleStatus.WAIT;
        else:
            return redirect(
                url_for(
                    "admin.index",
                    action="articles",
                    type="release"
                )
            )
        # if current_user.permission >= Permission.ADMIN:
        #     '''
        #         ADMIN USER could manager all articles
        #     '''
            

        # elif current_user.permission >= Permission.CONTROL:
        #     '''
        #         CONTROL USER could manger part articles
        #     '''
        #     pass;

        articles = Article.query.filter_by(status=status).order_by(Article.id.desc()).all();
        

        data["articles"] = articles;

    elif getaction == "permission":
        if current_user.permission < Permission.ADMIN:
            return redirect(
                url_for(
                    "admin.index",
                    action="articles"
                )
            )
        
        data["userlist"] = User;
        if gettype == "control":
            users = User.query.filter(User.permission >= Permission.CONTROL).order_by(User.id).all();
        elif gettype == "normal":
            users = User.query.filter(User.permission.between(Permission.USER,Permission.ADVENCE)).order_by(User.id).all();
        elif gettype == "base":
            users = User.query.filter(User.permission == Permission.BASE).order_by(User.id).all();
        else:
            return redirect(
                url_for(
                    "admin.index",
                    action="permission",
                    type="control"
                )
            )
        data["users"] = users;

    else:
        return redirect(
            url_for(
                "admin.index",
                action="articles"
            )
        )

    return render_template("admin/index.html",**data);