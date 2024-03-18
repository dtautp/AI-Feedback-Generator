from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash, send_file, after_this_request
from openai_module import create_post_openAI
from openai_module import request_prompt
from openai_module import extract_feedback_from_response
from firebase_module import validator_login, add_end_datetime_session, insert_requests_group, select_requests_by_id_request_group,  select_requests_group, insert_request, select_requests, validador_multiples_sesiones
from extract_text import update_textAssignments, create_request_group
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
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))


    session_details = session.get('session_details',{})
    session_id = session.get('session_id', None)
    print(session_details)
    print(session_id)
    global text_assignments
    text_assignments.clear()
    return render_template('feedback-generator.html', current_route='/feedback-generator')

@app.route('/read-assignments', methods=['GET','POST'])
def read_assignments():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

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
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

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
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))
    
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
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))
    
    user_id = session.get('session_details',{})['user_id']
    requests_group_user = select_requests_group(user_id)
    return render_template('feedback-historic.html', current_route='/feedback-historic', requests_group_user=requests_group_user)

@app.route('/feedback-preview/<id_requests_group>')
def preview(id_requests_group):
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

    requests = select_requests(id_requests_group)
    return render_template('feedback-preview.html', current_route='/feedback-historic', requests=requests, id_requests_group=id_requests_group)

@app.route('/feedback-test')
def prev_test():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

    return render_template('test.html')

# ruta uso api
@app.route('/test-openai', methods=['GET', 'POST'])
def openai_api():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('api-openai.html')
    
    if request.method == 'POST':
        question = request.form.get('question')

        if question:
            conversations = create_post_openAI(question)

        return render_template('api-openai.html', chat = conversations)



@app.route('/read-assignments2', methods=['GET','POST'])
def read_assignments2():
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

contador_progreso = 0
@app.route('/show-text-assignments2')
async def show_text_assignments2():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

    global contador_progreso
    contador_progreso = 0
    return render_template('feedback-generator5.html')

@app.route('/loading')
async def loading():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))
    
    request_group = json.loads(request.args.get('request_group'))
    print('Loading' + str(request_group))
    print(type(request_group))
    return render_template('loading.html', request_group=json.dumps(request_group), doc_number=len(request_group['request_group']))

@app.route('/get-counter-semaphore', methods=['GET'])
def get_counter_semaphore():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))

    # Return the value of counter_semaphore
    return json.dumps({'counter_semaphore_value': counter_semaphore._value})

# Initialize a semaphore
counter_semaphore = asyncio.Semaphore(0)

#
@app.route('/processing', methods=['GET','POST'])
async def processing():
    # Asegurar que el usuario se encuentre logeado
    if 'session_details' not in  session:
        return redirect(url_for('login'))
    
    request_group = request.form.get('request_group')

    print("Process" + str(request_group))
    print(type(request_group))

    request_group = json.loads(request_group)["request_group"]
    print("Process" + str(request_group))
    print(type(request_group))

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

    return redirect(url_for('preview', id_requests_group=id_request_group))   
    # return render_template('feedback-generator4.html', text_assignments=request_group, id_request_group=id_request_group)


# ruta uso api
@app.route('/test_s', methods=['GET', 'POST'])
def test_s():
    print(request.files.getlist('selectedFiles[]'))
    return "hello world"
    


if __name__ == '__main__':
    app.run(debug=True)