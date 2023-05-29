import re
from ..models import User


def isVaildRegister(email:str,pwd:str) -> bool:
    email = email.strip();
    pwd = pwd.strip();

    if email == '' or pwd == '':
        return '邮箱或密码不能为空';
    if not re.match(r'^\w+@\w+\.[a-z]{1,}$',email,re.I):
        return '邮箱格式不正确';
    if len(pwd) < 6 or not re.match(r'^(?=.*[A-Za-z])(?=.*\d).{6,}$',pwd):
        return '密码格式不正确';

    return 'ok';

def registerUserExisit(email:str) -> bool:
    email = email.lower()
    user = User.query.filter_by(email=email).first();
    if user:
        return True
    else:
        return False