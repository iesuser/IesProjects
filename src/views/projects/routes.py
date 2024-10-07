from flask import render_template, Blueprint, send_from_directory
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, Config.TEMPLATES_FOLDERS, "projects")
projects_blueprint = Blueprint("projects", __name__, template_folder=TEMPLATES_FOLDER)


@projects_blueprint.route("/view_project/<int:id>")
def view_projects(id):
    return render_template("view_project.html", project_id=id)

@projects_blueprint.route('/images/<int:proj_id>/<filename>')
def project_image(proj_id, filename):
    directory = path.join(Config.UPLOAD_FOLDER, str(proj_id), 'images') 
    return send_from_directory(directory, filename)