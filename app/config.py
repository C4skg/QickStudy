from hashlib import md5
from uuid import uuid4

class Config:
    SECRET_KEY = md5(str(uuid4()).encode()).hexdigest()
    
    MAIL_SERVER='smtp.qq.com'
    MAIL_PORT='465'
    MAIL_USERNAME='C4skg@qq.com'
    MAIL_PASSWORD='fhxgqmfgnryliabf'  #!可在邮箱设置中获取
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False

    #SQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/QickStudy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    #REDIS
    REDIS_URI = "8ceefcf67710.c.methodot.com"
    REDIS_PORT = 30955

    #HTML INFO
    TITLE = 'QickStudy'


class TestingEnv(Config):
    DEBUG = True



class ProductionEnv(Config):
    DEBUG = False

config = {
    'TestingEnv': TestingEnv,
    'ProductionEnv': ProductionEnv
}
    