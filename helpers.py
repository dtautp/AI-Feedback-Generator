import datetime

def email_to_code(email):
    user_id = email.split('@')[0]
    return user_id