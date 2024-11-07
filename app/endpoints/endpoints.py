"""
All endpoints are written here.
"""
from flask import request, redirect, Response, Blueprint

root = Blueprint('root', __name__)


@root.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return redirect('./text')
    res = Response()
    res.data = {"message": "We really shouldn't be doing this🌝"}
    return res
