from flask import abort,redirect,url_for
from flask import request
from flask_login import current_user
from flask_login import login_required

from .. import db
from ..models import User
from ..models import Permission
from ..responseData import adminAPIResponse
from . import admin

@admin.before_request
def before_request():
    if current_user.is_authenticated:
        pass;
    else:
        return redirect(url_for('auth.login'));


@admin.route('/api/permission/modification',methods=['POST'])
@login_required
def modify_permission():
    if not current_user.isAdministrator():
        return adminAPIResponse["8003"];

    uid = request.form.get('uid',None,type=int);
    permission = request.form.get('permission',None,type=int);

    if uid == None or permission == None:
        return adminAPIResponse["8002"];

    user = User.query.filter_by(id=uid).first();
    if not user:
        _clone = adminAPIResponse["8002"];
        _clone["message"] = "未找到该用户";
        return _clone;

    _result = user.modificationPermission(permission);
    if not _result:
        return adminAPIResponse["8001"];

    db.session.commit();
    return adminAPIResponse["8000"];