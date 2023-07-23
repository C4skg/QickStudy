from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import current_user
from flask_uploads import UploadNotAllowed
from werkzeug.exceptions import RequestEntityTooLarge

from copy import deepcopy
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
        childFolder = getDate();
        _clone = deepcopy(uploadResponse['6000'])

        for file in request.files.getlist('file'):
            try:
                path = photos.save(
                    file,
                    folder=childFolder
                )
                _clone['files'].append(
                    {
                        'filename': file.filename,
                        'status': 'success',
                        'path':  request.url_root + url_for('themes.upload',path=path)
                    }
                )
            except UploadNotAllowed:
                _clone['files'].append(
                    {
                        'filename': file.filename,
                        'status': 'failed',
                        'path': ''
                    }
                )
        return _clone;

    else:
        pass
    
    return uploadResponse['6001']