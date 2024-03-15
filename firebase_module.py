from datetime import datetime
from helpers import email_to_code, get_datetime
import pyrebase
import uuid
import os

config = {
    'apiKey': os.environ.get('FIREBASE_API_KEY'),
    'authDomain': os.environ.get("FIREBASE_AUTH_DOMAIN"),
    'projectId': os.environ.get("FIREBASE_PROJECT_ID"),
    'storageBucket': os.environ.get("FIREBASE_STORAGE_BUCKET"),
    'messagingSenderId': os.environ.get("FIREBASE_MESSAGINGSENDER_ID"),
    'appId': os.environ.get("FIREBASE_APP_ID"),
    'measurementId': os.environ.get("FIREBASE_MEASUREMENT_ID"),
    'databaseURL': 'https://ai-feedback-generator-default-rtdb.firebaseio.com'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def validator_login(email, password):
    user = auth.sign_in_with_email_and_password(email, password)
    current_datetime = get_datetime()
    session_id = str(uuid.uuid4())
    session_details = {
        'user_id': email_to_code(email),
        'user_email': email,
        'start_datetime': current_datetime
    }
    db.child('sessions_log').child(session_id).set(session_details)
    return {'session_id': session_id, 'session_details': session_details}

def add_end_datetime_session(session_id):
    end_datetime = get_datetime()
    db.child('sessions_log').child(session_id).child('end_datetime').set(end_datetime)

def insert_requests_group(request_group, use_id):
    request_group_data = {}
    for request in request_group:
        group_id = request['id_request_group']
        if group_id not in request_group_data:
            request_group_data[group_id] = {
                'id_user': use_id,
                'id_request': [],
                'file_name': [],
                'create_datetime': request['create_datetime'],
            }
        request_group_data[group_id]['id_request'].append(request['id_request'])
        request_group_data[group_id]['file_name'].append(request['file_name'])

    # print(request_group_data[group_id])
    db.child('requests_group').child(group_id).set(request_group_data[group_id])

def insert_request():
    return None

def select_system_prompt_by_id(system_prompt_id):
    system_prompt = dict(db.child('system_prompt').child(system_prompt_id).get().val())
    return system_prompt