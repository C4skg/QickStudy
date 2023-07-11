from flask import request
from flask import redirect,url_for,render_template_string


from ..func import verifyImgCode
from . import server

@server.route('/verifyCode')
def verifyCode():
    width = request.args.get('w',120,int)
    height = request.args.get('h',50,int)
    data,code = verifyImgCode().getImgCode();
    return render_template_string(
        '''
        <img src='data:image/png;base64,{{data}}' />
        ''',
        data = data
    );


