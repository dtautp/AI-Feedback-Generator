from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash
from openai_module import create_post_openAI
from openai_module import request_prompt
from openai_module import extract_feedback_from_response
from firebase_module import validator_login, add_end_datetime_session, insert_requests_group
from extract_text import update_textAssignments, create_request_group
from exportar_word import document_print
import json
import time
# from helpers import email_to_code
# import uuid
# from datetime import datetime

app = Flask(__name__)

app.secret_key = 'secret'

conversations = []
text_assignments = []

@app.route('/', methods=['POST','GET'])
def login():
    if 'session_details' in  session:
        return redirect(url_for('feedback_generator'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            result = validator_login(email, password)
            session['session_details'] = result['session_details']
            session['session_id'] = result['session_id']
            return redirect(url_for('feedback_generator'))
        except:
            return 'Failet to access'
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session_details = session.get('session_details',{})
    session_id = session.get('session_id', None)
    print(session_details)
    print(session_id)

    if session_details:
        add_end_datetime_session(session_id)
        session_details = session.pop('session_details', {})
        session_id = session.pop('session_id', None)

    return redirect(url_for('login'))

@app.route('/feedback-generator')
def feedback_generator():
    session_details = session.get('session_details',{})
    session_id = session.get('session_id', None)
    print(session_details)
    print(session_id)
    global text_assignments
    text_assignments.clear()
    return render_template('feedback-generator.html', current_route='/feedback-generator')

@app.route('/read-assignments', methods=['GET','POST'])
def read_assignments():
    if request.method == 'POST':
        files = request.files.getlist('Files[]')
        if files:
            global text_assignments
            text_assignments = update_textAssignments(files)
            # return redirect(url_for('show_text_assignments'))
        else:
            return "No se recibieron archivos"
    return render_template('feedback-generator3.html')

@app.route('/prueba')
def prueba():
    return redirect(url_for('show_text_assignments'))

@app.route('/show-text-assignments')
def show_text_assignments():
    file_text = []
    dic_list = []
    for item in text_assignments:
        # Procesamiento del feedback
        respuesta_diccionario = request_prompt(item['file_text'])
        print(respuesta_diccionario)
        dic = {}
        dic['archivo_nombre'] = (2, respuesta_diccionario['system_prompt_id'])
        dic['Fecha proceso'] = (0, respuesta_diccionario['time_stamp'])
        dic['Tarea entregada'] = (1, respuesta_diccionario['user_prompt'])
        text = ''
        text += json.loads(respuesta_diccionario['message'])['first_paragraph'] + '\n\n'
        for i in json.loads(respuesta_diccionario['message'])['second_paragraph']:
            text += i[list(i.keys())[0]] + ' '
        dic['Feedback'] = (1, text)
        # -------
        file_text.append(extract_feedback_from_response(respuesta_diccionario))
        # respuesta = create_post_openAI(item['file_text'])
        # print(respuesta)
    print('show-text-assignments', file_text)
    doc_url = document_print(dic_list, './temp_files/',str(int(time.time()*1000))+'.docx')
    return render_template('feedback-generator3.html', text_assignments=file_text, doc_url=doc_url)

@app.route('/feedback-historic')
def feedback_historic():
    return render_template('feedback-historic.html', current_route='/feedback-historic')

@app.route('/feedback-preview')
def preview():
    return render_template('feedback-preview.html')

@app.route('/feedback-test')
def prev_test():
    return render_template('test.html')

# ruta uso api
@app.route('/test-openai', methods=['GET', 'POST'])
def openai_api():
    if request.method == 'GET':
        return render_template('api-openai.html')
    
    if request.method == 'POST':
        question = request.form.get('question')

        if question:
            conversations = create_post_openAI(question)

        return render_template('api-openai.html', chat = conversations)

request_group = []

@app.route('/read-assignments2', methods=['GET','POST'])
def read_assignments2():
    if request.method == 'POST':
        files = request.files.getlist('Files[]')
        if files:
            global request_group
            request_group = create_request_group(files)
            # return redirect(url_for('show_text_assignments'))
        else:
            return "No se recibieron archivos"
    return render_template('feedback-generator4.html')

@app.route('/show-text-assignments2')
def show_text_assignments2():
    user_id = session.get('session_details',{})['user_id']
    file_text = []
    insert_requests_group_result = insert_requests_group(request_group, user_id)
    
    for item in request_group:
        file_text.append(item['file_text'])
        # respuesta = create_post_openAI(item['file_text'])
        # print(respuesta)
    print('show-text-assignments', file_text)
    return render_template('feedback-generator4.html', text_assignments=request_group)


if __name__ == '__main__':
    app.run(debug=True)