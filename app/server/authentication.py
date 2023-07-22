from flask import request,session,current_app
from flask import Response
from flask import redirect,url_for,render_template_string

from base64 import b64decode

from ..func import verifyImgCode,generateUID
from .. import redisClient
from . import server


def resetVCode(id:str):
    data,code = verifyImgCode().getImgCode();
    redisClient.hset(id,'img',data);
    redisClient.hset(id,'code',code)
    redisClient.expire(id,time=300)
    return (data,code)

@server.route('/verifyCode')
def getVCodeImg():
    id = session[current_app.config.get('SESSION_ID')];
    b64data = redisClient.hget(id,'img');
    if not b64data:
        b64data,code = resetVCode(id);


    data = b64decode(
        b64data.decode()
    )
    return Response(
        data,
        mimetype='image/png'
    )


    

@server.route('/resetCode')
def reload():
    id = session[current_app.config.get('SESSION_ID')]
    resetVCode(id);
    return 'ok';
