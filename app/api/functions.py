from flask import redirect,url_for
from flask import request

import os
from base64 import b64encode
from io import BytesIO
from PIL import Image,ImageFont
from PIL import ImageDraw

from . import api

def generateImgByName(name:str) -> str:
    '''
        default size : 100*100
        @return: base64 encode data
        
        @tips: <img src='data:image/png;base64,data'/>
    '''
    name = name.upper()
    width = 100
    height = 100
    img = Image.new('RGB',(width,height),(11,94,215))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        os.path.join(os.getcwd() , 'font/DK.ttf'),
        80
    )
    fw,fh = font.getsize(name[0]);

    draw.text(
        ((width - fw)/2,(height - fh)/2),
        name[0],
        font=font,
        fill=(255,255,255)
    )
    buffer = BytesIO()
    img.save(buffer,'png')
    
    return b64encode(buffer.getvalue()).decode()