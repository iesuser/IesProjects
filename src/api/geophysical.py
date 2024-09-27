from flask_restx import Resource
from werkzeug.exceptions import NotFound
import os
import uuid
import shutil
from flask_jwt_extended import jwt_required, current_user

from src.api.nsmodels import geophysical_ns, geophysical_model, geophysical_parser
from src.models import Geophysical
from src.config import Config
from src.utils.utils import save_uploaded_file


@geophysical_ns.route('/geophysical/<int:proj_id>')
@geophysical_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class GeophysicalListAPI(Resource):

    @geophysical_ns.marshal_with(geophysical_model)
    def get(self, proj_id):
        geophysical_records = Geophysical.query.filter_by(project_id=proj_id).all()
        if not geophysical_records:
            return {"error": "გეოფიზიკა არ მოიძებნა."}, 404

        # Add calculated fields to each geophysical record
        for geophysical in geophysical_records:
            # Calculate dynamic fields
            geophysical.seismic_profiles = len(geophysical.geophysic_seismic) > 0
            geophysical.profiles_number = len(geophysical.geophysic_seismic)
            geophysical.geophysical_logging = len(geophysical.geophysic_logging) > 0
            geophysical.logging_number = len(geophysical.geophysic_logging)
            geophysical.electrical_profiles = len(geophysical.geophysic_electrical) > 0
            geophysical.point_number = len(geophysical.geophysic_electrical)
            geophysical.georadar = len(geophysical.geophysic_georadar) > 0
        
        return geophysical_records, 200
    
    @jwt_required()
    @geophysical_ns.doc(parser=geophysical_parser)
    @geophysical_ns.doc(security = 'JsonWebToken')
    def post(self, proj_id):

        if not current_user.check_permission('can_geophysic'):
            return {"error": "არ გაქვს გეოფიზიკის დამატების ნებართვა."}, 403
        
        # Parse the incoming request data
        args = geophysical_parser.parse_args()

        # Extract files from the request
        pdf_files = args.get('archival_pdf', [])
        excel_files = args.get('archival_excel', [])

        # Initialize filenames
        pdf_filename = None
        excel_filename = None
        server_message = "წარმატებით დაემატა გეოფიზიკა."

        # Handle the PDF file upload
        if pdf_files:
            pdf_filename = save_uploaded_file(
                pdf_files[0],
                os.path.join(Config.UPLOAD_FOLDER, str(proj_id), 'geophysical', 'archival_pdf'),
                ['application/pdf'],
                '.pdf'
            )
            if not pdf_filename:
                server_message += ' არ აიტვირთა საარქივო PDF-ის ფაილი.'

        # Handle the Excel file upload
        if excel_files:
            excel_filename = save_uploaded_file(
                excel_files[0],
                os.path.join(Config.UPLOAD_FOLDER, str(proj_id), 'geophysical', 'archival_excel'),
                ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'],
                '.xlsx'
            )
            if not excel_filename:
                server_message += ' არ აიტვირთა საარქივო Excel-ის ფაილი.'

        # Create the Geophysical record
        new_geophysical = Geophysical(
            project_id=proj_id,
            vs30=args['vs30'],
            ground_category_geo=args['ground_category_geo'],
            ground_category_euro=args['ground_category_euro'],
            archival_pdf=pdf_filename,
            archival_excel=excel_filename
        )
        new_geophysical.create()

        return {"message": server_message}, 200

