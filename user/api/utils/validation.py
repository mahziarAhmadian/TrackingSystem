import re


def is_email(string):
    if not isinstance(string, str):
        return False
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(email_regex, string):
        return True
    return False


def is_phone_number(string):
    if not isinstance(string, str):
        return False
    phone_regex = '^[0][9]([0-9]){9}$'
    if re.search(phone_regex, string):
        return True
    return False

def is_national_id(string):
    return True


# print(is_phone_number(None))
