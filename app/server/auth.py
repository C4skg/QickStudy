from flask import Response
from flask import request,session,current_app
from flask import render_template,url_for,abort
from flask_login import current_user
from flask_login import login_user,login_required,logout_user
from datetime import datetime,timedelta
from base64 import b64decode

from .authentication import resetVCode
from .verify import isVaildRegister,registerUserExisit,isVaildEmail,isVaildPwd
from ..models import User,EventID,Permission,InfoError
from ..func import getRandomStr
from ..email import send_email
from .. import db,redisClient
from ..responseData import (
    loginResponse,
    logoutResponse,
    registerResponse,
    resetResponse,
    activateResponse
)

from . import server

@server.route('/confirm/<token>')
@login_required
def confirm(token):
    type = request.args.get('type',EventID.NONE,type=int);
    data = activateResponse['4003'];
    if type == EventID.ACTIVATE:
        if current_user.confirmed:
            data = activateResponse['4002'];
        try:
            flag = current_user.confirmToken(token)
            db.session.commit();
            data = activateResponse['4000'];
        except InfoError as e:
            data = activateResponse['4001'];
    
    return render_template('info.html',**data)

@server.route('/login',methods=['POST'])
def login():
    if current_user.is_authenticated:
        return loginResponse['1003'];
    
    type = request.form.get('type',EventID.NONE,type=int);
    if type and type == EventID.LOGIN:
        # verify code
        code = request.form.get('code','',type=str);

        id = session[current_app.config.get('SESSION_ID')];
        vCode = redisClient.hget(id,'code')
        if not vCode or vCode.decode().lower() != code.lower():
            resetVCode(id);
            return loginResponse['1002']
        
        # if verify code ok:
        resetVCode(id);

        username = request.form.get('username','',type=str);
        pwd  = request.form.get('pwd','',type=str);
        if username and pwd:
            user = User.query.filter((User.username == username) | (User.email == username)).first()
            if user and user.verifyPassword(pwd):
                if user.permission >= Permission.CONTROL:
                    login_user(user)
                else:
                    login_user(user,remember=True)
                e = loginResponse['1000'];
                if user.confirmed == False:
                    try:
                        token = request.form.get('token') or '';
                        print('token >>>',token)
                        flag = current_user.confirmToken(token)
                        print("flag >>> ",flag)
                        db.session.commit();

                    except InfoError as e:
                        logout_user();
                        return activateResponse['4001'];
            
                else:
                    e['route'] = request.args.get('next',url_for('main.index'),type=str);
                '''
                    登录成功后删除 redis 的验证码
                '''
                redisClient.delete(id);
                return e;
            else:
                return loginResponse['1001'];
    
    return loginResponse['1004'];


@server.route('/register',methods=['POST'])
def register():
    type = request.form.get('type',EventID.NONE,type=int);
    if type and type == EventID.REGISTER:
        code = request.form.get('code','',type=str);

        id = session[current_app.config.get('SESSION_ID')];
        vCode = redisClient.hget(id,'code')
        if not vCode or vCode.decode().lower() != code.lower():
            resetVCode(id);
            return registerResponse['2003']
        
        # if verify code ok:
        resetVCode(id);
        
        email = request.form.get('email',False,type=str);
        pwd = request.form.get('pwd',False,type=str);
        if email and pwd:
            flag = isVaildRegister(email,pwd);
            if flag:
                if registerUserExisit(email):
                    return registerResponse['2001'];
                    
                user = User(
                    username='用户_'+ getRandomStr(4),
                    pwd = pwd,
                    email = email.lower(),
                    permission = Permission.USER
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
                '''
                发送邮件后删除验证码
                '''
                redisClient.delete(id);
                return registerResponse['2000'];
    
    return registerResponse['2004'];
                
            
@server.route('/reset',methods=['POST'])
def reset():
    type = request.form.get('type',EventID.NONE,type=int);
    step = request.form.get('step',1,type=int);
    if type and type == EventID.RESET:
        if step == 1:
        #* 步骤判断
            code = request.form.get('code','',type=str);

            id = session[current_app.config.get('SESSION_ID')];
            vCode = redisClient.hget(id,'code')
            if not vCode or vCode.decode().lower() != code.lower():
                resetVCode(id);
                return resetResponse['3007']
            
            # if verify code ok:
            resetVCode(id);

            email = request.form.get('email','',type=str);
            if email and isVaildEmail(email):
                user = User.query.filter_by(email=email).first()
                if user:
                    if (
                        redisClient.exists(email) and
                        int(redisClient.hget(email,'type').decode()) == EventID.RESET and 
                        (datetime.now() - datetime.fromtimestamp(float(redisClient.hget(email,'time').decode()))) < timedelta(minutes=2)
                    ):
                        return resetResponse['3001'];
                    else:
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
                            redisClient.hset(email,'time',datetime.now().timestamp())
                            redisClient.hset(email,'type',EventID.RESET)
                            redisClient.expire(email,20)
                            send_email(user.email,'重置密码','auth/mail/confirm.html',**mailInfo)
                            '''
                            发送邮件后删除验证码
                            '''
                            redisClient.delete(id);
                            return resetResponse['3000'];
                        else:
                            return resetResponse['3006'];
            #* 若无法匹配邮箱
            return resetResponse['3004'];
        #* 步骤判断
        elif step == 2:
            pwd = request.form.get('pwd','',type=str);
            token = request.form.get('token','',type=str);
            if pwd and isVaildPwd(pwd):
                try:
                    flag = User.resetPassword(token,pwd);
                    db.session.commit();
                    return resetResponse['3002']
                except InfoError as e:
                    return resetResponse['3003']
            else:
                return resetResponse['3005'];

    return resetResponse['3008'];


@server.route('/logo/<id>')
def logo(id:int):
    user = User.query.filter_by(id=id).first();
    if user:
        data = b64decode(user.logo);
        return Response(
                    data,
                    mimetype='image/png'
                )
    abort(404);
    
        


@server.route('/logout')
@login_required
def logout():
    try:
        logout_user();
        data = logoutResponse['5000']
    except:
        data = logoutResponse['5001']
    return render_template(
        'info.html',
        **data
    )
