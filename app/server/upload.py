from flask_login import login_required
from flask_login import current_user
from flask_up

from ..models import Permission
from . import server

@server.route('/upload',methods=['GET','POST'])
# @login_required
def upload():
    # if current_user.permission < Permission.USER:
    #     return Permission.USER;
    
    pass;
