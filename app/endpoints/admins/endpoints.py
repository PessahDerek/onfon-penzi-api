from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required

from app.endpoints.admins.methods import seed_admin
from app.extensions import db, bcrypt
from app.models import User
from app.models.admin_model import Admin

admin = Blueprint('admin', __name__)


@admin.route('/login', methods=['POST'])
def login():
    def successful(admin_user: Admin):
        jwt_token = create_access_token(identity=str(admin_user.id))

        return jsonify({
            "message": f"Welcome back {admin_user.username}",
            "username": admin_user.username,
            "token": jwt_token
        })

    try:
        username, password = request.get_json().values()
        # check if user is in database
        found = db.session.query(Admin).filter(Admin.username == username).one_or_none()
        if found is None:  # not found
            # check if there is any admin
            admin_count = db.session.query(Admin).count()
            if admin_count > 0:  # if there is an existing admin refuse attempt
                return jsonify({"message": "Wrong password or username!"})
            # create first admin
            new_admin = seed_admin(username, password)
            return successful(new_admin)
        # compare password
        if bcrypt.check_password_hash(found.password, password):
            return successful(found)
        return jsonify({"message": "Wrong password or username!"}), 401
    except Exception as e:
        print("Error signing in: ", e)
        if type(e) == KeyError:
            return jsonify({"message": "All fields are required!"}), 400
        return jsonify({"message": "Sorry something went wrong please try again!"}), 500


@admin.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = db.session.query(User).all()
        serialized = [x.dict() for x in users if x.id != 1]
        return jsonify(serialized)
    except Exception as e:
        print("Error getting users: ", e)
        return jsonify({"message": "Something went wrong please try again!"}), 500
