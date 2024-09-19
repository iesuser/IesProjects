from flask_restx import reqparse, fields
from src.extensions import api
import werkzeug

from src.api.nsmodels.geophysical import geophysical_vs30_model

filter_ns = api.namespace('Filters', description='API endpoint for Filters related operations', path='/api')

filter_model = filter_ns.model('Filters', {
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
    'geophysical': fields.List(fields.Nested(geophysical_vs30_model))
})

def empty_or_none(value, name):
    if value == "":
        return None
    return str(value)


filter_parser = reqparse.RequestParser()

filter_parser.add_argument("proj_location", type=empty_or_none, help="Project location")
filter_parser.add_argument("contract_number", type=empty_or_none, help="Contract number")
filter_parser.add_argument('vs30_min', type=empty_or_none, help="VS30 Value")
filter_parser.add_argument('vs30_max', type=empty_or_none, help="VS30 Value")
filter_parser.add_argument("start_time", type=empty_or_none, help="Start time")
filter_parser.add_argument("end_time", type=empty_or_none, help="End time")
filter_parser.add_argument('pga', type=empty_or_none, action='append', required=False, help='Selected PGA values')