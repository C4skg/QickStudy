from flask import request,current_app
from flask import url_for
from flask_login import login_required
from flask_login import current_user
from flask_uploads import UploadNotAllowed
from werkzeug.exceptions import RequestEntityTooLarge

from copy import deepcopy
from base64 import b64encode

from ..func import getDate,getFinger,getFiletype
from ..models import Permission
from ..models import InfoError,UploadFileTooLarge,Images
from ..responseData import uploadResponse
from .. import photos,db
from . import server




UPLOAD_MAX_SIZE = 5 * 1024 * 1024;

@server.before_request
def before_request():
    global UPLOAD_MAX_SIZE;
    
    C_SIZE = current_app.config.get('UPLOADED_FILE_SIZE');
    if C_SIZE:
        UPLOAD_MAX_SIZE = C_SIZE;
    

@server.errorhandler(RequestEntityTooLarge)
def tooLarge(error):
    return uploadResponse['6002'];


@server.route('/user/upload',methods=['POST'])
@login_required
def photoUpload():
    if current_user.permission < Permission.USER:
        return uploadResponse['6003'];

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

#* editor
@server.route('/editor/upload',methods=['POST'])
@login_required
def upload():
    if current_user.permission < Permission.USER:
        return uploadResponse['6003'];

    if 'file' in request.files:
        childFolder = getDate();
        _clone = deepcopy(uploadResponse['6000'])
        for file in request.files.getlist('file'):
            try:
                data = file.read()
                size = len(data);
                if size > UPLOAD_MAX_SIZE:
                    raise(UploadFileTooLarge('The file is too large'));
                finger = getFinger(data)
                images = Images.query.filter_by(finger = finger).first()
                if images:
                    _clone['files'].append(
                        {
                            'filename': file.filename,
                            'status': 'success',
                            'path': images.getImagePath()
                        }
                    )
                    continue
                else:
                    file.seek(0);
                    sufix = getFiletype(file.filename)
                    path = photos.save(
                        file,
                        folder=childFolder,
                        name=finger + sufix
                    )
                    newImage = Images(
                        finger = finger,
                        path = path
                    )
                    db.session.add(newImage)
                    db.session.commit()
                    _clone['files'].append(
                        {
                            'filename': file.filename,
                            'status': 'success',
                            'path': url_for('themes.upload',path=path)
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

#* editor cover 
@server.route('/editor/cover',methods=['POST'])
@login_required
def cover():
    if current_user.permission < Permission.USER:
        return uploadResponse['6003'];

    if 'file' not in request.files:
        return uploadResponse['6001'];

    _clone = deepcopy(uploadResponse['6000'])
    file = request.files.get('file')
    A_id = request.form.get('articleId',-1,type=int)
    article = current_user.article.filter_by(id=A_id).first();
    
    try:
        if not article:
            '''
                if not match article
            '''
            raise( InfoError("No article's id is %s" % str(A_id)) )
        
        data = file.read()
        size = len(data)
        if size > UPLOAD_MAX_SIZE:
            raise(UploadFileTooLarge('The file is too large'));
        finger = getFinger(data)
        images = Images.query.filter_by(finger = finger).first()
        if images:
            path = images.getImagePath()
            _clone['files'].append(
                {
                    'filename': file.filename,
                    'status': 'success',
                    'path': path
                }
            )
            article.updateCover(path)
        else:
            file.seek(0);
            sufix = getFiletype(file.filename)
            path = photos.save(
                file,
                folder=getDate(),
                name=finger + sufix
            )
            newImage = Images(
                finger = finger,
                path = path
            )
            db.session.add(newImage)
            article.updateCover(path)
            _clone['files'].append(
                {
                    'filename': file.filename,
                    'status': 'success',
                    'path': url_for('themes.upload',path=path)
                }
            )
            

        db.session.commit();
        return _clone;

    except UploadFileTooLarge as e:
        print(e)
        return uploadResponse["6002"];

    except InfoError as e:
        return uploadResponse["6001"];
    