from flask_restx import Resource

from src.api.nsmodels import geological_ns, geological_model
from src.models import Geological


@geological_ns.route('/geological/<int:proj_id>')
@geological_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class GeologicalAPI(Resource):

    @geological_ns.marshal_with(geological_model)
    def get(self, proj_id):
        geological = Geological.query.filter_by(project_id=proj_id).all()
        if not geological:
            return {"error": "გეოლოგია არ მოიძებნა."}, 404
        
        return geological, 200
