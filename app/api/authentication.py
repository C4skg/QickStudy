from flask import request,session
from flask import redirect,url_for

from . import api


@api.before_request
def before_request():
    user = session.get('user');
    if not user:
        return redirect(url_for("auth.UserLogin",router=request.url));