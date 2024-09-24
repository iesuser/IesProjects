from flask.cli import with_appcontext
import click
from datetime import datetime
from werkzeug.security import generate_password_hash

from src.extensions import db
from src.models import Projects, Geological, Geophysical, GeophysicSeismic, GeophysicLogging, GeophysicElectrical
from src.models import User, Role


@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Creating Database")
    db.drop_all()
    db.create_all()
    click.echo("Database Created")

@click.command("populate_db")
@with_appcontext
def populate_db():
    click.echo("Creating First Project")
    new_project = Projects(
        projects_name="New Project",
        contract_number=12345,
        start_time=datetime.strptime('2024-01-23', '%Y-%m-%d').date(),
        end_time=datetime.strptime('2024-03-03', '%Y-%m-%d').date(),
        contractor="New Contractor",
        proj_location="Example Location",
        proj_latitude=42.1234,
        proj_longitude=43.649
    )
    new_project.create()

    click.echo("Creating Second Project")
    new_project = Projects(
        projects_name="Main Project",
        contract_number=12345,
        start_time=datetime.strptime('2024-02-23', '%Y-%m-%d').date(),
        end_time=datetime.strptime('2024-07-03', '%Y-%m-%d').date(),
        contractor="Main Contractor",
        proj_location="Example Location",
        proj_latitude=42.1234,
        proj_longitude=42.649
    )
    new_project.create()

    # click.echo("Creating First Geological")
    # new_geological = Geological(
    #     project_id = 1,
    #     geological_survey = True,
    #     objects_number = 2,
    #     boreholes = False,
    #     boreholes_number = 0,
    #     pits = False,
    #     pits_number = 0,
    #     laboratory_tests = True,
    #     points_number = 2,
    #     archival_material = "archival_material.xlsx"
    # )

    # new_geological.create()

    # click.echo("Creating Second Geological")
    # new_geological = Geological(
    #     project_id = 1,
    #     geological_survey = False,
    #     objects_number = 0,
    #     boreholes = False,
    #     boreholes_number = 0,
    #     pits = False,
    #     pits_number = 0,
    #     laboratory_tests = True,
    #     points_number = 20,
    #     archival_material = "example_material.xlsx"
    # )

    # new_geological.create()


    click.echo("Creating First Geophysical")
    new_geophysical = Geophysical(
        project_id=1,
        vs30=600,
        ground_category_geo="II",
        ground_category_euro="B",
        # archival_material="main_material.xlsx"
    )

    new_geophysical.create()

    click.echo("Creating First GeophysicSeismic")
    new_geophysical_seismic = GeophysicSeismic(
        geophysical_id=1,
        longitude=42.1234,
        latitude=42.549,
        profile_length=0,
        vs30=650,
        ground_category_geo="II",
        ground_category_euro="B",
        # archival_img="image.png",
        # archival_excel="test.xlsx",
        # archival_pdf="testarchve.pdf"
    )

    new_geophysical_seismic.create()

    click.echo("Creating Second GeophysicSeismic")
    new_geophysical_seismic = GeophysicSeismic(
        geophysical_id=1,
        longitude=42.1234,
        latitude=42.549,
        profile_length=0,
        vs30=550,
        ground_category_geo="II",
        ground_category_euro="B",
        # archival_img="image.png",
        # archival_excel="test.xlsx",
        # archival_pdf="testarchve.pdf"
    )

    new_geophysical_seismic.create()


    click.echo("Creating First GeophysicLogging")
    new_geophysical_logging = GeophysicLogging(
        geophysical_id=1,
        longitude=41.1234,
        latitude=42.549,
        profile_length=10,
        # archival_img="image.png",
        # archival_excel="test.xlsx",
    )

    new_geophysical_logging.create()

    click.echo("Creating First GeophysicElectrical")
    new_geophysic_electrical = GeophysicElectrical(
        geophysical_id=1,
        longitude=41.1234,
        latitude=42.549,
        profile_length=0,
        # archival_img="image.png",
        # archival_excel="test.xlsx",
    )

    new_geophysic_electrical.create()

    click.echo("Creating Role")
    role = Role(name="Admin", is_admin=True, can_project=True, can_geophysic=True,
                 can_geologic=True, can_geodetic=True, can_hazard=True)
    role.create()
    role = Role(name="User")
    role.create()

    click.echo("Creating User")
    admin_user = User (
        name="Roma",
        lastname="Grigalashvili",
        email="roma.grigalashvili@iliauni.edu.ge",
        password="Grigalash1",
        role_id=1
    )
    admin_user.create()

@click.command("insert_db")
@with_appcontext
def insert_db():

    click.echo("Update Password")
    user = User.query.filter_by(email="roma.grigalashvili@iliauni.edu.ge").first()
    if user:
        user.password="Grigalash1"

        user.save()
        click.echo("Password updated successfully.")

    else:
        click.echo("This User Not Found.")

    # click.echo("Update Role")
    # role = Role.query.filter_by(name="User").first()
    
    # if role:
    #     # Update existing Role attributes
    #     role.is_admin = False
    #     role.can_project = False
    #     role.can_geophysic = False
    #     role.can_geologic = False
    #     role.can_geodetic = False
    #     role.can_hazard = False
    #     role.save()
    #     click.echo("Role updated successfully.")

    # else:
    #     click.echo("This Role Not Found.")
    

    # click.echo("Create Role")
    # # Create a new Admin role if it does not exist
    # role = Role(
    #     name="Geophysicist",
    #     is_admin=False,
    #     can_project=True,
    #     can_geophysic=True,
    #     can_geologic=False,
    #     can_geodetic=False,
    #     can_hazard=False
    # )
    # role.create()
    # click.echo("Created New Role successfully.")