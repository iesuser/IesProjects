from flask_restx import Resource
from datetime import datetime
import os
import uuid
import shutil
import mimetypes
from flask_jwt_extended import jwt_required, current_user

from src.api.nsmodels import projects_ns, projects_model, projects_parser, projects_img_model, project_img_parser
from src.models import Projects, Images
from src.config import Config


@projects_ns.route('/projects')
@projects_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class ProjectsListAPI(Resource):

    @projects_ns.marshal_with(projects_model)
    def get(self):
        projects = Projects.query.all()

        if not projects:
            return {"error": "პროექტები არ მოიძებნა."}, 404

        # Add calculated fields to each project
        for project in projects:
            # Calculate dynamic fields
            project.geological_study = len(project.geological) > 0
            project.geophysical_study = len(project.geophysical) > 0
            # project.hazard_study = len(project.hazard) > 0
            # project.geodetic_study = len(project.geodetic) > 0
            # project.other_study = len(project.other) > 0
            project.hazard_study = False
            project.geodetic_study = False
            project.other_study = False

        return projects, 200
    
    @jwt_required()
    @projects_ns.doc(parser=projects_parser)
    @projects_ns.doc(security = 'JsonWebToken')
    def post(self):
                
        if not current_user.check_permission('can_project'):
            return {"error": "არ გაქვს პროექტის დამატების ნებართვა."}, 403
        
        args = projects_parser.parse_args()
        
        try:
            start_time = datetime.strptime(args['start_time'], '%Y-%m-%d').date()
            end_time = datetime.strptime(args['end_time'], '%Y-%m-%d').date()
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ YYYY-MM-DD."}, 400

        new_project = Projects(
            projects_name=args['projects_name'],
            contract_number=args['contract_number'],
            start_time=start_time,
            end_time=end_time,
            contractor=args['contractor'],
            proj_location=args['proj_location'],
            proj_latitude=args['proj_latitude'],
            proj_longitude=args['proj_longitude']
        )
        new_project.create()

        # Handle image uploads if provided
        image_types = ["image/jpeg", "image/png", "image/jpg"]
        images = args['images']

        invalid_files = []
        images_saved = False
        images_directory = os.path.join(Config.UPLOAD_FOLDER, str(new_project.id), 'images')

        if images:
            for image in images:
                if image.mimetype not in image_types:
                    invalid_files.append(image.filename)
                    continue

                if not images_saved:
                    os.makedirs(images_directory, exist_ok=True)
                    images_saved = True
                
                extension = mimetypes.guess_extension(image.mimetype) or ".jpg"
                file_name = str(uuid.uuid4()).replace('-', '')[:12] + extension
                image_path = os.path.join(images_directory, file_name)
                
                try:
                    # Save the file to the directory
                    image.save(image_path)
                    
                    # Save the file path to the database
                    new_image = Images(path=file_name, project_id=new_project.id)
                    new_image.create()
                except:
                    return {"error": "სურათის ვერ შეინახა"}, 400
        else:
            invalid_files.append("empty")
            
        if invalid_files:
            return {"message": "პროექტი შეიქმნა, მაგრამ პროექტის სურათი არ აიტვირთა"}, 200
        
        return {"message": "პროექტი წარმატებით შეიქმნა."}, 200
    
@projects_ns.route('/project/<int:id>')
@projects_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class ProjectAPI(Resource):

    @projects_ns.marshal_with(projects_model)
    def get(self, id):
        project = Projects.query.get(id)
        if not project:
            return {"error": "პროექტი არ მოიძებნა."}, 404
        
        images = Images.query.filter_by(project_id=id).all()
        project.images = images

        # Calculate dynamic fields
        project.geological_study = len(project.geological) > 0
        project.geophysical_study = len(project.geophysical) > 0
        # project.hazard_study = len(project.hazard) > 0
        # project.geodetic_study = len(project.geodetic) > 0
        # project.other_study = len(project.other) > 0
        project.hazard_study = False
        project.geodetic_study = False
        project.other_study = False

        return project, 200
    
    @jwt_required()
    @projects_ns.doc(parser=projects_parser)
    @projects_ns.doc(security = 'JsonWebToken')
    def put(self, id):

        if not current_user.check_permission('can_project'):
            return {"error": "არ გაქვს პროექტის რედაქტირების ნებართვა."}, 403

        args = projects_parser.parse_args()
        try:
            start_time = datetime.strptime(args['start_time'], '%Y-%m-%d').date()
            end_time = datetime.strptime(args['end_time'], '%Y-%m-%d').date()
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ YYYY-MM-DD."}, 400

        project = Projects.query.get(id)
        if project:
            project.projects_name = args["projects_name"]
            project.contract_number = args["contract_number"]
            project.start_time = start_time
            project.end_time = end_time
            project.contractor=args['contractor']
            project.proj_location = args["proj_location"]
            project.proj_latitude = args["proj_latitude"]
            project.proj_longitude = args["proj_longitude"]
            project.save()  
            return {"message": "პროექტი წარმატებით განახლდა."}, 200
        else:
            return {"error":"პროექტი არ მოიძებნა."}, 404

    @jwt_required()
    @projects_ns.doc(security = 'JsonWebToken')
    def delete(self, id):

        if not current_user.check_permission('is_admin'):
            return {"error": "არ გაქვს პროექტის წაშლის ნებართვა."}, 403
        
        project = Projects.query.get(id)
        if project:
            try:
                # Path to the entire project directory
                project_directory = os.path.join(Config.UPLOAD_FOLDER, str(id))

                # Delete the entire project directory if it exists
                if os.path.isdir(project_directory):
                    shutil.rmtree(project_directory)

                # Delete the project record from the database
                project.delete()
                return {"message": "წარმატებით წაიშალა პროექტი, ყველა მიბმული ფაილით."}, 200

            except OSError as e:
                return {"error": f"ვერ წაიშალა პროექტის, ყველა მიბმული ფაილი: {str(e)}"}, 400
        else:
            return {"error": "პროექტი არ მოიძებნა"}, 404
        
