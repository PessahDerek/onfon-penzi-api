"""
initialize the Flask application, configure it, and register any blueprints or extensions.
"""
from flask import Flask
from flask_cors import CORS

from .config import Config
from .endpoints import register_blueprint
from .extensions import db, bcrypt, jwt
from .middleware.Auth import AuthMiddleware


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3001"}})
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    # register blueprints
    register_blueprint(app)
    jwt.init_app(app)


    with app.app_context():
        db.create_all()

    return app
