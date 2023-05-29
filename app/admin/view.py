from flask import render_template
from flask import session

from . import admin


@admin.route('/')
def adminPage():

    return render_template('admin/index.html');