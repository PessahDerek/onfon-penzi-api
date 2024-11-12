
def valid_number(phone: str)->(bool, str):
    # starts with 0
    if not phone.startswith("0"):
        return False, "Number should start with 0"
    if not len(phone) == 10:
        return False, "Number should have 10 digits"
    return True, ""
