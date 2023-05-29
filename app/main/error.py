from flask import render_template

from ..config import html
from . import main

ERROR_INFO = {
    'code': 0,
    'title': '',
    'tips': ''
}

@main.app_errorhandler(400)
def forbidden(e):
    ERROR_INFO['code'] = 400;
    ERROR_INFO['title'] = '您的请求异常';
    ERROR_INFO['tips'] = '您的请求异常或该页面不存在，请稍后再试'
    return render_template('error/error.html',error=ERROR_INFO,title=html['title']),ERROR_INFO['code'];

@main.app_errorhandler(403)
def forbidden(e):
    ERROR_INFO['code'] = 403;
    ERROR_INFO['title'] = '您无权限访问此页面';
    ERROR_INFO['tips'] = '您的权限无法访问此页面，请检查是否登录或登录用户是否正确！'
    return render_template('error/error.html',error=ERROR_INFO,title=html['title']),ERROR_INFO['code'];

@main.app_errorhandler(404)
def notFound(e):
    ERROR_INFO['code'] = 404;
    ERROR_INFO['title'] = 'UH OH! 页面丢失';
    ERROR_INFO['tips'] = '您所寻找的页面不存在。你可以点击下面的按钮返回主页。'
    return render_template('error/error.html',error=ERROR_INFO,title=html['title']),ERROR_INFO['code'];


@main.app_errorhandler(500)
def ServerError(e):
    ERROR_INFO['code'] = 500;
    ERROR_INFO['title'] = '服务器错误';
    ERROR_INFO['tips'] = '服务器端错误，请稍后再试。'
    return render_template('error/error.html',error=ERROR_INFO,title=html['title']),ERROR_INFO['code'];