from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager
from flask_compress import Compress
from flask_uploads import UploadSet,IMAGES
from flask_uploads import configure_uploads

import redis
from .config import Config,config

csrf = CSRFProtect()
mail = Mail()
db = SQLAlchemy()
loginManager = LoginManager()
loginManager.login_view = 'auth.login'
photos = UploadSet('photos',IMAGES)

#^ set redis')
redisClient = redis.Redis(host=Config.REDIS_URI,port=Config.REDIS_PORT,password=Config.REDIS_PASSWORD)



def create_app( envname:str = 'ProductionEnv' ):
    '''
    Default mode is productionenv
    The debug is false
    '''
    app = Flask(__name__)

    #^ set config
    app.config.from_object(
        config.get(envname) or config.get('ProductionEnv')
    )

    #^ set uploads
    configure_uploads(app,photos);

    
    #^ set compress
    Compress(app)

    #^ init app
    csrf.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    loginManager.init_app(app)

    #^ register bluemap
    from .server import server as server_BluePrint
    from .main import main as main_BluePrint
    from .auth import auth as auth_BluePrint
    from .themes import themes as themes_BluePrint
    from .admin import admin as admin_BluePrint

    app.register_blueprint(server_BluePrint,url_prefix='/server')
    app.register_blueprint(auth_BluePrint,url_prefix='/user')
    app.register_blueprint(themes_BluePrint,url_prefix='/themes')
    app.register_blueprint(admin_BluePrint,url_prefix='/admin')
    app.register_blueprint(main_BluePrint)

    return app;

