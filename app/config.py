from hashlib import md5
from uuid import uuid4
from .func import generateUID32
class Config:
    
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
    SQL_USER = "qickstudy"
    SQL_PASSWORD = "123456"
    SQL_PORT = "3306"
    SQL_SCHEMA = "qickstudy"
    SQL_HOST = "127.0.0.1"
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_SCHEMA}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    #REDIS
    REDIS_URI = "127.0.0.1"
    REDIS_PORT = 6379

    #Elasticsearch
    ELASTICSEARCH_HOST = 'https://xxxxx:9200'
    ELASTICSEARCH_USERNAME = 'xxxxx'
    ELASTICSEARCH_PASSWORD = 'xxxxx'

    #用户全局 ID - session
    SESSION_ID = '_s_id'

    #UPLOAD
    UPLOADED_PHOTOS_DEST = 'upload';
    UPLOADED_FILE_SIZE = 5 * 1024 * 1024; # image size limited  5mb

    #HTML INFO
    TITLE = 'QickStudy'


class TestingEnv(Config):
    SECRET_KEY = "123456"
    DEBUG = True



class ProductionEnv(Config):
    SECRET_KEY = generateUID32()
    DEBUG = False

config = {
    'TestingEnv': TestingEnv,
    'ProductionEnv': ProductionEnv
}
    
