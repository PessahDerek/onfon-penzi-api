import json

import flask
from flask import jsonify, request, Response
from flask_cors import CORS

from app import create_app
from app.middleware.AdminAuth import AdminAuth
from app.models.admin_model import Admin
from app.utils.methods import decode_token
from app.extensions import db

app = create_app()

# app.wsgi_app = AdminAuth(app.wsgi_app)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# app.wsgi_app = AuthMiddleware(app.wsgi_app)
@app.route('/')
def index():
    return jsonify({'message': 'Hello World'})

@app.before_request
def before_request():
    token = flask.request.headers.get("Authorization")
    if token:
        decoded = decode_token(token.replace("Bearer ", ""))
        print("Req: ", flask.request.headers)
        if decoded is None:
            flask.g.setdefault('user', None)
        else:
            found = db.session.query(Admin).filter(Admin.id==decoded.get('id')).one_or_none()
            flask.g.user = found
    else:
        flask.g.user = None



if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
