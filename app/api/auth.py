from flask import request

from . import api

@api.route('/login')
def login():
    return request.url;