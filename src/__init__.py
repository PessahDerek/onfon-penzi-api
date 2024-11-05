from flask import Flask
from flask_graphql import GraphQLView
from .config import Config
from .extensions import db
from .schemas import schema

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register GraphQL view
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # Enable GraphiQL interface
        )
    )

    # Register blueprints
    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app