from flask import current_app
from flask_login import current_user
from flask_login import login_required

from . import php



@php.before_request
def before_request():
    if current_user.is_authenticated:
        pass;
    else:
        return (
            '''
                I hope you can find the leak on my website,
                and I will give you a flag as a reward
            '''
        )
    
@php.route('/ok.php')
def ok():
    return 'phpinfo();'