@projects_ns.route('/project/<int:proj_id>/images')
@projects_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class ProjectImageListAPI(Resource):

    @projects_ns.marshal_with(projects_img_model)
    def get(self, proj_id):

        # Fetch images associated with the project
        images = Images.query.filter_by(project_id=proj_id).all()
        if not images:
            return {"error": "სურათი არ მოიძებნა ამ პროექტისთვის"}, 404
        
        return images, 200

    @jwt_required()
    @projects_ns.doc(parser=project_img_parser)
    @projects_ns.doc(security = 'JsonWebToken')
    def post(self, proj_id):

        if not current_user.check_permission('can_project'):
            return {"error": "არ გაქვს სურათის ატვირთვის ნებართვა."}, 403
        
        # Ensure the project exists
        project = Projects.query.get(proj_id)
        if not project:
            return {"error": "პროექტი არ მოიძებნა."}, 404

        # Parse arguments
        args = project_img_parser.parse_args()
        images = args['images']
        if not images:
            return {"error": "სურათი არ არის მოინიშნა"}, 400
        
        # Validate image type and size (if needed)
        image_types = ["image/jpeg", "image/png", "image/jpg"]
        max_image_size = 5 * 1024 * 1024  # 5MB limit (example)

        images_directory = os.path.join(Config.UPLOAD_FOLDER,  str(proj_id), 'images')
        os.makedirs(images_directory, exist_ok=True)

        saved_images = []

        try:
            for image in images:
                if image.mimetype not in image_types:
                    return {"error": "ფაილი არ არის სურათის ტიპის (jpeg/png/jpg)."}, 400

                if image.content_length > max_image_size:
                    return {"error": "სურათის ზომა აჭარბებს ლიმიტს: 5MB limit."}, 400

                # Save each image
                extension = mimetypes.guess_extension(image.mimetype) or ".jpg"
                file_name = str(uuid.uuid4()).replace('-', '')[:12] + extension
                image_path = os.path.join(images_directory, file_name)
                image.save(image_path)

                # Save image record in the database
                new_image = Images(path=file_name, project_id=proj_id)
                new_image.create()
                saved_images.append({
                    'id': new_image.id,
                    'path': new_image.path
                })

            return {"message": "სურათი წარმატებით აიტვირთა."}, 200
        
        except OSError as e:
            return {"error": f"სურათები ვერ შეინახა: {str(e)}"}, 400


@projects_ns.route('/project/<int:proj_id>/images/<int:image_id>')
@projects_ns.doc(security = 'JsonWebToken')
class ProjectImageAPI(Resource):

    @jwt_required()
    def delete(self, proj_id, image_id):

        if not current_user.check_permission('can_project'):
            return {"error": "არ გაქვს სურათის წაშლის ნებართვა."}, 403
        
        # Find the image record
        image = Images.query.filter_by(id=image_id, project_id=proj_id).first()
        if not image:
            return {"error": "სურათი არ მოიძებნა."}, 404

        # Path to the image file
        images_directory = os.path.join(Config.UPLOAD_FOLDER, str(proj_id), 'images')
        image_path = os.path.join(images_directory, image.path)
        
        try:
            # Delete the image file from the filesystem
            if os.path.isfile(image_path):
                os.remove(image_path)
            
            # Delete the image record from the database
            image.delete()

            # Optionally, delete the directory if it's empty
            if os.path.isdir(images_directory) and not os.listdir(images_directory):
                os.rmdir(images_directory)
                
            return {"message": "წარმატებით წაიშალა სურათი."}, 200
        
        except OSError as e:
            return {"message": f"სურათი ვერ შეინახა: {str(e)}"}, 400


