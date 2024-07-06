import colorama
import tqdm
from authlib.jose import jwt , JoseError
from flask import current_app
from flask import url_for
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import event

from .func import generateImgByName,getRandomStr
from .config import Config
from . import db , loginManager,EsClient

colorama.init(autoreset=True)


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
    FOLLOW = 5;
    SCORE = 6;
    EXPERIENCE = 7;

class ArticleStatus:
    NOTPASS = 0; #不通过,被退回
    DRAFT   = 1; #草稿状态
    WAIT    = 2; #审核 , 及发布前
    NORMAL  = 3; #已正常发布
    PRIVATE = 4; #仅自己可见

    Desc = {
        NOTPASS:{
            "color": "red",
            "name" : "未通过",
            "desc" : "文章未通过审核,可能存在不恰当内容,请检查后重新申请审核"
        },
        DRAFT:{
            "color": "mute",
            "name" : "草稿",
            "desc" : "文章为草稿状态,仅自己可见"
        },
        WAIT:{
            "color": "yellow",
            "name" : "审核中",
            "desc" : "文章审核中,耐心等待"
        },
        NORMAL:{
            "color": "green",
            "name" : "已发布",
            "desc" : "文章已正常发布"
        },
        PRIVATE:{
            "color": "primary",
            "name": "私有",
            "desc" : "该文章内容仅你自己可见"
        }
    }

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
    

#Error define
class InfoError(ValueError):
    '''
    @param: ValueError:str  use your value to raise the error
    '''
    pass

class UploadFileTooLarge(ValueError):
    '''
    throw the error if the file too larger;
    '''
    pass;


class UserAttend(db.Model):
    __tablename__ = 'Qc_UserAttend'
    id = db.Column(db.Integer,primary_key = True);
    attendDate = db.Column(db.DateTime(),default = datetime.now);
    userId = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'))

    def signIn(self):
        pass

    def __repr__(self):
        return '<UserAttend %s>' % self.userId
    
class Logs(db.Model):
    __tablename__ = 'Qc_logs'
    id = db.Column(db.Integer,primary_key=True)
    eventId = db.Column(db.Integer,nullable=False,index=True);
    desc = db.Column(db.String(1000),nullable=False);
    nums = db.Column(db.Integer,nullable=False,default=0,index=True);
    timestamp = db.Column(db.DateTime(),default=datetime.now)

    def __repr__(self):
        return '<Qc_logs %s>' % self.id;

class UserInfo(db.Model):
    __tablename__ = 'Qc_UserInfo'
    id = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'),primary_key=True);
    experience = db.Column(db.Integer,default=0);
    score = db.Column(db.Integer,default=0); #* 积分
    
    def addScore(self,value:int,desc:str) -> bool:
        if value <= 0:
            return False;
            
        self.score += value;

        log = Logs(
            eventId = EventID.SCORE,
            desc = desc,
            nums = value
        )
        db.session.add(log);
        db.session.add(self);
        return True;
    
    def addExperience(self,value:int,desc:str) -> bool:
        if value <= 0:
            return False;

        self.addExperience += value;

        log = Logs(
            eventId = EventID.EXPERIENCE,
            desc = desc,
            nums = value
        )
        db.session.add(log);
        db.session.add(self);
        return True;

    def reduceScore(self,value:int,desc:str) -> bool:
        if value <= 0 or value > self.score:
            return False;

        self.score -= value;

        log = Logs(
            eventId = EventID.SCORE,
            desc = desc,
            nums = value
        )
        db.session.add(log);
        db.session.add(self)
        return True;

    def reduceExperience(self,value:int,desc:str) -> bool:
        if value <= 0 or value > self.experience:
            return False;

        self.experience -= value;

        log = Logs(
            eventId = EventID.EXPERIENCE,
            desc = desc,
            nums = value
        )
        db.session.add(log);
        db.session.add(self)
        return True;
    
    def __repr__(self):
        return '<Qc_UserInfo %s>' % self.id;
    

    

class Follow(db.Model):
    __tablename__ = 'follows'
    followerId = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'),primary_key=True);  #关注用户
    followTarget = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'),primary_key=True); #被关注用户
    time = db.Column(db.DateTime(),default=datetime.now)


'''
for Article table
'''
class Art_agree(db.Model):
    __tablename__ = 'Qc_art_Agree'
    id = db.Column(db.Integer,primary_key=True);
    articleId = db.Column(db.Integer,db.ForeignKey('Qc_articles.id'))
    userId = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'))
    time = db.Column(db.DateTime(),default=datetime.now)


class Art_types(db.Model):
    __tablename__ = 'Qc_art_Types'
    id = db.Column(db.Integer,primary_key=True)
    typeName = db.Column(db.String(50))


class Art_comment(db.Model):
    __tablename__ = 'Qc_comment'
    id = db.Column(db.Integer,primary_key=True)
    articleId = db.Column(db.Integer,db.ForeignKey('Qc_articles.id'))
    userId = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'))
    context = db.Column(db.String(1000));
    parentId = db.Column(db.Integer,default=0,index=True);
    replyId = db.Column(db.Integer,default=0,index=True);
    time = db.Column(db.DateTime(),default=datetime.now)

    def __repr__(self):
        return '<Art_comment_%s>' % self.id;


