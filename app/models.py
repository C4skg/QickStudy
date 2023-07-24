from authlib.jose import jwt , JoseError
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import event


from .func import generateImgByName,getRandomStr

from . import db , loginManager

class Permission:
    BASE    = 0;  #!对于违反某些规定的用于给予最低权限，无法发布文章，仅能看文章和关注用户
    USER    = 1;  #^ 可以查看、签到、关注用户、写文章
    ADVENCE = 2;  #* 发布五篇审核过后的文章后，自动升级为进阶用户，可以通过发布文章等方式积攒积分
    CONTROL = 4;  #& 审核文章，解除 BASE 用户的封禁，删除，修改文章状态
    ADMIN   = 8;  #! 系统控制人

    DESC = {
        BASE : {
            "name" : "受限用户",
            "desc" : "你可能违反了某些规定，你目前只能做一些基本的事，耐心等待封禁解除"
        },
        USER : {
            "name" : "普通用户",
            "desc" : "你是本站的普通用户"
        },
        ADVENCE : {
            "name" : "进阶用户",
            "desc" : "你是本站的进阶用户，从现在起你可以升级了"
        },
        CONTROL : {
            "name" : "管理用户",
            "desc" : "你对本站有一定的控制权限，做好本职工作，维护好我们的小站点"
        },
        ADMIN : {
            "name" : "系统",
            "desc" : "你是本站的最高控制者！"
        },
    }

class EventID:
    NONE     = -1;
    REGISTER = 1;
    LOGIN    = 2;
    RESET    = 3;
    ACTIVATE = 4;

class ArticleStatus:
    NOTPASS = 0; #不通过,被退回
    DRAFT   = 1; #草稿状态
    WAIT    = 2; #审核中
    NORMAL  = 3; #正常发布

class UserExperience:
    LEVEL = {
        '1': 0,
        '2': 100,
        '3': 300,
        '4': 1000,
        '5': 3000,
        '6': 10000,
        '7': 30000,
        '8': 100000
    }

    @staticmethod
    def getLevel(exp:int) -> int:
        '''
        返回当前等级
        '''
        for i,v in enumerate(UserExperience.LEVEL.values()):  
            if exp < v:
                return i;
        return i;
      
    @staticmethod
    def getNextValue(LV:int) -> int:
        '''
        返回下个等级需要的经验
        '''
        value = UserExperience.LEVEL.get(str(LV+1)) or 0
        
        return value;
    


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

class UserInfo(db.Model):
    __tablename__ = 'Qc_UserInfo'
    id = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'),primary_key=True);
    experience = db.Column(db.Integer,default=0);
    score = db.Column(db.Integer,default=0); #* 积分

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
    cover = db.Column(db.Text,nullable=True) #文章封面

class User(UserMixin,db.Model):
    __tablename__ = 'Qc_Users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column('username',db.String(50),unique=True,index=True)
    pwd_hash = db.Column('password',db.String(128))
    #! logic del
    delFlag = db.Column('delFlag',db.Boolean,default=False)
    # phone = db.Column('phone',db.String(11),nullable=False,unique=True,index=True)
    email = db.Column('email',db.String(64),unique=True,index=True)
    confirmed = db.Column('confirmed',db.Boolean,default=False,index=True)
    #* LOGO
    logo = db.Column('logo',LONGTEXT)

    sinceTime = db.Column('sinceTime',db.DateTime(),default=datetime.now)
    resetTime = db.Column('resetTime',db.DateTime(),default=datetime.now)
    permission = db.Column('permission',db.Integer,index=True,default=Permission.BASE)
    attend = db.relationship('UserAttend',backref='UserAttend',lazy='select') #! 用户签到

    followTarget = db.relationship('Follow',foreign_keys=[Follow.followTarget],lazy='select') #关注的用户
    followers = db.relationship('Follow',foreign_keys=[Follow.followerId],lazy='select')      #被哪些用户关注

    article = db.relationship('Article',backref='Article',lazy='select')

    userInfo = db.relationship('UserInfo',backref='UserInfo',lazy='select')


    @property
    def pwd(self):
        raise AttributeError('password is not a readable attribute')

    @pwd.setter
    def pwd(self, password):
        self.pwd_hash = generate_password_hash(password)

    def verifyPassword(self,pwd):
        return check_password_hash(self.pwd_hash,pwd)


    '''
    verify is Administrator
    '''
    def isAdministrator(self):
        return self.permission == Permission.ADMIN

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
        eventid = data.get('type') or EventID.NONE;
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
            'retime': datetime.timestamp(datetime.now())
        }
        key = current_app.config['SECRET_KEY']
        return jwt.encode(
            header=header,
            payload=data,
            key=key
        )
    
    def changelogo(self,data:str):
        '''
            data is base64 String
        '''
        self.logo = data
        db.session.merge(self);
        
        return True;

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
        eventid = data.get('type') or EventID.NONE;
        if eventid != EventID.RESET:
            raise InfoError("Your token is invalid")
        
        time = data.get('retime') or 0
        if time and (datetime.now() - datetime.fromtimestamp(time)).seconds > 3600:
            raise InfoError("token 超时");

        user = User.query.get(data.get('id'));
        if not user or user.username != data.get('name'):
            raise InfoError("token 参数异常");

        if user.resetTime != user.sinceTime and (datetime.now() - user.resetTime).days < 1:
            raise InfoError("距上次重置时间小于一天");
        
        user.pwd = newPassword
        user.resetTime = datetime.now()
        db.session.merge(user);

        return True;

    def __repr__(self):
        return '<Qc_User %s>' % self.id
    
    @property
    def getId(self):
        '''
        for login_user() require
        '''
        return self.id;

def beforeInsertEvent(mapper, connection, target):
    '''
        generate the logo by username while creating user;
        create userInfo;
    '''
    target.logo = generateImgByName(target.username.upper())
    userInfo = UserInfo()
    target.userInfo.append(userInfo);

event.listen(User,'before_insert',beforeInsertEvent);


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
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        cache = getRandomStr(6)
        user = User(username='admin',pwd=cache,email='C4skg@qq.com',confirmed=True,permission=Permission.ADMIN)
        db.session.add(user)
        db.session.commit()
        print( 
            'username:','admin',
            'password:',cache
        )