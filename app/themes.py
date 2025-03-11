from flask import Blueprint,Response
from flask import current_app
from flask import abort
from flask.helpers import safe_join,send_file

import os

from .func import Icon

themes = Blueprint('themes',__name__)

@themes.route('/static/<path:path>')
def static(path):
    file = safe_join(current_app.root_path,'static',path)
    if os.path.isfile(file):
        return send_file(file);

    abort(404);

@themes.route('/upload/<path:path>')
def upload(path):
    root_path = os.path.dirname(
        os.path.abspath(__name__)
    )
    uploadPath = current_app.config.get('UPLOADED_PHOTOS_DEST')
    if not uploadPath:
        file = safe_join(current_app.root_path,'upload',path)
    else:
        file = safe_join(root_path,uploadPath,path)

    if os.path.isfile(file):
        print(file)
        return send_file(file)
    
    abort(404)