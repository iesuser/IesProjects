from flask_restx import Resource
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity

from src.models import User, Role
from src.api.nsmodels import accounts_ns, user_model, user_parser, accounts_model, roles_model, roles_parser


@accounts_ns.route('/user')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class UserApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.marshal_with(user_model)
    def get(self):
        identity = get_jwt_identity()
        user = User.query.filter_by(uuid=identity).first()

        if user:
            role = Role.query.filter_by(id=user.role_id).first()
            user.role_name = role.name
            if not role:
                return {"error": "როლი ვერ მოიძებნა."}, 400
            return user, 200
        else:
            return {'error': 'მომხმარებელი ვერ მოიძებნა.'}, 404

@accounts_ns.route('/accounts')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class UserListApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.marshal_with(accounts_model)
    def get(self):
        # Check if the user has permission
        if not current_user.check_permission('can_users'):
            return {"error": "არ გაქვს მომხმარებლის ნახვის ნებართვა."}, 403

        # Query all users from the database
        users = User.query.all() 
        # Prepare the response data using a list comprehension
        result = [
            {
                "id": user.id,
                "username": f"{user.name} {user.lastname}",
                "email": user.email,
                "role": {
                    "name": user.role.name if user.role else "No Role",
                    "is_admin": user.role.is_admin if user.role else False,
                    "can_users": user.role.can_users if user.role else False,
                    "can_project": user.role.can_project if user.role else False,
                    "can_geophysic": user.role.can_geophysic if user.role else False,
                    "can_geologic": user.role.can_geologic if user.role else False,
                    "can_hazard": user.role.can_hazard if user.role else False,
                    "can_geodetic": user.role.can_geodetic if user.role else False,
                } if user.role else None,
            }
            for user in users
        ]

        return result, 200

@accounts_ns.route('/account/<string:uuid>')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class AccountAPI(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.expect(user_parser)
    def put(self, uuid):
        identity = get_jwt_identity()
        check_user = User.query.filter_by(uuid=identity).first()

        if identity == uuid or (check_user and check_user.role.name == "Admin"):
            user = User.query.filter_by(uuid=uuid).first()

            if not user:
                return {'error': 'მომხმარებელი ვერ მოიძებნა.'}, 404

            args = user_parser.parse_args()

            # Change password logic
            if args.get('change_password'):
                # Verify old password
                if not user.check_password(args.get("old_password")):
                    return {'error': 'ძველი პაროლი არასწორად არის შეყვანილი.'}, 400
                
                # Check if new password is provided and valid
                new_password = args.get("new_password")
                repeat_new_password = args.get("repeat_new_password")

                if not new_password or not repeat_new_password:
                    return {"error": "გთხოვთ შეიყვანოთ ახალი პაროლი და მისი გაწვდილი."}, 400

                if new_password != repeat_new_password:
                    return {"error": "ახალი პაროლები არ ემთხვევა ერთმანეთს."}, 400

                if new_password == args.get("old_password"):
                    return {"error": "ახალი პაროლი უნდა განსხვავდება ძველისგან."}, 400

                if len(new_password) < 8:
                    return {"error": "პაროლი უნდა იყოს მინიმუმ 8 სიმბოლო."}, 400

                # Update the password
                user.password = new_password

            if check_user.role.name == "Admin":
                # Verify old password when not changing it
                role = Role.query.filter_by(name=args["role_name"]).first()
                if not role:
                    return {"error": "როლი ვერ მოიძებნა."}, 400
                user.role_id = role.id
                
            # Update user fields
            user.name = args["name"]
            user.lastname = args["lastname"]
            
            # Save changes
            user.save()

            return {'message': 'მონაცემები წარმატებით განახლდა.'}, 200
        else:
            return {'error': "არ გაქვს მონაცემების განახლების ნებართვა."}, 403


@accounts_ns.route('/roles')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class RolesListApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.marshal_with(roles_model)
    def get(self):
        # Check if the user has permission
        if not current_user.check_permission('can_users'):
            return {"error": "არ გაქვს მომხმარებლის ნახვის ნებართვა."}, 403
        
        # Fetch all roles from the database
        roles = Role.query.all()
        
        if not roles:
            return {'error': 'როლი ვერ მოიძებნა.'}, 404
        
        return roles, 200

@accounts_ns.route('/roles/<int:role_id>')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class RolesAPI(Resource):
    @jwt_required()
    @accounts_ns.doc(parser=roles_parser)
    @accounts_ns.doc(security = 'JsonWebToken')
    def put(self):
        """Update an existing role"""
        args = roles_parser.parse_args()
        
        # Query the role by ID, not name
        role = Role.query.get(role_id)

        if not role:
            return {"error": "Role not found."}, 404

        # Update role fields if provided
        if args['is_admin'] is not None:
            role.is_admin = args['is_admin']
        if args['can_users']:
            role.can_users = args['can_users']
        if args['can_project']:
            role.can_project = args['can_project']
        if args['can_geophysic']:
            role.can_geophysic = args['can_geophysic']
        if args['can_geologic']:
            role.can_geologic = args['can_geologic']
        if args['can_hazard']:
            role.can_hazard = args['can_hazard']
        if args['can_geodetic']:
            role.can_geodetic = args['can_geodetic']

        role.save()
        return {"message": f"Role '{role.name}' updated successfully."}, 200