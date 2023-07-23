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
    MAIL_DEBUG = False

    #Compress
    COMPRESS_ALGORITHM = 'gzip'
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'text/plain', 'application/json', 'application/javascript','image/png','image/jpeg','text/svg']
    COMPRESS_LEVEL = 9

    #SQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/QickStudy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    #REDIS
    REDIS_URI = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_PASS = "QickStudy"

    #用户全局 ID - session
    SESSION_ID = '_s_id'

    #UPLOAD
    UPLOADED_PHOTOS_DEST = 'upload';
    # MAX_CONTENT_LENGTH = 5 * 1024 * 1024; # image size limited

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
    