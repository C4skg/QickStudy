from flask import request,session
from flask import redirect,url_for,render_template_string
from random import randint,sample
from string import digits,ascii_letters

from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
from base64 import b64encode

from . import api

@api.route('/verifyCode')
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



class verifyImgCode:
    '''
        verifycode class
    '''
    def rndColor(self):
        '''
            get the random color
        '''
        return (randint(32, 127), randint(32, 127), randint(32, 127))
    
    def gText(self):
        '''
            generate verify text
            4s
        '''
        code = ''.join(
            sample(digits + ascii_letters , 4)
        )
        return code

    def drawLines(self, draw, num, width, height):
        '''划线'''
        for num in range(num):
            x1 = randint(0, width / 2)
            y1 = randint(0, height / 2)
            x2 = randint(0, width)
            y2 = randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=1)
    
    def getImgCode(self,width:int=120,height:int=50):
        code = self.gText();

        img = Image.new(
            'RGB',
            (width,height),
            'white'
        )
        font = ImageFont.truetype(
            r'C:\Users\System-Pc\Desktop\arial.ttf',
            40
        )
        draw = ImageDraw.Draw(img)
        for item,v in enumerate(code):
            draw.text(
                (5 + randint(-3,3) + 23 * item,5 + randint(-3,3)),
                text=v,
                fill=self.rndColor(),
                font=font
            )

        self.drawLines(
            draw,
            4,
            width,
            height
        )

        #to base64
        data = BytesIO()
        img.save(data,format='PNG')
        dataBytes = data.getvalue()

        bytesEncode = b64encode(dataBytes).decode()

        return bytesEncode,code;
