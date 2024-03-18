from datetime import datetime
from helpers import email_to_code, get_datetime
import pyrebase
import uuid
import os
import json

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

def validador_multiples_sesiones(email):
    user_email = email
    logins = dict(db.child("sessions_log").order_by_child("user_id").equal_to(user_email).get().val())
    multiples_logins = False
    for i in logins.keys():
        if(len(logins[i].keys())==3):
            multiples_logins = True
    return multiples_logins

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

def insert_request(group_info, chatgpt_response, session_id, user_id):
    insert_dict = {}
    request_id = group_info['id_request']
    insert_dict['id_session'] = session_id
    insert_dict['id_request_group'] = group_info['id_request_group']
    insert_dict['file_name'] = group_info['file_name']
    insert_dict['id_user'] = user_id
    insert_dict['system_prompt_id'] = chatgpt_response['system_prompt_id']
    insert_dict['user_prompt'] = chatgpt_response['user_prompt']
    insert_dict['seed'] = chatgpt_response['seed']
    insert_dict['system_fingerprint'] = chatgpt_response['system_fingerprint']
    insert_dict['usage'] = chatgpt_response['usage']
    insert_dict['result_text'] = chatgpt_response['result_text']
    insert_dict['time_stamp'] = chatgpt_response['time_stamp']
    insert_dict['price'] = chatgpt_response['price']
    insert_dict['execution_time'] = chatgpt_response['execution_time']
    db.child('requests').child(request_id).set(insert_dict)
    return insert_dict

def select_system_prompt_by_id(system_prompt_id):
    system_prompt = dict(db.child('system_prompt').child(system_prompt_id).get().val())
    return system_prompt

def select_requests_by_id_request_group(id_request_group):
    requests = dict(db.child("requests").order_by_child("id_request_group").equal_to(id_request_group).get().val())
    return requests

def select_requests_group(user_id):

    #obtener datos de fb
    requests_group_user = db.child("requests_group").order_by_child("id_user").equal_to(user_id).get()
    # print(requests_group_user)
    # Ordenar las solicitudes por fecha de mayor a menor
    requests_group_user_order = sorted(requests_group_user.each(), key=lambda x: x.val().get("create_datetime", 0), reverse=True)
    # Convertir la lista ordenada en un diccionario
    requests_group_user_data = {request.key(): request.val() for request in requests_group_user_order}

    return requests_group_user_data

def select_requests(id_requests_group):
    requests = db.child("requests").order_by_child("id_request_group").equal_to(id_requests_group).get()
    requests_order = sorted(requests.each(), key=lambda x: x.val().get("time_stamp", 0))
    requests_data = {request.key(): request.val() for request in requests_order}

    return requests_data