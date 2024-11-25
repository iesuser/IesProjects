from src.extensions import db
from src.models.base import BaseModel

class Geophysical(db.Model, BaseModel):
    __tablename__ = "geophysical"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), nullable=False)

    vs30 = db.Column(db.Integer, nullable=False)
    ground_category_geo = db.Column(db.String(255), nullable=False)
    ground_category_euro = db.Column(db.String(255), nullable=False)
    archival_excel = db.Column(db.String(255), nullable=True)
    archival_pdf = db.Column(db.String(255), nullable=True)

    project = db.relationship('Projects', back_populates='geophysical')
    geophysic_seismic = db.relationship('GeophysicSeismic', back_populates='geophysical', cascade='all, delete-orphan')
    geophysic_logging = db.relationship('GeophysicLogging', back_populates='geophysical', cascade='all, delete-orphan')
    geophysic_electrical = db.relationship('GeophysicElectrical', back_populates='geophysical', cascade='all, delete-orphan')
    geophysic_georadar = db.relationship('GeophysicGeoradar', back_populates='geophysical', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Geophysical {self.id}>'
    
class GeophysicSeismic(db.Model, BaseModel):
    __tablename__ = "geophysic_seismic"

    id = db.Column(db.Integer, primary_key=True)

    geophysical_id = db.Column(db.Integer, db.ForeignKey('geophysical.id', ondelete="CASCADE"), nullable=False)
    
    first_latitude = db.Column(db.Float, nullable=False)
    first_longitude = db.Column(db.Float, nullable=False)
    second_latitude = db.Column(db.Float, nullable=False)
    second_longitude = db.Column(db.Float, nullable=False)
    profile_length = db.Column(db.Float, nullable=False)
    vs30 = db.Column(db.Integer, nullable=False)
    ground_category_geo = db.Column(db.String(255), nullable=False)
    ground_category_euro = db.Column(db.String(255), nullable=False)
    archival_img = db.Column(db.String(255), nullable=True)
    archival_excel = db.Column(db.String(255), nullable=True)
    archival_pdf = db.Column(db.String(255), nullable=True)

    geophysical = db.relationship('Geophysical', back_populates='geophysic_seismic')

    def __repr__(self):
        return f'<Seismic Profile {self.id}>'
    
class GeophysicLogging(db.Model, BaseModel):
    __tablename__ = "geophysic_logging"

    id = db.Column(db.Integer, primary_key=True)

    geophysical_id = db.Column(db.Integer, db.ForeignKey('geophysical.id', ondelete="CASCADE"), nullable=False)

    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    profile_length = db.Column(db.Float, nullable=False)
    archival_img = db.Column(db.String(255), nullable=True)
    archival_excel = db.Column(db.String(255), nullable=True)
    archival_pdf = db.Column(db.String(255), nullable=True)

    geophysical = db.relationship('Geophysical', back_populates='geophysic_logging')

    def __repr__(self):
        return f'<Logging Profile {self.id}>'
    
class GeophysicElectrical(db.Model, BaseModel):
    __tablename__ = "geophysic_electrical"

    id = db.Column(db.Integer, primary_key=True)

    geophysical_id = db.Column(db.Integer, db.ForeignKey('geophysical.id', ondelete="CASCADE"), nullable=False)

    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    profile_length = db.Column(db.Float, nullable=False)
    archival_img = db.Column(db.String(255), nullable=True)
    archival_excel = db.Column(db.String(255), nullable=True)
    archival_pdf = db.Column(db.String(255), nullable=True)

    geophysical = db.relationship('Geophysical', back_populates='geophysic_electrical')

    def __repr__(self):
        return f'<Electrical Profile {self.id}>'
    

class GeophysicGeoradar(db.Model, BaseModel):
    __tablename__ = "geophysic_georadar"

    id = db.Column(db.Integer, primary_key=True)

    geophysical_id = db.Column(db.Integer, db.ForeignKey('geophysical.id', ondelete="CASCADE"), nullable=False)

    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    profile_length = db.Column(db.Float, nullable=False)
    archival_img = db.Column(db.String(255), nullable=True)
    archival_excel = db.Column(db.String(255), nullable=True)
    archival_pdf = db.Column(db.String(255), nullable=True)

    geophysical = db.relationship('Geophysical', back_populates='geophysic_georadar')

    def __repr__(self):
        return f'<Georadar Profile {self.id}>'
    
