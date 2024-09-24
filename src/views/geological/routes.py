from flask import render_template, Blueprint
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, "templates", "geological")
geological_blueprint = Blueprint("geological", __name__, template_folder=TEMPLATES_FOLDER)


@geological_blueprint.route("/projects")
def projects():
    return render_template("projects.html")

@geological_blueprint.route('/create_project', methods=['GET', 'POST'])
def create_project():
    return render_template("create_project.html")

@geological_blueprint.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    return render_template("edit_project.html", project_id=id)