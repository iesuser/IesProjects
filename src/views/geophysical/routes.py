from flask import render_template, Blueprint, send_from_directory, abort
from os import path

from src.config import Config
from src.models import Geophysical

# Define the folder path for the templates
TEMPLATES_FOLDER = path.join(Config.BASE_DIR, "src/templates", "geophysical")

# Create a Blueprint for the geophysical routes
geophysical_blueprint = Blueprint("geophysical", __name__, template_folder=TEMPLATES_FOLDER)


# Route to view a specific Geophysical record by its ID
@geophysical_blueprint.route("/view_geophysical/<int:id>")
def view_geophysical(id):
    geophysical_record = Geophysical.query.get(id)
    if not geophysical_record:
        abort(404, description="Geophysical record not found")
    proj_id = geophysical_record.project_id

    # Render the template for viewing the Geophysical record
    return render_template("view_geophysical.html", geophysical_id=id, project_id=proj_id)


# Route to serve archival material (like PDFs) for a specific project ID
@geophysical_blueprint.route('/<int:proj_id>/geophysical/archival_excel/<filename>')
def archival_excel(proj_id, filename):
    directory = f'temp/{proj_id}/geophysical/archival_excel/'
    return send_from_directory(directory, filename)

# Route to serve archival material (like PDFs) for a specific project ID
@geophysical_blueprint.route('/<int:proj_id>/geophysical/archival_pdf/<filename>')
def archival_pdf(proj_id, filename):
    directory = f'temp/{proj_id}/geophysical/archival_pdf/'
    return send_from_directory(directory, filename)

# Route to serve seismic archival images for a specific Geophysical record
@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/seismic/archival_img/<filename>')
def geophySeismic_img(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/seismic/archival_img/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/seismic/archival_excel/<filename>')
def geophySeismic_excel(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/seismic/archival_excel/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/seismic/archival_pdf/<filename>')
def geophySeismic_pdf(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/seismic/archival_pdf/'
    return send_from_directory(directory, filename)


# Route to serve logging archival images for a specific Geophysical record
@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/logging/archival_img/<filename>')
def geophyLogging_img(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/logging/archival_img/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/logging/archival_excel/<filename>')
def geophyLogging_excel(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/logging/archival_excel/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/logging/archival_pdf/<filename>')
def geophyLogging_pdf(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/logging/archival_pdf/'
    return send_from_directory(directory, filename)


# Route to serve electrical archival images for a specific Geophysical record
@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/electrical/archival_img/<filename>')
def geophyElectrical_img(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/electrical/archival_img/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/electrical/archival_excel/<filename>')
def geophyElectrical_excel(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/electrical/archival_excel/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/electrical/archival_pdf/<filename>')
def geophyElectrical_pdf(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/electrical/archival_pdf/'
    return send_from_directory(directory, filename)


# Route to serve georadar archival images for a specific Geophysical record
@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/georadar/archival_img/<filename>')
def geophyGeoradar_img(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/georadar/archival_img/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/georadar/archival_excel/<filename>')
def geophyGeoradar_excel(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/georadar/archival_excel/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/georadar/archival_pdf/<filename>')
def geophyGeoradar_pdf(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/georadar/archival_pdf/'
    return send_from_directory(directory, filename)
