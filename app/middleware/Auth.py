import json
from flask import g
from werkzeug import Response
from werkzeug.wrappers import Request

class AuthMiddleware:
    """
    Checks to ensure the user is identified using their phone number
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        phone = request.cookies.get('phone')  # if request.cookies.get('phone') else request.headers.get("Set-Cookie")

        if request.path.replace("/", "").endswith("start"):
            return self.app(environ, start_response)
        if not phone:
            response = Response(
                json.dumps({"message": "Please restart conversation!"}),
                status=401,
                mimetype='application/json'
            )
            return response(environ, start_response)
        environ['phone'] = phone
        return self.app(environ, start_response)
