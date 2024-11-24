"""
initialize the Flask application, configure it, and register any blueprints or extensions.
"""
from flask import Flask

from .config import Config
from .endpoints import register_blueprint
from .extensions import db, bcrypt
from .middleware.Auth import AuthMiddleware


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    # CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    # register blueprints
    register_blueprint(app)

    with app.app_context():
        db.create_all()

    return app
