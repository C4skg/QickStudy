import os
from base64 import b64encode
from io import BytesIO
from PIL import Image,ImageFont,ImageDraw
from random import randint,sample
from string import digits,ascii_letters

'''
更具字符串首个字符生成图片
'''
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

'''
生产随机字符串
'''
def getRandomStr(nums:int) -> str:
    return ''.join(
            sample(digits + ascii_letters , k=nums)
        )

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
            draw.line(((x1, y1), (x2, y2)), fill=self.rndColor(), width=1)
    
    def getImgCode(self,width:int=120,height:int=50):
        code = self.gText();

        img = Image.new(
            'RGBA',
            (width,height),
            (0,0,0,0)
        )
        font = ImageFont.truetype(
            os.path.join(os.getcwd() , 'font/VF-Thin.ttf'),
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