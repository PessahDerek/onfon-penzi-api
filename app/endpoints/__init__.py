"""
Blueprint registration
"""
from flask import Flask
from .users import endpoints as user_ep
from .admins import endpoints as admin_ep


def register_blueprint(app: Flask):
    app.register_blueprint(user_ep.root, url_prefix='/api')
    app.register_blueprint(admin_ep.admin, url_prefix='/admin')
