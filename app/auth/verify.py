import re
from ..models import User


def isVaildRegister(email:str,pwd:str) -> bool:
    email = email.strip().lower();
    pwd = pwd.strip();
    if not isVaildPwd(pwd) or not isVaildEmail(email):
        return False;

    return True;

def registerUserExisit(email:str) -> bool:
    email = email.strip().lower()
    user = User.query.filter_by(email=email).first();
    if user:
        return True
    else:
        return False
    
def isVaildEmail(email:str) -> bool:
    email = email.strip().lower()
    if not re.match(r'^\w+@\w+\.[a-z]{1,}$',email,re.I):
        return False;

    return True;

def isVaildPwd(pwd:str) -> bool:
    pwd = pwd.strip();
    if len(pwd) < 6 or not re.match(r'^(?=.*[A-Za-z])(?=.*\d).{6,}$',pwd):
        return False;

    return True;