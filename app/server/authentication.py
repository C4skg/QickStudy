from flask import request
from flask import Response
from flask import redirect,url_for,render_template_string

from base64 import b64decode

from ..func import verifyImgCode
from .. import redisClient
from . import server


def resetVCode(ip:str):
    data,code = verifyImgCode().getImgCode();
    redisClient.hset(ip,'img',data);
    redisClient.hset(ip,'code',code)
    redisClient.expire(ip,time=300)
    return (data,code)

@server.route('/verifyCode')
def getVCodeImg():
    b64data = redisClient.hget(request.remote_addr,'img');
    if not b64data:
        b64data,code = resetVCode(request.remote_addr);


    data = b64decode(
        b64data.decode()
    )
    return Response(
        data,
        mimetype='image/png'
    )


    

@server.route('/resetCode')
def reload():
    resetVCode(request.remote_addr);
    return 'ok';
