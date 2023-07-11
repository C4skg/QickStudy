from flask import abort,redirect,url_for
from flask_login import current_user
from flask_login import login_required

from . import admin

@admin.before_request
def before_request():
    if current_user.is_authenticated:
        if current_user.isAdministrator():
            pass;
        else:
            abort(404)
    else:
        return redirect(url_for('auth.login'))