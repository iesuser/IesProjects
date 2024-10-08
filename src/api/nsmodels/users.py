from flask_restx import reqparse, fields
from src.extensions import api


users_ns = api.namespace('Users', description='API endpoint for Role Management', path='/api')

# Role model for documentation in Swagger UI
roles_model = users_ns.model('Roles', {
    'name': fields.String(required=True, description='Role Name'),
    'is_admin': fields.Boolean(description='Admin Privileges'),
    'can_users': fields.Boolean(description='Permission to manage users'),
    'can_project': fields.Boolean(description='Permission to manage projects'),
    'can_geophysic': fields.Boolean(description='Permission to manage geophysic data'),
    'can_geologic': fields.Boolean(description='Permission to manage geologic data'),
    'can_hazard': fields.Boolean(description='Permission to manage hazard data'),
    'can_geodetic': fields.Boolean(description='Permission to manage geodetic data'),
})
