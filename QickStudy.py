from flask_migrate import Migrate,MigrateCommand,upgrade
from flask_script import Manager

from app.models import User,Permission,UserAttend
from app import create_app
from app import db


app = create_app('TestingEnv');
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Permission=Permission,UserAttend=UserAttend)

if __name__ == '__main__':
    manager.run()