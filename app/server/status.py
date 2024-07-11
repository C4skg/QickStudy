from flask import current_app
from flask_login import current_user

from . import server


@server.route("/status")
def status():
    return {};