from flask import request,current_app
from flask_login import current_user
from flask_login import login_user,logout_user

from . import api

@api.route('/login')
def login():
    return request.url;