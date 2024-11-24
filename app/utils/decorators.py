import json
from functools import wraps

import flask
from flask import g, Response, jsonify


def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        print("G: ",)
        if g.get('user') is None:
            res = Response(json.dumps({'message': 'You are not logged in'}), 401)
            return flask.abort(res)
        return func(*args, **kwargs)
    return decorated