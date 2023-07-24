from flask import request,current_app
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


class UploadFileTooLarge(ValueError):
    '''
    throw the error if the file too larger;
    '''
    pass;

UPLOAD_MAX_SIZE = 5 * 1024 * 1024;

@server.before_request
def before_request():
    if current_user.permission < Permission.USER:
        return uploadResponse['6003'];

    C_SIZE = current_app.config.get('UPLOADED_FILE_SIZE');
    if C_SIZE:
        UPLOAD_MAX_SIZE = C_SIZE;
    

@server.errorhandler(RequestEntityTooLarge)
def tooLarge(error):
    return uploadResponse['6002'];


@server.route('/uupload',methods=['POST'])
@login_required
def photoUpload():

    if 'file' in request.files:
        try:
            data = request.files.get('file').read()
            if len(data) > UPLOAD_MAX_SIZE:
                raise UploadFileTooLarge('The upload file is too large')

            base64 = b64encode(data).decode();
            current_user.changelogo(base64);
            db.session.commit();

            return uploadResponse['6000']
        except:
            return uploadResponse['6002']
    else:
        pass;

    return uploadResponse['6001']


@server.route('/upload',methods=['POST'])
@login_required
def upload():

    if 'file' in request.files:
        childFolder = getDate();
        _clone = deepcopy(uploadResponse['6000'])

        for file in request.files.getlist('file'):
            try:
                size = len(file.read());
                if size > UPLOAD_MAX_SIZE:
                    raise(UploadFileTooLarge('The file is too large'));

                file.seek(0);
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
            except:
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



@server.route('/insertArticle')
@login_required
def createArticle():
    pass;