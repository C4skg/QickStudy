from flask import abort,redirect,url_for
from flask import session
from flask_login import current_user
from ..models import User

from . import admin

@admin.before_request
def before_request():
    if current_user.isAdministrator():
        pass;
    else:
        abort(404)