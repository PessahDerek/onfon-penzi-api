import re
import datetime
from jose import jwt


def valid_number(phone: str) -> (bool, str):
    # starts with 0
    if not phone.startswith("0"):
        return False, "Number should start with 0"
    if not len(phone) == 10:
        return False, "Number should have 10 digits"
    return bool(re.match(r'^[0-9]+$', phone)), ""


def retrieve_text_between(words: [str], text: str) -> str | None:
    pattern = rf"{words[0]}(.*?){words[1]}"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0].strip() if len(matches) > 0 else None


def generate_token(user_id: int) -> str:
    expire = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
        minutes=120
    )
    return jwt.encode(
        algorithm='HS256',
        claims={'id': user_id, "exp": expire},
        key="fjk$al$sfj(#als$_fji309-2#_($_!_)#_LCK:ASK_kfl,cc93-_(@!_$(%**"
    )


def decode_token(token: str) -> dict | None:
    try:
        if token is None:
            return None
        return jwt.decode(
            token=token,
            key="fjk$al$sfj(#als$_fji309-2#_($_!_)#_LCK:ASK_kfl,cc93-_(@!_$(%**",
            algorithms=['HS256']
        )
    except Exception as e:
        print(e)
        return None
