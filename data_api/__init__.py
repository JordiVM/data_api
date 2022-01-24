from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from data_api.data import data_bp

# Create instance for flask SQL extension, not yet attached to application
db = SQLAlchemy()


# Flask application factory
def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprint(app)
    return app


def initialize_extensions(app):
    # Bind extensions to the Flask application instance (app)
    db.init_app(app)


def register_blueprint(app):
    app.register_blueprint(data_bp)
