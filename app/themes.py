from flask import Blueprint,Response
from flask import current_app
from flask import abort
from flask.helpers import safe_join,send_file

import os
import gzip
themes = Blueprint('themes',__name__)

@themes.route('/static/<path:path>')
def static(path):
    file = safe_join(current_app.root_path,'static',path)
    if os.path.isfile(file):
        return send_file(file)
    abort(404);