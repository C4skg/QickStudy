from flask import request,current_app
from flask import render_template
from flask_login import login_required

from ..config import html
from . import main

@main.route('/',methods=['GET','POST'])
@login_required
def index():
    path = request.args.get('path','/',type=str)

    return render_template('index.html',title=html['title']);