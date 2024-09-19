from flask_restx import reqparse, fields
from src.extensions import api
from werkzeug.datastructures import FileStorage


geophysical_ns = api.namespace('Geophysical', description='API endpoint for Geophysical related operations', path='/api')

geophysical_model = api.model('Geophysical', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a geophysical record'),
    'project_id': fields.Integer(required=True, description='The ID of the related project'),
    'vs30': fields.Integer(required=True, description='VS30 value'),
    'ground_category_geo': fields.String(required=True, description='Geological ground category'),
    'ground_category_euro': fields.String(required=True, description='European ground category'),
    'seismic_profiles': fields.Boolean(required=True, description='Whether seismic profiles are included'),
    'profiles_number': fields.Integer(required=True, description='Number of profiles'),
    'geophysical_logging': fields.Boolean(required=True, description='Whether geophysical logging is included'),
    'logging_number': fields.Integer(required=True, description='Number of loggings'),
    'electrical_profiles': fields.Boolean(required=True, description='Whether electrical profiles are included'),
    'point_number': fields.Integer(required=True, description='Number of points'),
    'georadar': fields.Boolean(required=True, description='Whether georadar is included'),
    'archival_excel': fields.String(description='The URL of the archival Excel file'),
    'archival_pdf': fields.String(description='The URL of the archival PDF')
})

geophysical_vs30_model = api.model('Geophysical', {
    'vs30': fields.Integer(required=True, description='VS30 value'),
})

geophysical_parser = reqparse.RequestParser()

geophysical_parser.add_argument('vs30', type=int, required=True, default=500, help="VS30 Value")
geophysical_parser.add_argument('ground_category_geo', type=str, required=True, default="II", help='Geological ground category')
geophysical_parser.add_argument('ground_category_euro', type=str, required=True, default="B", help='European ground category')
geophysical_parser.add_argument("archival_excel", required=False, type=FileStorage, location="files", action="append", help="Upload archival EXCEL (XLS/XLSX)")
geophysical_parser.add_argument("archival_pdf", required=False, type=FileStorage, location="files", action="append", help="Upload archival PDF (PDF)")