class Article(db.Model):
    __tablename__ = 'Qc_articles'

    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci'
    }
    

    id = db.Column(db.Integer,primary_key = True);
    userId = db.Column(db.Integer,db.ForeignKey('Qc_Users.id'));
    title = db.Column(db.String(100),nullable=False);
    context = db.Column(LONGTEXT,nullable=False);
    lastTime = db.Column(db.DateTime(),nullable=False,default=datetime.now);
    status = db.Column(db.Integer,nullable=False,default=ArticleStatus.DRAFT,index=True)
    cover = db.Column(db.Text,nullable=True) #文章封面  路径
    agree = db.relationship('Art_agree',backref='Article',lazy='dynamic',order_by='Art_agree.time');

    # 文章类型
    typeId = db.Column(db.Integer)

    comments = db.relationship('Art_comment',backref='Article',lazy='dynamic')
    

    __mapper_args__ = {
        "order_by": id.desc()
    }

    def updateCover(self,path:str) -> bool:
        self.cover = path;
        self.lastTime = datetime.now();
        db.session.add(self);

        return True;

    def updateTitle(self,title:str) -> bool:
        length = len(title)
        if length == 0 or length > 100:
            return False;

        self.title = title;
        self.lastTime = datetime.now();
        db.session.add(self);
    
        return True;

    def updateContext(self,context:str) -> bool:
        length = len(context)
        if length == 0:
            return False;
    
        self.context = context;
        self.lastTime = datetime.now();
        db.session.add(self);
    
        return True;

    def updateStatus(self,status:int) -> bool:
        current_status = self.status;
        if current_status == status:
            return False;
    
        self.status = status;
        
        db.session.add(self);
    
        return True;

    def updateAgree(self) -> bool:
        self.agree += 1;
        db.session.add(self);
    
        return True;

    def updateType(self,n:int) -> bool:
        if Art_types.query.filter_by(id=n).first() or int(n)==0:
            self.typeId = n;
            db.session.add(self);
            return True;
        else:
            return False;

    def __repr__(self):
        return '<Article_%s>' % self.id;

class Images(db.Model):
    __tablename__ = 'Qc_images'

    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci'
    }

    id = db.Column(db.Integer,primary_key = True)
    finger = db.Column(db.Text)
    path = db.Column(db.Text)

    def getImagePath(self):
        return self.path;


class User(UserMixin,db.Model):
    __tablename__ = 'Qc_Users'

    __table_args__ = {
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci'
    }


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

    article = db.relationship('Article',backref='User',lazy='dynamic',order_by='Article.id')
    comments = db.relationship('Art_comment',backref='User',lazy='dynamic')

    userInfo = db.relationship('UserInfo',backref='User',lazy='select')


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


    def changeUserName(self,data:str):
        '''
            data is plain text
        '''
        if len(data) > 25:
            return False
        
        self.username = data
        db.session.merge(self)

        return True


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

'''
    sql event listener
'''

def user_beforeInsertEvent(mapper, connection, target):
    '''
        generate the logo by username while creating user;
        create userInfo;
    '''
    target.logo = generateImgByName(target.username.upper())
    userInfo = UserInfo()
    target.userInfo.append(userInfo);

    '''
        do not need `db.session.commit()`;
    '''

event.listen(User,'before_insert',user_beforeInsertEvent);


'''
    ElasticSearch Upload
'''
def ArticleDocumentUpload(id:int,title:str,context:str,author:int,type:int=0,methods:str='add') -> bool:
    if methods not in ['add','update']:
        return False;
    
    try:
        EsClient.index(
            index = Config.ELASTICSEARCH_INDEX,
            id=id,
            document={
                'title': title,
                'context': context,
                'author': str(author),
                'type': str(type)
            }
        )
    except:
        return False;
    
    return True;


def article_afterInsert(mapper,connection,target):
    uploadStatus = ArticleDocumentUpload(
        id=target.id,
        title=target.title,
        context=target.context,
        type=target.typeId,
        author=target.userId
    )
    print(
        colorama.Fore.GREEN + 'insert article success'
    )

event.listen(Article,'after_insert',article_afterInsert);



def article_afterUpdate(mapper,connection,target):
    updateStatus = ArticleDocumentUpload(
        id=target.id,
        title=target.title,
        context=target.context,
        type=target.typeId,
        author=target.userId,
        methods='update'
    );
    print(
        colorama.Fore.GREEN + 'update article success'
    )

event.listen(Article,'after_update',article_afterUpdate);




class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    
    def isAdministrator(self):
        return False

loginManager.anonymous_user = AnonymousUser

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def insertDocument():
    '''
        @insert article by query article db
    '''
    articles = Article.query.filter_by(status=ArticleStatus.NORMAL).all()
    for article in tqdm.tqdm(articles):
        result = ArticleDocumentUpload(
            id=article.id,
            title=article.title,
            context=article.context,
            author=article.userId,
            type=article.typeId
        )
        if not result:
            print(colorama.Fore.RED + 'article: ' + article.id,'error!');
            exit(0);

    print(
        colorama.Fore.GREEN + 'insert success!'
    );

def initDB():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        cache = getRandomStr(6)
        user = User(username='admin',pwd=cache,email='C4skg@qq.com',confirmed=True,permission=Permission.ADMIN)
        db.session.add(user)
        db.session.commit()
        print(
            colorama.Fore.GREEN + 'username:','admin',
            colorama.Fore.GREEN + 'password:',cache
        )
        
    else:
        print(
            colorama.Fore.RED + 
            '''
                Your db has already init
            '''
        )