from flask import Flask
from informes.src.Infraestructure.config import DevelopmentConfig
from informes.src.Infraestructure.routes.api_routes import api_blueprint
from flask_cors import CORS
import os

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/*": {"origins": "*"}})

    if not os.path.exists('temp'):
        os.makedirs('temp')

    app.register_blueprint(api_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)