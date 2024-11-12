from flask import request, redirect, Blueprint, jsonify, make_response

from app.models import Message, User
from app.utils.methods import valid_number
from .methods import intro_message, create_account, save_details, save_description
from ..extensions import db

root = Blueprint('root', __name__)


# Entry route, redirects to fetch text if request is GET, else returns an error message
@root.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return redirect('./text')
    res = jsonify({"message": "We really shouldn't be doing this🌝. <br> Wrong api endpoint!"})
    return res


# api endpoint to start conversations, sets cookie
@root.route("/start", methods=["POST", "GET"])
def start_conversation():
    try:
        phone = request.get_json()["phone"]
        if not phone:
            return jsonify({"message": "Please provide a   number!"}), 400
        # check if phone is valid phone number
        valid, err = valid_number(phone)
        if not valid:
            return jsonify({"message": err}), 400
        res = make_response()
        res.set_cookie("phone", phone)
        res.set_cookie("user_id", "2")
        res.data = b"{'message': 'hello'}"
        return res
    except Exception as e:
        if type(e) == KeyError:
            print("err: ", e)
            res = jsonify({"message": "Phone number is required!"})
            res.status = 400
            return res
        print(e)
        res = jsonify({"message": "Sorry, something went wrong! Please try again!"})
        res.status = 500
        return res


@root.route("/text", methods=["GET"])
def get_texts():
    try:
        user_id = request.cookies.get("user_id")
        print("cookie: ",int(user_id))
        texts = db.session.query(Message).filter_by(user_id=int(user_id)).all()
        json_ready_list = [text.to_dict() for text in texts]
        print("text: ", json_ready_list)
        return jsonify(json_ready_list)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@root.route("/text", methods=["POST"])
def handle_text():
    try:
        active_user = db.session.query(User).filter_by(phone=request.cookies.get("phone")).one_or_none()
        text = request.get_json()["text"]
        # split based on #
        split_text = text.split("#")
        # first element is the prefix, if no element set None
        prefix: str | None = split_text[0].lower() if len(split_text) > 0 else None
        if prefix is None and text != "penzi":  # invalid message format
            print(split_text)
            return jsonify({"message": "Please provide a text!"}), 400
        # if prefix == "penzi":  # initiate chat
        #     return intro_message()r
        if prefix.startswith("start"):
            return create_account(text)
        if prefix.startswith("details"):
            return save_details(active_user, text)
        if prefix.startswith("myself"):
            return save_description(active_user, text)

        return jsonify(text)
    except Exception as e:
        if type(e) == KeyError:
            print("Err: ", e)
            return jsonify({"message": "Please provide a text!"}), 400
        print(e)
        return jsonify({"message": "Something went wrong, please try again later"}), 500
