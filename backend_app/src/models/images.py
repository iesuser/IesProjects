from src.extensions import db
from src.models.base import BaseModel

class Images(db.Model, BaseModel):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=False)
    
    project = db.relationship('Projects', back_populates='images')

    def __repr__(self):
        return f'<Image {self.id} {self.path}>'