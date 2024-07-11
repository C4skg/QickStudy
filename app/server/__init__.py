from flask import Blueprint


server = Blueprint('server',__name__)

from . import auth, authentication,upload,article,search,center,status