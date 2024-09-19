from src.api.nsmodels.projects import projects_ns, projects_model, projects_parser, projects_img_model, project_img_parser
from src.api.nsmodels.geological import geological_ns, geological_model
from src.api.nsmodels.geophysical import geophysical_ns, geophysical_model, geophysical_parser
from src.api.nsmodels.geophysic_details import  geophysic_seismic_ns, geophysic_seismic_model, geophysical_seismic__parser
from src.api.nsmodels.geophysic_details import geophysic_logging_ns, geophysic_logging_model, geophysic_logging_parser
from src.api.nsmodels.geophysic_details import geophysic_electrical_ns, geophysic_electrical_model, geophysic_electrical_parser
from src.api.nsmodels.geophysic_details import geophysic_georadar_ns, geophysic_georadar_model, geophysic_georadar_parser
from src.api.nsmodels.authentication import auth_ns, registration_parser, auth_parser, user_model, user_parser
from src.api.nsmodels.filters import filter_ns, filter_parser, filter_model