from authlib.jose import jwt , JoseError
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.mysql import LONGTEXT
from . import db , loginManager

class Permission:
    LOWER   = 0;  #!对于违反某些规定的用于给予最低权限，无法发布文章，仅能看文章和关注用户
    BASE    = 1;  #^ 可以查看、签到、关注用户、写文章
    ADVENCE = 2;  #* 发布五篇审核过后的文章后，自动升级为进阶用户，可以通过发布文章等方式积攒积分
    CONTROL = 4;  #& 审核文章，提升 BASE 用户权限，删除，修改文章状态,即进阶用户
    ADMIN   = 8;  #! 系统控制人

class EventID:
    REGISTER = 1;
    LOGIN = 2;
    RESET = 3;

class ArticleStatus:
    NOTPASS = 0; #不通过
    DRAFT = 1;
    WAIT = 2;
    NORMAL = 3;

    


class InfoError(ValueError):
    '''
    @param: ValueError:str  use your value to raise the error
    '''
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

class Follow(db.Model):
    __tablename__ = 'follows'
    followerId = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'),primary_key=True);  #follow 用户
    followTarget = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'),primary_key=True); #被 follow 用户
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key = True);
    userId = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'));
    title = db.Column(db.String(100),nullable=False);
    context = db.Column(LONGTEXT,nullable=False);
    timestamp = db.Column(db.DateTime,nullable=False,default=datetime.utcnow);
    status = db.Column(db.Integer,nullable=False,default=ArticleStatus.DRAFT,index=True)


class User(UserMixin,db.Model):
    __tablename__ = 'Qc_Users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column('username',db.String(50),unique=True,index=True)
    pwd_hash = db.Column('password',db.String(128))
    # phone = db.Column('phone',db.String(11),nullable=False,unique=True,index=True)
    email = db.Column('email',db.String(64),unique=True,index=True)
    sinceTime = db.Column('sinceTime',db.DateTime(),default=datetime.now)
    confirmed = db.Column('confirmed',db.Boolean,default=False);
    permission = db.Column('permission',db.Integer,index=True,default=Permission.BASE)
    attend = db.relationship('UserAttend',backref='UserAttend',lazy='select') #! 用户签到

    followTarget = db.relationship('Follow',foreign_keys=[Follow.followTarget],lazy='select') #关注的用户
    followers = db.relationship('Follow',foreign_keys=[Follow.followerId],lazy='select')      #被哪些用户关注

    article = db.relationship('Article',backref='Article',lazy='select')


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
            'name': self.username,
            'type': EventID.REGISTER,
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
        # if the token is right
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY']
            );
        except JoseError:
            raise InfoError("Your token is invalid");
        
        # if the token is valid
        eventid = data.get('type') or -1;
        if eventid != EventID.REGISTER:
            raise InfoError("Your token is invalid")
        
        time = data.get('timestamp') or 3600
        
        if (datetime.now() - self.sinceTime).seconds > time:
            db.session.delete(self)
            db.session.commit()
            raise InfoError("token 超时激活，请重新注册");
        
        if data.get('id') != self.id or data.get('name') != self.username:
            raise InfoError("You token is invalid");

        #! token verify success
        self.confirmed = True
        db.session.add(self);

        return True
    
    def generateResetToken(self):
        header = {'alg': 'HS256'}
        data = {
            'id': self.id,
            'name': self.username,
            'type': EventID.RESET,
            'retime': datetime.now()
        }
        key = current_app.config['SECRET_KEY']
        return jwt.encode(
            header=header,
            payload=data,
            key=key
        )

    @staticmethod
    def resetPassword(token,newPassword):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY']
            )
        except JoseError:
            raise InfoError("Your token is invalid");
        
        # if the token is valid
        eventid = data.get('type') or -1;
        if eventid != EventID.RESET:
            raise InfoError("Your token is invalid")
        
        time = data.get('retime')
        if time and (datetime.now() - time).seconds > 3600:
            raise InfoError("token 超时激活，请重新注册");

        user = User.query.get(data.get('id'))
        if user.username != data.get('name'):
            return False;
    
        user.password = newPassword
        db.session.add(user);

        return True;

    
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