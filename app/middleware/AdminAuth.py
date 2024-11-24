from flask import Request, g
from ..extensions import db
from app import create_app
from app.utils.methods import decode_token
from ..models.admin_model import Admin


class AdminAuth:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        with create_app().app_context():
            this_request = Request(environ)
            token = this_request.headers.get('Authorization')
            print("Token is: ", token)
            token_d = decode_token(token.replace("Bearer ", "")) if token else None
            found = db.session.query(Admin).filter(Admin.id==token_d['id']).one_or_none() if token_d else None
            g.setdefault('user', found.dict() if found else None)
            print("User is: ", g.user)
        print("Pers: ", g.get("user"))
        return self.app(environ, start_response)
