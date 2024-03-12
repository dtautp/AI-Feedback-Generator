from datetime import datetime
from helpers import email_to_code
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
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session_id = str(uuid.uuid4())
    session_details = {
        'user_id': email_to_code(email),
        'user_email': email,
        'start_datetime': current_datetime
    }
    db.child('sessions_log').child(session_id).set(session_details)
    return {'session_id': session_id, 'session_details': session_details}

def add_end_datetime_session(session_id):
    end_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.child('sessions_log').child(session_id).child('end_datetime').set(end_datetime)