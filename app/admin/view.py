from flask import render_template
from flask import current_app

from . import admin


@admin.route('/')
def adminPage():
    return render_template('admin/index.html');