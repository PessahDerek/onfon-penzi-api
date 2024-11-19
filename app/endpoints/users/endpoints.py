from flask import request, redirect, Blueprint, jsonify, make_response

from app.models import Message, User
from app.utils.methods import valid_number
from .methods import intro_message, create_account, save_details, save_description, handle_matching, handle_next, \
    request_user_data, request_description, follow_up_request_details
from app.extensions import db
from sqlalchemy.sql.operators import ilike_op

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
        found = db.session.query(User).filter_by(phone=phone).one_or_none()
        res = make_response(jsonify({"message": "hello world"}))
        res.set_cookie("phone", phone)
        res.set_cookie("user_id", str(found.id) if found else "")
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
        print("cookie: ", int(user_id))
        texts = db.session.query(Message).filter_by(user_id=int(user_id)).all()
        json_ready_list = [text.dict() for text in texts]
        print("text: ", json_ready_list)
        return jsonify(json_ready_list)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@root.route("/text", methods=["POST"])
def handle_text():
    try:
        active_user = db.session.query(User).filter_by(phone=request.cookies.get("phone")).one_or_none()
        text: str = request.get_json()["text"]
        # split based on #
        split_text = text.split("#")
        # first element is the prefix, if no element set None
        prefix: str | None = split_text[0].lower() if len(split_text) > 0 else None
        if prefix is None and text != "penzi":  # invalid message format
            return jsonify({"message": "Please provide a text!"}), 400
        # if prefix == "penzi":  # initiate chat
        #     return intro_message()r
        if prefix.startswith("start"):
            return create_account(text)
        if prefix.startswith("details"):
            return save_details(active_user, text)
        if prefix.startswith("myself"):
            return save_description(active_user, text)
        if prefix.startswith("match"):
            return handle_matching(active_user, text)
        if prefix.lower().startswith("next"):
            return handle_next(active_user, text)
        if valid_number(text)[0]:  # message is a valid phone number
            return request_user_data(active_user, text.strip())
        if prefix.lower().startswith('describe'):
            return request_description(active_user, text)
        if text.lower() == 'yes':
            return follow_up_request_details(active_user, text)
        return jsonify(text)
    except Exception as e:
        if type(e) == KeyError:
            print("Err: ", e)
            return jsonify({"message": "Please provide a text!"}), 400
        print(e)
        return jsonify({"message": "Something went wrong, please try again later"}), 500
