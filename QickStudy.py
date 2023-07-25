from flask_migrate import Migrate,MigrateCommand,upgrade
from flask_script import Manager
from flask import session

from app.func import generateUID6
from app.models import initDB
from app.models import User,Permission,UserAttend,Article,Follow
from app import create_app
from app import db

from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime


app = create_app('TestingEnv');
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

#^ background jobs
scheduler = BackgroundScheduler()

@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Permission=Permission,
        UserAttend=UserAttend,
        Article=Article,
        Follow=Follow
    )
    
@app.before_request
def before_request():
    id = app.config['SESSION_ID'];
    if session.get(id):
        pass;
    else:
        session[id] = generateUID6();

def CleanUser():
    with app.app_context():
        data = User.query.filter_by(confirmed=False).all()
        for e in data:
            if (datetime.now() - e.sinceTime).seconds >= (3600):
                db.session.delete(e);
                db.session.commit();

scheduler.add_job(
    func=CleanUser,
    trigger='interval',
    seconds=60*30
)
scheduler.start()

@manager.command
def deploy():

    upgrade();

    # inert admin user
    initDB();


if __name__ == '__main__':
    manager.run()