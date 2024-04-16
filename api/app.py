from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash, send_file, after_this_request
from openai_module import create_post_openAI, request_prompt, extract_feedback_from_response
from firebase_module import validator_login, validator_login_datos, add_end_datetime_session, insert_requests_group, select_requests_by_id_request_group,  select_requests_group, insert_request, select_requests, validador_multiples_sesiones, validador_session, contador_descargas, contador_copias
from extract_text import update_textAssignments, create_request_group, create_request_group2
from exportar_word import document_print, preparar_diccionario
from helpers import format_datetime, first_paragraph_value, second_paragraph_value, format_time_stamp
import json
import time
import os
import asyncio
import sys

# import uuid
# from datetime import datetime
# this comment is a test

app = Flask(__name__)

# custom filter
app.jinja_env.filters["format_date"] = format_datetime
app.jinja_env.filters["format_time_stamp"] = format_time_stamp
app.jinja_env.filters["first_paragraph_value"] = first_paragraph_value
app.jinja_env.filters["second_paragraph_value"] = second_paragraph_value

app.secret_key = 'secret'

conversations = []
text_assignments = []


excluded_routes = ['', 'user_cheking','static','guardar_resultados','.well-known','get_ruta']  # Add routes to exclude from session verification
@app.before_request
def before_request():
    if(str(request.path).split('/')[1] not in excluded_routes):
        if 'session_details' not in  session:
            print("Sesion Flask no encontrada")
            return redirect(url_for('login', error_code="Sesión Error"))
        val_ses = validador_session(session['session_id'])
        if(val_ses == None):
            session.pop('session_details', {})
            session.pop('session_id', None)
            print("Sesion Val resulto None")
            return redirect(url_for('login', error_code="Sesión Error"))
        elif(val_ses == True):
            session.pop('session_details', {})
            session.pop('session_id', None)
            print("Sesion Val resulto True")
            return redirect(url_for('login', error_code="Se ha cerrado la sesión"))



    

# 1
@app.route('/', methods=['POST','GET'])
def login():
    if 'session_details' in  session:
        return redirect(url_for('feedback_generator'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        sesiones_multiples = validador_multiples_sesiones(email)
        if(sesiones_multiples[0]>0):
            for i in sesiones_multiples[1]:
                add_end_datetime_session(i)
        try:
            result = validator_login(email, password)
            session['session_details'] = result['session_details']
            session['session_id'] = result['session_id']
            return redirect(url_for('feedback_generator'))
        except Exception as e:
            print(e)
            return render_template('login.html', error_code = "Usuario o contraseña incorrectos")
    if 'error_code' in request.args:
        return render_template('login.html', error_code = request.args['error_code'])
    return render_template('login.html')

# 1
@app.route('/user_cheking', methods=['POST','GET'])
def user_cheking():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        try:
            # Validar de que el usuario sea correcto
            validator_login_datos(email, password)
            # Validar multiples sesiones
            sesiones_multiples = validador_multiples_sesiones(email)
            if(sesiones_multiples[0]>0):
                return json.dumps({'response':400, 'error_code':'multi_login'})
        except Exception as e:
            print(e)
            return json.dumps({'response':400, 'error_code':'login_fail'})
    
    return json.dumps({'response':200, 'error_code':''})

# 2
@app.route('/logout')
def logout():
    session_details = session.get('session_details',{})
    session_id = session.get('session_id', None)

    if session_details:
        add_end_datetime_session(session_id)
        session_details = session.pop('session_details', {})
        session_id = session.pop('session_id', None)

    return redirect(url_for('login'))




@app.route('/feedback-generator', methods=['GET','POST'])
def feedback_generator():

    if request.method == 'POST':
        files = request.files.getlist('archivo')
        request_group = create_request_group(files)
            
    return render_template('feedback-generator.html', current_route='/feedback-generator')

@app.route('/guardar_resultados', methods=['POST'])
def guardar_resultados():
    resultados = request.json
    request_group = create_request_group2(resultados)
    return json.dumps({'request_group':request_group})



# 4
@app.route('/read-assignments', methods=['GET','POST'])
def read_assignments():
    request_group = []

    if request.method == 'POST':
        files = request.files.getlist('selectedFiles[]')
        if files:
            request_group = create_request_group(files)
            # return redirect(url_for('show_text_assignments'))
        else:
            return "No se recibieron archivos"
    return redirect(url_for('loading', request_group=json.dumps({'request_group':request_group})))

# 5
@app.route('/loading', methods=['GET','POST'])
async def loading():
    
    global counter_semaphore
    counter_semaphore = asyncio.Semaphore(0)
    request_group = json.loads(request.form['request_group'])
    return render_template('loading.html', request_group=json.dumps(request_group), doc_number=len(request_group['request_group']), homework_number = request.form['homework_number'])

request_group_len = 0

# 6
counter_semaphore = asyncio.Semaphore(0) # Initialize a semaphore

# 7
@app.route('/processing', methods=['GET','POST'])
async def processing():
    time_start = time.time()
    
    global request_group_len
    request_group = request.form.get('request_group')
    request_group = json.loads(request_group)["request_group"]
    request_group_len = len(request_group)

    global counter_semaphore
    counter_semaphore = asyncio.Semaphore(0)
    user_id = session.get('session_details',{})['user_id']
    file_text = []
    insert_requests_group_result = insert_requests_group(request_group, user_id, request.form.get('homework_number'))
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
    

    try:
        # chatgpt_responses = await asyncio.gather(*[track_and_execute(index, task, counter_semaphore) for index, task in enumerate(tasks)])
        tasks_coroutines = [asyncio.wait_for(track_and_execute(index, task, counter_semaphore), 40) for index, task in enumerate(tasks)]
        chatgpt_responses = await asyncio.gather(*tasks_coroutines) 
        print('Tiempo suficiente')
    except Exception as e:
        print(e)
        return redirect(url_for('preview', id_requests_group=id_request_group, err_code='timeout'))
    

    await counter_semaphore.acquire() # Wait until all tasks are completed

    time_end = time.time()
    print('Exec: ' + str(time_end - time_start))

    return redirect(url_for('preview', id_requests_group=id_request_group))
    

    


@app.route('/generate_response_file',methods=['POST','GET'])
def download_temp_document():
    id_request_group = request.form.get('id_request_group')
    file = preparar_diccionario(select_requests_by_id_request_group(id_request_group))
    contador_descargas(id_request_group)
    return send_file(file, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', as_attachment=True, download_name='feedback.docx')

@app.route('/feedback-preview/contador_copiar',methods=['PUT'])
def contador_copiar():
    if request.method == 'PUT':
        contador_copias(request.json['request_id'])
    return json.dumps({'response':200})


@app.route('/feedback-historic')
def feedback_historic():
    requests_group_user = select_requests_group(session.get('session_details',{})['user_id'])
    return render_template('feedback-historic.html', current_route='/feedback-historic', requests_group_user=requests_group_user)


@app.route('/feedback-preview/<id_requests_group>')
def preview(id_requests_group):
    requests = select_requests(id_requests_group)
    return render_template('feedback-preview.html', current_route='/feedback-historic', requests=requests, id_requests_group=id_requests_group)

@app.route('/get_ruta')
def get_ruta():
    current_file_path = os.path.abspath(__file__)
    print(current_file_path)
    print(current_file_path.split('\\'))
    if(current_file_path.split('\\')[1]=='var'):
        module_dir = os.path.abspath('/var/task/api')
        sys.path.append(module_dir)

    for path in sys.path:
        print(path)
    return current_file_path

if __name__ == '__main__':
    app.run(debug=True)