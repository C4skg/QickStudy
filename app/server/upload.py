from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import current_user
from flask_uploads import UploadNotAllowed
from werkzeug.exceptions import RequestEntityTooLarge

from base64 import b64encode

from ..func import getDate
from ..models import Permission
from ..responseData import uploadResponse
from .. import photos,db
from . import server        

@server.errorhandler(RequestEntityTooLarge)
def tooLarge(error):
    return uploadResponse['6002'];

@server.route('/uupload',methods=['POST'])
@login_required
def photoUpload():
    if current_user.permission < Permission.BASE:
        return uploadResponse['6003'];

    if 'file' in request.files:
        try:
            data = request.files.get('file').read()
            base64 = b64encode(data).decode();
            current_user.changelogo(base64);
            db.session.commit();

            return uploadResponse['6000']
        except:
            pass;
    else:
        pass;

    return uploadResponse['6001']

@server.route('/upload',methods=['POST'])
@login_required
def upload():
    if current_user.permission < Permission.BASE:
        return uploadResponse['6003'];

    if 'file' in request.files:
        try:
            childFolder = getDate();
            path = photos.save(
                request.files['file'],
                folder=childFolder
            )
            _clone = uploadResponse['6000']
            _clone['backURI'] = url_for('themes.upload',path=path)
            return _clone;
        except UploadNotAllowed:
            pass;
    else:
        pass;
    
    return uploadResponse['6001']