from authlib.jose import jwt , JoseError
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from uuid import uuid4

from . import db , loginManager

class Permission:
    BASE    = 1;  #^ 仅查看权限
    ADVENCE = 2;  #* 可以创建文章
    CONTROL = 4;  #& 审核文章，提升 BASE 用户权限，删除/隐藏文章,即进阶用户
    ADMIN   = 8;  #! 系统控制人

class InfoError(ValueError):
    pass


class UserAttend(db.Model):
    __tablename__ = 'Qc_UserAttend'
    id = db.Column(db.Integer,primary_key = True);
    attendDate = db.Column(db.DateTime(),default = datetime.now);
    userId = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'))

    def signIn(self):
        pass

    def __repr__(self):
        return '<UserAttend %s>' % self.userId


class User(UserMixin,db.Model):
    __tablename__ = 'Qc_Users'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column('username',db.String(50),unique=True,index=True)
    pwd_hash = db.Column('password',db.String(128))
    # phone = db.Column('phone',db.String(11),nullable=True,unique=True,index=True)
    email = db.Column('email',db.String(64),unique=True,index=True)
    sinceTime = db.Column('sinceTime',db.DateTime(),default=datetime.now)
    confirmed = db.Column('confirmed',db.Boolean,default=False);
    permission = db.Column('permission',db.Integer,index=True,default=Permission.BASE)

    attend = db.relationship('UserAttend',backref='UserAttend',lazy='select')


    @property
    def pwd(self):
        raise AttributeError('password is not a readable attribute')

    @pwd.setter
    def pwd(self, password):
        self.pwd_hash = generate_password_hash(password)

    def verifyPassword(self,pwd):
        return check_password_hash(self.pwd_hash,pwd)

    def generateConfirmToken(self,time:int=3600):
        header = {'alg': 'HS256'}
        data = {
            'id': self.id,
            'uname': self.name,
            'timestamp': time
        }
        key = current_app.config['SECRET_KEY']

        return jwt.encode(
            header=header,
            payload=data,
            key=key
        )
    
    def __repr__(self):
        return '<Qc_User %s>' % self.id

    def confirmToken(self,token):
        key = current_app.config['SECRET_KEY']

        try:
            data = jwt.decode(token,key);
        except JoseError:
            raise InfoError("Your token is invalid");
        
        time = data.get('timestamp') or 3600
        
        if (datetime.now() - self.sinceTime).seconds > time:
            db.session.delete(self)
            db.session.commit()
            raise InfoError("token 超时激活，请重新注册");
        
        if data.get('id') != self.id or data.get('uname') != self.name:
            raise InfoError("You token is invalid");

        #! token verify success
        self.confirmed = True
        db.session.add(self);

        return True
    
    @property
    def getId(self):
        return self.id;

class AnonymousUser(AnonymousUserMixin):

    def can(self,permissions):
        return False
    
    def isAdministrator(self):
        return False

loginManager.anonymous_user = AnonymousUser

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def initDB():
    admin = User.query.filter_by(name='admin').first()
    if not admin:
        cache = str(uuid4())[:6]
        user = User(name='admin',pwd=cache,email='C4skg@qq.com',confirmed=True,permission=Permission.ADMIN)
        db.session.add(user)
        db.session.commit()
        print( 
            'username:','admin',
            'password:',cache
         )