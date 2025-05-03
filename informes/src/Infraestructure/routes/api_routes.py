from flask import Blueprint
from informes.src.Infraestructure.routes.summary_routes import summary_blueprint
from informes.src.Infraestructure.routes.alerts_routes import alertas_blueprint
from informes.src.Infraestructure.routes.aplicaciones_routes import aplicaciones_blueprint
from informes.src.Infraestructure.routes.toptalkers_routes import toptalkers_blueprint
api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api_blueprint.register_blueprint(summary_blueprint)
api_blueprint.register_blueprint(alertas_blueprint)
api_blueprint.register_blueprint(aplicaciones_blueprint)
api_blueprint.register_blueprint(toptalkers_blueprint)