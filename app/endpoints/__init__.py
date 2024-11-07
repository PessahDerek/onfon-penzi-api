"""
Blueprint registration
"""
from flask import Flask
from . import endpoints

def register_blueprint(app: Flask):
    app.register_blueprint(endpoints.root, url_prefix='/api')
