from flask import Blueprint,abort
from flask.helpers import safe_join,send_file
from flask import current_app
import os

themes = Blueprint('themes',__name__)

@themes.route('/static/<path:path>')
def static(path):
    file = safe_join(current_app.root_path,'static',path)
    print(file)
    if os.path.isfile(file):
        return send_file(file);
        
    abort(404);