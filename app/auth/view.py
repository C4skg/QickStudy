from flask import request
from flask import render_template,url_for,redirect
from datetime import datetime,timedelta

from flask_login import current_user
from flask_login import login_required,logout_user

from ..models import EventID,Permission
from ..models import User

from .. import db
from . import auth


@auth.before_request
def before_request():
    if current_user.is_authenticated:
        pass;


@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'));
    token = request.args.get('token','',type=str);
    data = {
        'type': EventID.LOGIN,
        'token': token
    }
    

    return render_template('auth/login.html',**data)



@auth.route('/register',methods=['GET','POST'])
def register():
    data = {
        'type': EventID.REGISTER
    }

    return render_template('auth/register.html',**data);

@auth.route('/reset',methods=['GET','POST'])
def reset():
    step = request.args.get('step',1,type=int);
    token = request.args.get('token','',type=str);
    data = {
        'type': EventID.RESET,
        'step': step,
        'token': token
    }
    

    return render_template('auth/reset.html',**data)


@auth.route('/userInfo/<id>')
@login_required
def userInfo(id):
    data = {
        'user': current_user,
        "permission": Permission
    }
    user = User.query.filter((User.id == id)).first()
    if user:
        data['user'] = user;
        
    
    return render_template('auth/userinfo.html',**data);


@auth.route('/attend')
@login_required
def attend():
    print(current_user.attend)

    return 'attend'