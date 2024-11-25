from flask_restx import Resource
from datetime import datetime
from flask_jwt_extended import jwt_required
from sqlalchemy import and_

from src.api.nsmodels import filter_ns, filter_parser, filter_model
from src.models import Projects, Geophysical


@filter_ns.route('/filter_project')
@filter_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class FilterProjectAPI(Resource):
    @jwt_required()
    @filter_ns.doc(parser=filter_parser)
    @filter_ns.doc(security='JsonWebToken')
    @filter_ns.marshal_list_with(filter_model)
    def post(self):
        '''გავფილტროთ პროექტები სხვადასხვა პარამეტრებით'''
        # Parse the filter arguments
        args = filter_parser.parse_args()

        # Extract filter parameters
        proj_location = args.get("proj_location")
        contract_number = args.get("contract_number")
        vs30_min = args.get("vs30_min")
        vs30_max = args.get("vs30_max")
        pga_values = args.get("pga", [])

        # print("vs30_min:", vs30_min, "vs30_max:", vs30_max, "pga_values:", pga_values)

        start_time = None
        end_time = None

        if args.get('start_time'):
            try:
                start_time = datetime.strptime(args['start_time'], '%Y-%m-%d').date()
            except ValueError:
                return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ YYYY-MM-DD."}, 400

        if args.get('end_time'):
            try:
                end_time = datetime.strptime(args['end_time'], '%Y-%m-%d').date()
            except ValueError:
                return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ YYYY-MM-DD."}, 400

        # Build the base query for Projects
        project_query = Projects.query

        # Apply location filter if provided
        if proj_location:
            project_query = project_query.filter(Projects.proj_location.like(f"%{proj_location}%"))

        # Apply contract number filter if provided
        if contract_number:
            project_query = project_query.filter(Projects.contract_number.like(f"%{contract_number}%"))

        # Apply date range filter only if both start_time and end_time are provided
        if start_time and not end_time:
            project_query = project_query.filter(Projects.start_time >= start_time)
        elif end_time and not start_time:
            project_query = project_query.filter(Projects.end_time <= end_time)
        elif start_time and end_time:
            project_query = project_query.filter(
                and_(
                    Projects.start_time >= start_time,
                    Projects.end_time <= end_time
                )
            )

        # Join with the Geophysical table (left join to include projects without geophysical data)
        project_query = project_query.outerjoin(Geophysical, Geophysical.project_id == Projects.id)

        # Apply VS30 range filter if provided
        if vs30_min and vs30_max:
            project_query = project_query.filter(
                Geophysical.vs30.between(vs30_min, vs30_max)
            )
        elif vs30_min:
            project_query = project_query.filter(Geophysical.vs30 >= vs30_min)
        elif vs30_max:
            project_query = project_query.filter(Geophysical.vs30 <= vs30_max)

        # Get the filtered projects
        filtered_projects = project_query.all()

        # Add calculated fields to each project
        for project in filtered_projects:
            # Calculate dynamic fields
            project.geological_study = len(project.geological) > 0
            project.geophysical_study = len(project.geophysical) > 0
            # project.hazard_study = len(project.hazard) > 0
            # project.geodetic_study = len(project.geodetic) > 0
            # project.other_study = len(project.other) > 0
            project.hazard_study = False
            project.geodetic_study = False
            project.other_study = False

        # Return the filtered projects
        return filtered_projects, 200
