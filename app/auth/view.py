from flask import request,session
from flask import render_template,url_for,redirect
from random import choices
from string import ascii_letters,digits

from flask_login import current_user
from flask_login import login_required,login_user,logout_user

from ..models import User,UserAttend,InfoError,Permission
from ..email import send_email
from .verify import isVaildRegister,registerUserExisit
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

    username = request.form.get('username',False,type=str);
    pwd  = request.form.get('pwd',False,type=str);

    if username and pwd:
        e = {
            'status': '-1',
            'router': '.'
        }
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        if user and user.verifyPassword(pwd):
            if user.permission >= Permission.CONTROL:
                login_user(user)
            else:
                login_user(user,remember=True)

            e['status'] = '1';
            if user.confirmed == False:
                token = request.args.get('token','')
                e['router'] = url_for('auth.confirm',token=token);
            else:
                e['router'] = request.args.get('next',url_for('main.index'),type=str);

        return e;

    return render_template('auth/login.html')



@auth.route('/register',methods=['GET','POST'])
def register():
    email = request.form.get('email',False,type=str);
    pwd = request.form.get('pwd',False,type=str);
    if email and pwd:
        flag = isVaildRegister(email,pwd);
        if flag == 'ok':
            if registerUserExisit(email):
                return {
                    'status': -1,
                    'info': '该邮箱已注册'
                }
            user = User(
                username='用户_'+''.join(choices(list(ascii_letters+digits),k=6)),
                pwd = pwd,
                email = email.lower()
            )
            db.session.add(user);
            db.session.commit();
            #! 一定要插入数据库后，不然无法获取自增的 id
            token = user.generateConfirmToken()
            #! 发送邮件
            send_email(user.email,'请确认你的账户','auth/mail/confirm.html',user=user,host=request.url_root,token=token)

            return {
                'status': 1,
                'info': '注册成功，请注意查收邮件'
            }
        else:
            return {
                'status': -1,
                'info': flag
            }
            

    return render_template('auth/register.html');

@auth.route('/reset',methods=['GET','POST'])
def reset():
    username = request.form.get('username',False,type=str);
    # if email:

@auth.route('/logout')
@login_required
def logout():
    logout_user();
    data = {
        'title': '你已退出登录',
        'context': '',
        'type': 'info',
        'location': url_for('auth.login')
    }
    return render_template(
        'info.html',
        **data
    )


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(
            url_for('main.index')
        )
    data = {
        'title': '',
        'context': '',
        'type': 'success',
        'location': ''
    }
    try:
        flag = current_user.confirmToken(token)
        db.session.commit();
        data['title'] = "恭喜！你已经成功激活你的账户！"
        data['location'] = url_for('main.index')
        
    except InfoError as e:
        data['title'] = '激活失败'
        data['context'] = str(e)
        data['type'] = 'error'

    return render_template('info.html',**data)




@auth.route('/userInfo')
@login_required
def userInfo():
    id = request.args.get('id',False);
    if id:
        return id;
    else:
        return current_user.username;


@auth.route('/attend')
@login_required
def attend():
    print(current_user.attend)

    return 'attend'