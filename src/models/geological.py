from src.extensions import db
from src.models.base import BaseModel

class Geological(db.Model, BaseModel):
    __tablename__ = "geological"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=False)
    
    geological_survey = db.Column(db.Boolean, nullable=False)
    objects_number = db.Column(db.Integer, nullable=False)
    boreholes = db.Column(db.Boolean, nullable=False)
    boreholes_number = db.Column(db.Integer, nullable=False)
    pits = db.Column(db.Boolean, nullable=False)
    pits_number = db.Column(db.Integer, nullable=False)
    laboratory_tests = db.Column(db.Boolean, nullable=False)
    points_number = db.Column(db.Integer, nullable=False)
    archival_material = db.Column(db.String(255), nullable=False)

    project = db.relationship('Projects', back_populates='geological')

    def __repr__(self):
        return f'<Geological {self.id}>'