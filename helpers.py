from datetime import datetime, timedelta
import uuid

def email_to_code(email):
    user_id = email.split('@')[0]
    return user_id

def generate_id():
    return str(uuid.uuid4())

def get_datetime():
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return fecha_actual
