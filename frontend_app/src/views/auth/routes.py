from flask import render_template, Blueprint
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, "src","templates", "auth")
auth_blueprint = Blueprint("auth", __name__, template_folder=TEMPLATES_FOLDER)


@auth_blueprint.route("/login")
def auth():
    return render_template("login.html")

@auth_blueprint.route("/registration")
def registration():
    return render_template("registration.html")