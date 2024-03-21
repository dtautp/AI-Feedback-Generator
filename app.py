from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash, send_file, after_this_request
from openai_module import create_post_openAI
from openai_module import request_prompt
from openai_module import extract_feedback_from_response
from firebase_module import validator_login, add_end_datetime_session, insert_requests_group, select_requests_by_id_request_group,  select_requests_group, insert_request, select_requests, validador_multiples_sesiones
from extract_text import update_textAssignments, create_request_group, create_request_group2
from exportar_word import document_print, preparar_diccionario
from helpers import format_datetime, first_paragraph_value, second_paragraph_value
import json
import time
import os
import asyncio

# import uuid
# from datetime import datetime

app = Flask(__name__)

# custom filter
app.jinja_env.filters["format_date"] = format_datetime
app.jinja_env.filters["first_paragraph_value"] = first_paragraph_value
app.jinja_env.filters["second_paragraph_value"] = second_paragraph_value

app.secret_key = 'secret'

conversations = []
text_assignments = []


# 1
@app.route('/', methods=['POST','GET'])
def login():
    if 'session_details' in  session:
        return redirect(url_for('feedback_generator'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if(validador_multiples_sesiones(email)):
            return render_template('login.html', error_code = 'Multiples sesiones')
        try:
            result = validator_login(email, password)
            session['session_details'] = result['session_details']
            session['session_id'] = result['session_id']
            print(session)
            return redirect(url_for('feedback_generator'))
        except:
            return render_template('login.html', error_code = 'Login Fallido')
        
    return render_template('login.html')

# 2
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


@app.route('/guardar_resultados', methods=['POST'])
def guardar_resultados():
    resultados = request.json
    request_group = create_request_group2(resultados)
    print("guardar: " + str(request_group))

    return json.dumps({'request_group':request_group})

@app.route('/feedback-generator', methods=['GET','POST'])
def feedback_generator():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        files = request.files.getlist('archivo')
        request_group = create_request_group(files)
        print('Read' + str(request_group))
            
    return render_template('feedback-generator.html', current_route='/feedback-generator')



# 4
@app.route('/read-assignments', methods=['GET','POST'])
def read_assignments():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

    request_group = []

    if request.method == 'POST':
        files = request.files.getlist('selectedFiles[]')
        if files:
            request_group = create_request_group(files)
            print('Read' + str(request_group))
            # return redirect(url_for('show_text_assignments'))
        else:
            return "No se recibieron archivos"
    return redirect(url_for('loading', request_group=json.dumps({'request_group':request_group})))

# 5
@app.route('/loading', methods=['GET','POST'])
async def loading():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))
    
    global counter_semaphore
    counter_semaphore = asyncio.Semaphore(0)
    request_group = json.loads(request.form['request_group'])
    print('Loading' + str(request_group))
    print(type(request_group))
    return render_template('loading.html', request_group=json.dumps(request_group), doc_number=len(request_group['request_group']))

# 6
counter_semaphore = asyncio.Semaphore(0) # Initialize a semaphore
@app.route('/get-counter-semaphore', methods=['GET'])
def get_counter_semaphore():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))
    
    # Return the value of counter_semaphore
    return json.dumps({'counter_semaphore_value': counter_semaphore._value})

# 7
@app.route('/processing', methods=['GET','POST'])
async def processing():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))
    
    request_group = request.form.get('request_group')
    request_group = json.loads(request_group)["request_group"]

    global counter_semaphore
    counter_semaphore = asyncio.Semaphore(0)
    user_id = session.get('session_details',{})['user_id']
    file_text = []
    insert_requests_group_result = insert_requests_group(request_group, user_id)
    id_request_group = ''
    tasks = []

    async def track_and_execute(index, task, counter_semaphore):
        nonlocal id_request_group
        result = await task # Wait for the task to finish
        counter_semaphore.release() # Increase the counter
        if result is not None:
            insert_request(request_group[index], result, session.get('session_id'), user_id) # Perform your insertions here

    for item in request_group:
        id_request_group = item['id_request_group']
        task = asyncio.create_task(request_prompt(1, item['file_text']))
        tasks.append(task)
    
    chatgpt_responses = await asyncio.gather(*[track_and_execute(index, task, counter_semaphore) for index, task in enumerate(tasks)])

    

    await counter_semaphore.acquire() # Wait until all tasks are completed
    return redirect(url_for('preview', id_requests_group=id_request_group))
    

    


@app.route('/generate_response_file',methods=['POST','GET'])
def download_temp_document():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))
    
    file = preparar_diccionario(select_requests_by_id_request_group(request.form.get('id_request_group')))
    return send_file(file, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', as_attachment=True, download_name='feedback.docx')


@app.route('/feedback-historic')
def feedback_historic():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))
    
    requests_group_user = select_requests_group(session.get('session_details',{})['user_id'])
    return render_template('feedback-historic.html', current_route='/feedback-historic', requests_group_user=requests_group_user)

@app.route('/feedback-preview/<id_requests_group>')
def preview(id_requests_group):
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

    requests = select_requests(id_requests_group)
    return render_template('feedback-preview.html', current_route='/feedback-historic', requests=requests, id_requests_group=id_requests_group)








if __name__ == '__main__':
    app.run(debug=True)