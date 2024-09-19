from flask_restx import reqparse, fields
from src.extensions import api

geological_ns = api.namespace('Geological', description='API endpoint for Geological related operations', path='/api')

geological_model = api.model('Geological', {
    'id': fields.Integer(required=True, description='Geological id', example=1),
    'geological_survey': fields.Boolean(required=True, description='Geological survey', example=True),
    'objects_number': fields.Integer(required=True, description='Objects number', example=10),
    'boreholes': fields.Boolean(required=True, description='Boreholes', example=True),
    'boreholes_number': fields.Integer(required=True, description='Boreholes number', example=5),
    'pits': fields.Boolean(required=True, description='Pits', example=False),
    'pits_number': fields.Integer(required=True, description='Pits number', example=0),
    'laboratory_tests': fields.Boolean(required=True, description='Laboratory tests', example=True),
    'points_number': fields.Integer(required=True, description='Points number', example=20),
    'archival_material': fields.String(required=True, description='Archival material', example='Archival data')
})