from flask import jsonify, make_response, request

from app.extensions import db
from app.models import User, Details, Message, Gender, MatchTable, PairTable, SentMatched
from app.utils.methods import retrieve_text_between


def get_system_obj():
    found = db.session.query(User).get(1)
    return found if found else None

def descriptive_message_template(found: User):
    details = found.dict()['details']
    return f"{found.name} aged {found.age}, {found.county} County, {found.town} town, {details['education']}, {details['profession']}, {details['marital_status']}, {details['religion']}, {details['ethnicity']}. Send DESCRIBE {found.phone} to get more details about {found.name.split(' ')[0]}."


def save_message(user: User, message: str, user_id: int):
    try:
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
        # sort to fit so that its low-high
        age_range.sort()
        # filter those who fit the criteria
        found = db.session.query(User).filter(
            User.age >= age_range[0],
            User.age <= age_range[1],
            User.town == town.lower(),
            User.gender != user.gender
        ).all()
        # return jsonify(serialized)
        # commit message bearing the request criteria
        saved = save_message(user, text, user.id)
        # commit message with the result analysis
        save_message(get_system_obj(),
                     f"We have {len(found)} {'ladies' if user.gender.name == 'MALE' else 'men'} who match your choice! We will send you details of 3 of them shortly. To get more details about a lady, SMS her number e.g., 0722010203 to 22141",
                     user.id)
        # commit 3 matches to send in the follow-up text
        sent = []
        send_msg = ""
        for person in found[:3]:
            send_msg += f"{person.name} aged {person.age} {person.phone}.\n"
            sent.append(person)
        send_msg += f"Send NEXT to 22141 to receive details of the remaining {len(found) - len(sent)} {'ladies' if user.gender.name == 'MALE' else 'men'}"
        # commit follow-up message
        save_message(get_system_obj(), send_msg, user.id)
        # create new match table with the records
        match = MatchTable()
        match.sender_id = user.id
        match.message_id = saved.id

        # contain list of all the pairs
        matches_list = []
        for person in found:  # iterate through the found list to add to the matching pair
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
            new_sent.user_id = person.id  # save the id of the individual who has already been included in first follow-up text
            sent_list.append(new_sent)
        match.sent = sent_list
        db.session.add(match)
        db.session.commit()
        # send message
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        print("Error matching: ", e)
        raise Exception(e)


def handle_next(user: User, text: str):
    try:
        # find latest matching table
        table = db.session.query(MatchTable).filter_by(sender_id=user.id).order_by(MatchTable.id).all()
        save_message(user, text, user.id)
        if len(table) < 1:  # user hasn't requested for any matching
            save_message(get_system_obj(), "You haven't made a match request yet", user.id)
            return jsonify({"message": "Message sent"}), 200
        # find latest match request
        last = table[-1]
        # find if 6 have been sent
        sent = last.sent.all()
        sent_serialized = [s.dict()['user_id'] for s in sent]
        all_matches = [pair_table.dict() for pair_table in last.matches.all()]
        not_sent = [x for x in all_matches if x['user2_id'] not in sent_serialized]

        if len(not_sent) < 1:
            save_message(get_system_obj(), "No more matches left", user.id)
            db.session.commit()
            return jsonify({"message": "Message sent"}), 200
        send_msg = ""
        new_sent = []
        # Pick 3
        for data in not_sent[:3]:
            person = db.session.query(User).filter(User.id == data["user2_id"]).one_or_none()
            new_sent.append(person)
            send_msg += f"{person.name} aged {person.age} {person.phone}.\n"
            sent.append(person)
        remaining = len(not_sent) - (len(sent) + 3)
        send_msg += f"Send NEXT to 22141 to receive details of the remaining {remaining if remaining > 0 else 0} {'ladies' if user.gender.name == 'MALE' else 'men'}"
        save_message(get_system_obj(), send_msg, user.id)
        # save those sent
        for new_s in new_sent:
            new_sent_record = SentMatched()
            new_sent_record.user_id = new_s.id
            new_sent_record.match_table_id = last.id
            db.session.add(new_sent_record)
        db.session.commit()
        return jsonify(sent_serialized), 200
    except Exception as e:
        print("Error handling next: ", e)
        raise Exception(e)


def request_user_data(user: User, phone: str):
    try:
        # Find the user
        found = db.session.query(User).filter_by(phone=phone).one_or_none()
        save_message(get_system_obj(), phone, user.id)
        if found is None:  # user not found
            save_message(get_system_obj(), "We could not find this user, double-check the number and try again",
                         user.id)
            db.session.commit()
            return jsonify({"message": "Message sent"}), 200
        # return jsonify(details), 200
        msg = descriptive_message_template(found)
        save_message(get_system_obj(), msg, user.id)
        # notify the user
        notification_msg = f"Hi {found.name.split(' ')[0]}, a {'man' if user.gender == Gender.MALE else 'lady'} called {user.name} is interested in you and requested your details. {'He' if user.gender == Gender.MALE else 'She'} is aged {user.age} based in {user.town}. Do you want to know more about {'him' if user.gender == Gender.MALE else 'her'}? Send YES to 22141"
        save_message(get_system_obj(), notification_msg, found.id)
        db.session.commit()
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        raise Exception("Error handling requesting user data: ", e)

def request_description(user: User, text: str):
    try:
        _prefix, phone = text.split(" ")
        found = db.session.query(User).filter_by(phone=phone).one_or_none()
        save_message(get_system_obj(), text, user.id)
        if found is None:
            save_message(get_system_obj(), "We could not find the user, please double-check the number and try again!", user.id)
            db.session.commit()
            return jsonify({"message": "Message sent"}), 200
        details = found.dict()["details"]
        msg = f"{found.name} describes {'herself' if found.gender == Gender.FEMALE else 'himself'} as {details['description']}"
        save_message(get_system_obj(), msg, user.id)
        db.session.commit()
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        raise Exception("Error handling request_description: ", e)


def follow_up_request_details(user: User, text: str):
    """Requested by the user whose information was requested"""
    try:
        save_message(user, text, user.id)
        # find the message informing them they are needed
        crush = db.session.query(Message).filter(Message.message.ilike(f"%interested%")).filter_by(user_id=user.id).order_by('created_at').all()
        found_serialized = [m.dict() for m in crush]
        if len(found_serialized) == 0:
            save_message(get_system_obj(), "We could not find any user who requested your information!", user.id)
            db.session.commit()
            return jsonify({"message": "Message sent"}), 200
        specific_msg = found_serialized[-1]
        print(specific_msg)
        crush_name = retrieve_text_between(["called", "is"], specific_msg['message'])
        if crush_name is None:
            save_message(get_system_obj(), "Sorry something went wrong. We could not find the user!", user.id)
            db.session.commit()
            return jsonify({"message": "Message sent"}), 200
        crush = db.session.query(User).filter(User.name == crush_name).one_or_none()
        if crush is None:
            save_message(get_system_obj(), "Sorry something went wrong. We could not find the user!", user.id)
            db.session.commit()
            return jsonify({"message": "Message sent"}), 200
        msg = descriptive_message_template(crush)
        save_message(get_system_obj(), msg, user.id)
        db.session.commit()
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        raise Exception("Error handling request_details: ", e)
