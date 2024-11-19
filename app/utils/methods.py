import re

def valid_number(phone: str)->(bool, str):
    # starts with 0
    if not phone.startswith("0"):
        return False, "Number should start with 0"
    if not len(phone) == 10:
        return False, "Number should have 10 digits"
    return bool(re.match(r'^[0-9]+$', phone)), ""

def retrieve_text_between(words:[str], text: str) -> str | None :
    pattern = rf"{words[0]}(.*?){words[1]}"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0].strip() if len(matches) > 0 else None