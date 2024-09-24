from flask_restx import reqparse, fields
from src.extensions import api
import werkzeug

# from src.api.nsmodels.geological import geological_model
from src.api.nsmodels.geophysical import geophysical_vs30_model

projects_ns = api.namespace('Projects', description='API endpoint for Projects related operations', path='/api')

projects_img_model = projects_ns.model('Image', {
    'id': fields.Integer(required=True, description='Image ID', example=1),
    'path': fields.String(required=True, description='Image path', example='3419382269fa.png')
})

projects_model = projects_ns.model('Projects', {
    'id': fields.Integer(required=True, description='Project id', example=1),
    'projects_name': fields.String(required=True, description='Project name', example='New Project'),
    'contract_number': fields.String(required=False, description='Contract number', example='1A2345'),
    'start_time': fields.Date(required=True, description='Start time (YYYY-MM-DD)', example='2024-01-23'),
    'end_time': fields.Date(required=True, description='End time (YYYY-MM-DD)', example='2024-03-03'),
    'contractor': fields.String(required=False, description='Contractor', example='New Contractor'),
    'proj_location': fields.String(required=True, description='Project location', example='Example Location'),
    'proj_latitude': fields.Float(required=True, description='Project latitude', example=42.0163),
    'proj_longitude': fields.Float(required=True, description='Project longitude', example=43.1412),
    'geological_study': fields.Boolean(required=False, description='Geological study', example=True),
    'geophysical_study': fields.Boolean(required=False, description='Geophysical study', example=False),
    'hazard_study': fields.Boolean(required=False, description='Hazard study', example=True),
    'geodetic_study': fields.Boolean(required=False, description='Geodetic study', example=False),
    'other_study': fields.Boolean(required=False, description='Other study', example=False),
    # 'geological': fields.List(fields.Nested(geological_model))
    'geophysical': fields.List(fields.Nested(geophysical_vs30_model))
    # 'images': fields.List(fields.Nested(projects_img_model), description='List of images')
})

def empty_or_none(value, name):
    if value == "":
        return None
    return str(value)

projects_parser = reqparse.RequestParser()

projects_parser.add_argument("projects_name", required=True, type=str, help="Project name example: AKHN Project")
projects_parser.add_argument("contract_number", required=False, type=empty_or_none, help="Contract number example: 12345")
projects_parser.add_argument("start_time", required=True, type=str, help="Start time example: 2024-08-13")
projects_parser.add_argument("end_time", required=True, type=str, help="End time example: 2024-08-16")
projects_parser.add_argument("contractor", required=False, type=empty_or_none, help="Contarctor name example: AKHN Contractor")
projects_parser.add_argument("proj_location", required=True, type=str, help="Project location example: ახალქალაქი")
projects_parser.add_argument("proj_latitude", required=True, type=float, help="Latitude example: 41.4256")
projects_parser.add_argument("proj_longitude", required=True, type=float, help="Longitude example: 43.513")
projects_parser.add_argument("images", required=False, type=werkzeug.datastructures.FileStorage, location="files", action="append", help="Upload images (JPEG/PNG/JPG)")


project_img_parser = reqparse.RequestParser()
project_img_parser.add_argument("images", required=True, type=werkzeug.datastructures.FileStorage, location="files", action="append", help="Upload images (JPEG/PNG/JPG)")
