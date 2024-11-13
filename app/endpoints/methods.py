from flask import jsonify, make_response, request

from ..extensions import db
from ..models import User, Details, Message, Gender, MatchTable, PairTable, SentMatched


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
        return new_message
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
    print("Creating account...")
    try:
        _prefix, name, age, gender, county, town = text.lower().split("#")
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
        if len(text_arr) == 6:
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
            # user_obj.details = add_details.id

            db.session.commit()

            # save user message
            save_message(user_obj, text, user_obj.id)
            # save system message
            save_message(get_system_obj(), default_msg, user_obj.id)
            db.session.commit()
            return jsonify({"message": "Message sent"}), 200
        else:  # details not provided
            default_msg = "You were registered for dating with your initial details. To search for a MPENZI, SMS match#age#town to 22141 and meet the person of your dreams. E.g., match#23-25#Nairobi"
            save_message(user_obj, text, user_obj.id)
            save_message(get_system_obj(), default_msg, user_obj.id)
            db.session.commit()
            return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        raise Exception(e)


def save_description(user_obj: User, text: str) -> [str]:
    try:
        detail_obj = db.session.query(Details).filter_by(user_id=user_obj.id).one_or_none()
        if detail_obj is None:
            return ["Sorry we could not find your account! Please register first!"]
        description = text.lower().replace("myself", "").strip()
        print("Desc: ", description)
        detail_obj.description = description
        db.session.add(detail_obj)

        default_msg = "You are now registered for dating. To search for a MPENZI, SMS match#age#town to 22141 and meet the person of your dreams. E.g., match#23-25#Kisumu"
        save_message(user_obj, text, user_obj.id)
        save_message(get_system_obj(), default_msg, user_obj.id)
        db.session.commit()
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        raise Exception(e)


def handle_matching(user: User, text: str):
    try:
        _prefix, age, town = text.split("#")
        age_range = [int(age.split("-")[0]), int(age.split("-")[1])] if (age.find("-") > -1) else [int(age),
                                                                                                   int(age)]
        age_range.sort()
        found = db.session.query(User).filter(
            User.age >= age_range[0],
            User.age <= age_range[1],
            User.town == town.lower(),
            User.gender != user.gender
        ).all()
        # return jsonify(serialized)
        # commit message
        saved = save_message(user, text, user.id)
        save_message(get_system_obj(),
                     f"We have {len(found)} {'ladies' if user.gender.name == 'MALE' else 'men'} who match your choice! We will send you details of 3 of them shortly. To get more details about a lady, SMS her number e.g., 0722010203 to 22141",
                     user.id)
        # commit 3 matches
        sent = []
        send_msg = ""
        for person in found[:3]:
            send_msg += f"{person.name} aged {person.age} {person.phone}.\n"
            sent.append(person)
        send_msg += f"Send NEXT to 22141 to receive details of the remaining {len(found) - len(sent)} {'ladies' if user.gender.name == 'MALE' else 'men'}"
        save_message(get_system_obj(), send_msg, user.id)
        # create new match
        match = MatchTable()
        match.sender_id = user.id
        match.message_id = saved.id
        matches_list = []
        for person in found:
            pair = PairTable()
            pair.user1_id = user.id
            pair.user2_id = person.id
            pair.match_table_id = match.id
            matches_list.append(pair)
        match.matches = matches_list
        sent_list = []
        for person in sent:
            new_sent = SentMatched()
            new_sent.match_table_id = match.id
            new_sent.user_id = user.id
            sent_list.append(new_sent)
        match.sent = sent_list
        db.session.add(match)
        db.session.commit()
        # send message
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        print("Error matching: ", e)
        raise Exception(e)
