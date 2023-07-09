from flask import request,session
from flask import render_template,url_for,redirect
from random import choices
from datetime import datetime
from string import ascii_letters,digits

from flask_login import current_user
from flask_login import login_required,login_user,logout_user

from ..models import User,UserAttend,InfoError,Permission,EventID
from ..email import send_email
from .verify import isVaildRegister,registerUserExisit,isVaildEmail,isVaildPwd
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
    data = {
        'type': EventID.LOGIN
    }
    type = request.form.get('type',EventID.NONE,type=int);
    if type and type == EventID.LOGIN:
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

    return render_template('auth/login.html',**data)



@auth.route('/register',methods=['GET','POST'])
def register():
    data = {
        'type': EventID.REGISTER
    }
    type = request.form.get('type',EventID.NONE,type=int);
    if type and type == EventID.REGISTER:
        email = request.form.get('email',False,type=str);
        pwd = request.form.get('pwd',False,type=str);
        if email and pwd:
            flag = isVaildRegister(email,pwd);
            if flag:
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
                mailInfo = {
                    'title': '用户注册',
                    'context': '感谢您注册此平台',
                    'tips': '完成注册，请点击下面按钮跳转登录验证邮箱即可。',
                    'button': '点击此处进行验证',
                    'user': user,
                    'host': request.url_root,
                    'link': url_for('auth.login',token=token)
                }
                send_email(user.email,'请确认你的账户','auth/mail/confirm.html',**mailInfo)

                return {
                    'status': 1,
                    'info': '注册成功，请注意查收邮件'
                }
            else:
                return {
                    'status': -1,
                    'info': '格式不正确'
                }

    return render_template('auth/register.html',**data);

@auth.route('/reset',methods=['GET','POST'])
def reset():
    step = request.args.get('step',1,type=int);
    data = {
        'type': EventID.RESET,
        'step': step
    }
    type = request.form.get('type',EventID.NONE,type=int);
    if type and type == EventID.RESET:
        if step == 1:
            info = {
                'status': -1,
                'step': 1,
                'info': '无此用户'
            }
            email = request.form.get('email','',type=str);
            if email and isVaildEmail:
                user = User.query.filter_by(email=email).first()
                if user:
                    if user.resetTime == user.sinceTime or (datetime.now() - user.resetTime).days >= 1:
                        token = user.generateResetToken()
                        #! 发送邮件
                        mailInfo = {
                            'title': '重置密码',
                            'context': '请确实是本人操作，并根据下面提示进行重置密码',
                            'tips': '点击下方按钮进行密码重置',
                            'button': '点击此处重置密码',
                            'user': user,
                            'host': request.url_root,
                            'link': url_for('auth.reset',token=token,step=2),
                            'token': token
                        }
                        send_email(user.email,'重置密码','auth/mail/confirm.html',**mailInfo)
                        info['status'] = 1
                        info['info'] = '已发送重置密码邮件,清注意查收'
                    else:
                        info['info'] = '距上次重置时间小于一天'

            return info;
        else:
            info = {
                'status': -1,
                'step': 2,
                'info': '密码格式错误'
            }
            pwd = request.form.get('pwd','',type=str);
            token = request.args.get('token','',type=str);
            if pwd and isVaildPwd(pwd):
                try:
                    flag = User.resetPassword(token,pwd);
                    db.session.commit();
                    info['status'] = 1
                    info['info'] = '密码重置成功'
                except InfoError as e:
                    info['info'] = str(e);
            
            return info;

    return render_template('auth/reset.html',**data)

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