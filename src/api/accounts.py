from flask_restx import Resource
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity

from src.models import User, Role
from src.api.nsmodels import accounts_ns, user_model, user_parser, accounts_model, accounts_parser, roles_model, roles_parser


@accounts_ns.route('/user')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class UserApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.marshal_with(user_model)
    def get(self):
        """საკუთარი მომხმარებლის მონაცემების მიღება"""
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

@accounts_ns.route('/user/<string:uuid>')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class UserUpdateAPI(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.expect(user_parser)
    def put(self, uuid):
        """შესაძლებელია საკუთარი მონაცემის განახლება"""
        identity = get_jwt_identity()
        check_user = User.query.filter_by(uuid=identity).first()

        if identity == uuid:
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
                
            # Update user fields
            user.name = args["name"]
            user.lastname = args["lastname"]
            
            # Save changes
            user.save()

            return {'message': 'მონაცემები წარმატებით განახლდა.'}, 200
        else:
            return {'error': "არ გაქვს მონაცემების განახლების ნებართვა."}, 403

@accounts_ns.route('/accounts')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class AccountsListApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.marshal_with(accounts_model)
    def get(self):
        """მომხმარებლების სიის მიღება, წვდომა აქვს მხოლოდ role-ით (can_users) """
        # Check if the user has permission
        if not current_user.check_permission('can_users'):
            return {"error": "არ გაქვს მომხმარებლის ნახვის ნებართვა."}, 403

        # Query all users from the database
        users = User.query.all()
        # Prepare the response data using a list comprehension
        result = [
            {
                "uuid": user.uuid,
                "username": f"{user.name} {user.lastname}",
                "email": user.email,
                "role": {
                    "id": user.role.id if user.role else "null",
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
@accounts_ns.route('/accounts/<string:uuid>')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class AccountsApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.doc(parser=accounts_parser)
    def put(self, uuid):
        """მომხმარებლის როლის შეცვლა, წვდომა აქვს მხოლოდ role-ით (can_users)"""
        # Check if the user has permission
        if not current_user.check_permission('can_users'):
            return {"error": "არ გაქვს მომხმარებლის ნახვის ნებართვა."}, 403

        args = accounts_parser.parse_args()
        role_id = args["role_id"]

        user = User.query.filter_by(uuid=uuid).first()
        if not user:
            return {"error": "მომხმარებელი არ მოიძებნა"}, 404
            
        role = Role.query.get(role_id)
        if not role:
            return {"error": "როლი არ მოიძებნა"}, 404
        
        user.role_id = role_id
        user.save()
        return {"message": "მომხმარებლის როლი წარმატებით განახლდა"}, 200

@accounts_ns.route('/roles')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class RolesListApi(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.marshal_with(roles_model)
    def get(self):
        """როლების სიის მიღება, წვდომა აქვს მხოლოდ role-ით (can_users)"""
        # Check if the user has permission
        if not current_user.check_permission('can_users'):
            return {"error": "არ გაქვს მომხმარებლის ნახვის ნებართვა."}, 403
        
        # Fetch all roles from the database
        roles = Role.query.all()
        
        if not roles:
            return {'error': 'როლი ვერ მოიძებნა.'}, 404
        
        return roles, 200
    
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.doc(parser=roles_parser)
    def post(self):
        """როლის დამატება, წვდომა აქვს მხოლოდ role-ით (can_users)"""
        # Check if the user has permission
        if not current_user.check_permission('can_users'):
            return {"error": "არ გაქვს მომხმარებლის განახლების ნებართვა."}, 403
        
        # Parse the input arguments
        args = roles_parser.parse_args()
        
        # Check if the role already exists
        if Role.query.filter_by(name=args['name']).first():
            return {"error": "ეს როლი უკვე არსებობს."}, 400
        
        # Create a new role
        new_role = Role(
            name=args['name'],
            is_admin=args.get('is_admin', False),
            can_users=args.get('can_users', False),
            can_project=args.get('can_project', False),
            can_geophysic=args.get('can_geophysic', False),
            can_geologic=args.get('can_geologic', False),
            can_hazard=args.get('can_hazard', False),
            can_geodetic=args.get('can_geodetic', False)
        )
        
        # Save the new role to the database
        new_role.create()
        return {"message": f"როლი წარმატებით დაემატა."}, 200

@accounts_ns.route('/roles/<int:role_id>')
@accounts_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Forbidden', 404: 'Not Found'})
class RolesAPI(Resource):
    @jwt_required()
    @accounts_ns.doc(security='JsonWebToken')
    @accounts_ns.marshal_with(roles_model)
    def get(self, role_id):
        """როლის დეტალების მიღება, წვდომა აქვს მხოლოდ role-ით (can_users)"""
        # Check if the user has permission
        if not current_user.check_permission('can_users'):
            return {"error": "არ გაქვს მომხმარებლის ნახვის ნებართვა."}, 403
        
        # Fetch the role by ID
        role = Role.query.get(role_id)
        
        if not role:
            return {'error': 'როლი ვერ მოიძებნა.'}, 404
        
        return role, 200

    @jwt_required()
    @accounts_ns.doc(security = 'JsonWebToken')
    @accounts_ns.doc(parser=roles_parser)
    def put(self, role_id):
        """როლის განახლება, წვდომა აქვს მხოლოდ role-ით (can_users)"""
        # Check if the user has permission
        if not current_user.check_permission('can_users'):
            return {"error": "არ გაქვს მომხმარებლის განახლების ნებართვა."}, 403

        args = roles_parser.parse_args()
        # Query the role by ID, not name
        role = Role.query.get(role_id)

        if not role:
            return {"error": "როლი ვერ მოიძებნა."}, 404

        # Update role fields if provided
        if args['name'] is not None:
            role.name = args['name']
        if args['is_admin'] is not None:
            role.is_admin = args['is_admin']
        if args['can_users'] is not None:
            role.can_users = args['can_users']
        if args['can_project'] is not None:
            role.can_project = args['can_project']
        if args['can_geophysic'] is not None:
            role.can_geophysic = args['can_geophysic']
        if args['can_geologic'] is not None:
            role.can_geologic = args['can_geologic']
        if args['can_hazard'] is not None:
            role.can_hazard = args['can_hazard']
        if args['can_geodetic'] is not None:
            role.can_geodetic = args['can_geodetic']

        role.save()
        return {"message": f"როლი წარმატებით განახლდა."}, 200