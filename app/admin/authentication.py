from flask import abort,redirect,url_for
from flask import session
from flask_login import current_user
from ..models import User

from . import admin

@admin.before_request
def before_request():
    user = session.get('user');
    # if not user :
    #     return redirect(url_for('auth.UserLogin'));
    # if user != 'C4skg':
    #     abort(403);