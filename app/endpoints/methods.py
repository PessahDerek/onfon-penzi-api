from flask import jsonify, make_response, request

from ..extensions import db
from ..models import User, Details, Message, Gender


def get_system_obj():
    found = db.session.query(User).get(1)
    return found if found else None


def save_message(user: User, message: str, user_id: int):
    try:
        print("x->", user, "\n", user_id)
        new_message = Message()
        new_message.message = message
        new_message.msg_type = "incoming" if user.id != 1 else "outgoing"
        new_message.user_id = user_id
        new_message.phone = user.phone
        db.session.add(new_message)
    except Exception as e:
        print("Error saving message: ", e)
        raise Exception(e)


def intro_message() -> [str]:
    try:
        default_msg = "Welcome to our dating service with 6000 potential dating partners! To register SMS start#name#age#gender#county#town to 22141.E.g., start#John Doe#26#Male#Nakuru#Naivasha"
        # save user message
        # save system msg
        # save_message(get_system_obj(), phone)
    except Exception as e:
        raise Exception(e)
    # return "Welcome to our dating service with 6000 potential dating partners! To register SMS start#name#age#gender#county#town to 22141.E.g., start#John Doe#26#Male#Nakuru#Naivasha"


def create_account(text: str) -> [str]:
    try:
        _prefix, name, age, gender, county, town = text.split("#")
        # check for duplicates;
        found = db.session.query(User).filter_by(phone=request.cookies.get("phone")).one_or_none()
        if found is not None:
            res = make_response(jsonify({"message": "Account already exists"}))
            res.set_cookie("user_id", str(found.id))
            res.status_code = 400
            return res
        gender = gender.lower()
        new_user = User()
        new_user.name = name
        new_user.phone = request.cookies.get("phone")
        new_user.age = age  # int(age) if type(age) == str else age
        new_user.gender = Gender.MALE if gender == "male" else Gender.FEMALE
        new_user.county = county
        new_user.town = town
        db.session.add(new_user)
        db.session.commit()
        default_msg = "Your profile has been created successfully Jamal. SMS details#levelOfEducation#profession#maritalStatus#religion#ethnicity to 22141. E.g. details#diploma#driver#single#christian#mijikenda"

        # Save user message
        print("new: ", new_user.id)
        save_message(new_user, text, new_user.id)
        # save system message
        print("heh", new_user.id)
        save_message(get_system_obj(), default_msg, new_user.id)
        res = make_response(jsonify({"message": "Message sent"}))
        res.set_cookie("phone", new_user.phone)
        res.set_cookie("user_id", str(new_user.id))
        db.session.commit()
        return res
        # return , 200
    except Exception as e:
        print("E is: ", e)
        raise Exception(e)


def save_details(user_obj: User, text: str) -> [str]:
    try:
        text_arr = text.split("#")
        if len(text_arr) == 7:
            default_msg = "This is the last stage of registration. SMS a brief description of yourself to 22141 starting with the word MYSELF. E.g., MYSELF chocolate, lovely, sexy etc."
            _details, education, profession, marital_status, religion, ethnicity = text.split("#")
            add_details = Details()
            add_details.user_id = user_obj.id
            add_details.education = education
            add_details.profession = profession
            add_details.marital_status = marital_status
            add_details.religion = religion
            add_details.ethnicity = ethnicity
            db.session.add(add_details)
            user_obj.details = add_details.id
            db.session.commit()

            # save user message
            save_message(user_obj, text, user_obj.id)
            # save system message
            save_message(get_system_obj(), default_msg, user_obj.id)
            return jsonify({"message": "Message sent"}), 200
        else:  # details not provided
            default_msg = "You were registered for dating with your initial details. To search for a MPENZI, SMS match#age#town to 22141 and meet the person of your dreams. E.g., match#23-25#Nairobi"
            save_message(user_obj, text, user_obj.id)
            save_message(get_system_obj(), default_msg, user_obj.id)
            return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        raise Exception(e)


def save_description(user_obj: User, text: str) -> [str]:
    try:
        detail_obj = db.session.query(Details).filter_by(user_id=user_obj.id).one_or_none()
        if detail_obj is None:
            return ["Sorry we could not find your account! Please register first!"]
        description = text.split("#")[1]
        detail_obj.description = description
        db.session.flush(description)

        default_msg = "You are now registered for dating. To search for a MPENZI, SMS match#age#town to 22141 and meet the person of your dreams. E.g., match#23-25#Kisumu"
        save_message(user_obj, text)
        save_message(get_system_obj(), default_msg)
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        raise Exception(e)