@geophysical_ns.route('/geophysical/<int:proj_id>/<int:id>')
@geophysical_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class GeophysicalAPI(Resource):
    @geophysical_ns.marshal_with(geophysical_model)
    def get(self, proj_id, id):
        # Query the Geophysical record with the specified project_id and id
        geophysical = Geophysical.query.filter_by(project_id=proj_id, id=id).first()
        if not geophysical:
            return {"error": "გეოფიზიკა არ მოიძებნა."}, 404
        
        # Calculate dynamic fields
        geophysical.seismic_profiles = len(geophysical.geophysic_seismic) > 0
        geophysical.profiles_number = len(geophysical.geophysic_seismic)
        geophysical.geophysical_logging = len(geophysical.geophysic_logging) > 0
        geophysical.logging_number = len(geophysical.geophysic_logging)
        geophysical.electrical_profiles = len(geophysical.geophysic_electrical) > 0
        geophysical.point_number = len(geophysical.geophysic_electrical)
        geophysical.georadar = len(geophysical.geophysic_georadar) > 0
        
        return geophysical, 200
    
    @jwt_required()
    @geophysical_ns.doc(parser=geophysical_parser)
    @geophysical_ns.doc(security = 'JsonWebToken')
    def put(self, proj_id, id):
                
        if not current_user.check_permission('can_geophysic'):
            return {"error": "არ გაქვს გეოფიზიკის რედაქტირების ნებართვა."}, 403
        

        # Find the existing geophysical record
        geophysical = Geophysical.query.filter_by(project_id=proj_id, id=id).first()
        if not geophysical:
            return {"error": "გეოფიზიკა არ მოიძებნა."}, 404

        # Parse the incoming request data
        args = geophysical_parser.parse_args()

        # Extract files from the request
        pdf_files = args.get('archival_pdf', [])
        excel_files = args.get('archival_excel', [])

        # Initialize filenames
        pdf_filename = geophysical.archival_pdf
        excel_filename = geophysical.archival_excel
        server_message = "წარმატებით განახლდა გეოფიზიკა."

        # Handle the PDF file upload
        if pdf_files:
            upload_folder = os.path.join(Config.UPLOAD_FOLDER, str(proj_id), 'geophysical', 'archival_pdf')
            pdf_filename = save_uploaded_file(
                pdf_files[0],
                upload_folder,
                ['application/pdf'],
                '.pdf'
            )
            if pdf_filename:
                # If there's an existing archival_pdf, delete it
                if geophysical.archival_pdf:
                    old_file_path = os.path.join(upload_folder, geophysical.archival_pdf)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                geophysical.archival_pdf = pdf_filename
            else:
                server_message += ' არ აიტვირთა საარქივო PDF-ის ფაილი.'
            

        # Handle the Excel file upload
        if excel_files:
            upload_folder = os.path.join(Config.UPLOAD_FOLDER, str(proj_id), 'geophysical', 'archival_excel')
            excel_filename = save_uploaded_file(
                excel_files[0],
                upload_folder,
                ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'],
                '.xlsx'
            )
            if excel_filename:
                # If there's an existing archival_excel , delete it
                if geophysical.archival_excel:
                    old_file_path = os.path.join(upload_folder, geophysical.archival_excel)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                geophysical.archival_excel = excel_filename    
            else:
                server_message += ' არ აიტვირთა საარქივო Excel-ის ფაილი.'

        # Update other fields
        geophysical.vs30 = args['vs30']
        geophysical.ground_category_geo = args['ground_category_geo']
        geophysical.ground_category_euro = args['ground_category_euro']

        # Save the changes
        geophysical.save()

        return {"message": server_message}, 200
    
    @jwt_required()
    @geophysical_ns.doc(security = 'JsonWebToken')
    def delete(self, proj_id, id):
                        
        if not current_user.check_permission('can_geophysic'):
            return {"error": "არ გაქვს გეოფიზიკის წაშლის ნებართვა."}, 403
        
        # Fetch the geophysical record
        geophysical = Geophysical.query.filter_by(project_id=proj_id, id=id).first()
        if not geophysical:
            return {"error": "გეოფიზიკა არ მოიძებნა."}, 404

        # Delete the associated PDF file if it exists
        if geophysical.archival_pdf or geophysical.archival_excel:
            geophysical_directory = os.path.join(Config.UPLOAD_FOLDER, str(proj_id), 'geophysical')

            # Delete the entire project directory if it exists
            if os.path.isdir(geophysical_directory):
                shutil.rmtree(geophysical_directory)

        # Delete the geophysical record
        geophysical.delete()

        return {"message": "წარმატებით წაიშალა გეოფიზიკა"}, 200