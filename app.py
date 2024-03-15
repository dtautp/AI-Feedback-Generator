from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash, send_file, after_this_request
from openai_module import create_post_openAI
from openai_module import request_prompt
from openai_module import extract_feedback_from_response
from firebase_module import validator_login, add_end_datetime_session, insert_requests_group, insert_request, select_requests_by_id_request_group
from extract_text import update_textAssignments, create_request_group
from exportar_word import document_print, preparar_diccionario
import json
import time
import os
import asyncio
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
    lis_responses = []
    for item in text_assignments:
        respuesta_diccionario = request_prompt(1,item['file_text'])
        lis_responses.append(respuesta_diccionario)
        file_text.append(extract_feedback_from_response(respuesta_diccionario))
        # respuesta = create_post_openAI(item['file_text'])
        # print(respuesta)
    print('show-text-assignments', file_text)
    return render_template('feedback-generator3.html', text_assignments=file_text, lis_responses=json.dumps({'lis_responses':lis_responses}))


@app.route('/generate_response_file',methods=['POST','GET'])
def download_temp_document():
    id_request_group = request.form.get('id_request_group')
    file_name = preparar_diccionario(select_requests_by_id_request_group(id_request_group))
    @after_this_request
    def remove_temp_file(res):
        for i in os.listdir('./temp_files/'):
            try:
                os.remove('./temp_files/'+i)
            except Exception as error:
                app.logger.error("Error removing file: %s", error)
                continue
        return res
    return send_file(file_name, as_attachment=True)


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

contador_progreso = 0
@app.route('/show-text-assignments2')
async def show_text_assignments2():
    global contador_progreso
    contador_progreso = 0
    return render_template('feedback-generator5.html')

@app.route('/get-counter-semaphore', methods=['GET'])
def get_counter_semaphore():
    # Return the value of counter_semaphore
    return json.dumps({'counter_semaphore_value': counter_semaphore._value, 'doc_number':len(request_group)})

# Initialize a semaphore
counter_semaphore = asyncio.Semaphore(0)

#
@app.route('/show-text-assignments3', methods=['GET','POST'])
async def show_text_assignments3():
    global counter_semaphore
    counter_semaphore = asyncio.Semaphore(0)
    user_id = session.get('session_details',{})['user_id']
    file_text = []
    insert_requests_group_result = insert_requests_group(request_group, user_id)
    id_request_group = ''
    tasks = []

    async def track_and_execute(index, task, counter_semaphore):
        nonlocal id_request_group
        
        # Wait for the task to finish
        result = await task
        
        # Increase the counter
        counter_semaphore.release()
        print("Semaphore value:", counter_semaphore._value)

        if result is not None:
            # Perform your insertions here
            insert_request(request_group[index], result, session.get('session_id'), user_id)


    for item in request_group:
        id_request_group = item['id_request_group']
        task = asyncio.create_task(request_prompt(1, item['file_text']))
        tasks.append(task)
    
    start_time = time.time()
    chatgpt_responses = await asyncio.gather(*[track_and_execute(index, task, counter_semaphore) for index, task in enumerate(tasks)])
    end_time = time.time()
    print(end_time - start_time)

    # Wait until all tasks are completed
    await counter_semaphore.acquire()
        
    return render_template('feedback-generator4.html', text_assignments=request_group, id_request_group=id_request_group)
    


if __name__ == '__main__':
    app.run(debug=True)