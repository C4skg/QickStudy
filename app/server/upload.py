from flask import request
from flask_login import login_required
from flask_login import current_user
from flask_uploads import UploadNotAllowed

from ..models import Permission
from ..responseData import uploadResponse
from .. import photos
from . import server

@server.route('/uupload',methods=['POST'])
# @login_required
def photoUpload():
    if request.method == 'POST':
        print(request.form)
    # if current_user.permission < Permission.USER:
    #     return uploadResponse['6002']
    # try:
        # filename = photos.save(request.files[''])
    # pass;
    # print(
        # request
    # )

    return '';
