from flask import session,g
from flask import redirect,url_for,request

from . import api

@api.route('/create')
def create():
    return 'create';