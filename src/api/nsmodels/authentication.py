from flask_restx import reqparse, inputs, fields
from src.extensions import api


auth_ns = api.namespace('Authentification', description='API endpoint for Authentification related operations', path='/api')

registration_parser = reqparse.RequestParser()
registration_parser.add_argument('name', type=str, required=True, help="Name example: Roma (1-20 characters)")
registration_parser.add_argument('lastname', type=str, required=True, help="LastName example: Grigalashvili (1-20 characters)")
registration_parser.add_argument('email', type=inputs.email(check=True), required=True, help="Email example: roma.grigalashvili@iliauni.edu.ge")
registration_parser.add_argument('password', type=str, required=True, help="Password example: Grigalash1")
registration_parser.add_argument('passwordRepeat', type=str, required=True, help='Repeat the password example: Grigalash1')
registration_parser.add_argument('role_name', type=str, required=False, help="Name of the role example: User")

# auth parser
auth_parser = reqparse.RequestParser()
auth_parser.add_argument("email", required=True, type=str, help="Email example: roma.grigalashvili@iliauni.edu.ge")
auth_parser.add_argument("password", required=True, type=str, help="Password example: Grigalash1")

user_model = auth_ns.model('User', {
    'uuid': fields.String(required=True, type=str, description='The unique UUID of the user'),
    'name': fields.String(required=True, type=str, description='The name of the user'),
    'lastname': fields.String(required=True,  type=str, description='The lastname of the user'),
    'email': fields.String(required=True, type=inputs.email(check=True), description='The email of the user'),
    'role_name': fields.String(required=True, type=str, description='The role ID associated with the user')
})

# auth parser
user_parser = reqparse.RequestParser()

user_parser.add_argument('name', required=True, type=str, help='Name example: Roma (1-20 characters)')
user_parser.add_argument('lastname', required=True, type=str, help='LastName example: Grigalashvili (1-20 characters)')
user_parser.add_argument("old_password", required=False, type=str, help="Old password example: Grigalash1")
user_parser.add_argument("new_password", required=False, type=str, help="New Password example: Grigalash27")
user_parser.add_argument("repeat_new_password", required=False, type=str, help="Repeat new Password example: Grigalash27")
user_parser.add_argument("change_password", required=True, type=inputs.boolean, help="Password example: true")
user_parser.add_argument('role_name', required=True, type=str, help='Name of the role example: User')