import os
import sys

current_file_path = os.path.abspath(__file__)
if(current_file_path[:4]=='/var'):
    module_dir = os.path.abspath('/var/task/api')
    sys.path.append(module_dir)

from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash, send_file, after_this_request
from firebase_module import validator_login, validator_login_datos, add_end_datetime_session, select_requests_by_id_request_group, select_requests_group, select_requests, validador_multiples_sesiones, validador_session, contador_descargas, contador_copias, select_value_request_group
from exportar_word import preparar_diccionario
from helpers import format_datetime, first_paragraph_value, second_paragraph_value, format_time_stamp, get_form_by_homework, get_feedback, get_name_homework
import json

app = Flask(__name__)

# custom filter
app.jinja_env.filters["format_date"] = format_datetime
app.jinja_env.filters["format_time_stamp"] = format_time_stamp
app.jinja_env.filters["first_paragraph_value"] = first_paragraph_value
app.jinja_env.filters["second_paragraph_value"] = second_paragraph_value
app.jinja_env.filters["get_feedback"] = get_feedback
app.jinja_env.filters["get_name_homework"] = get_name_homework

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

@app.route('/', methods=['POST','GET'])
def login():
    if 'session_details' in  session:
        return redirect(url_for('feedback_historic'))

    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        sesiones_multiples = validador_multiples_sesiones(email)
        if(sesiones_multiples[0]>0):
            for i in sesiones_multiples[1]:
                add_end_datetime_session(i)
        try:
            result = validator_login(email, password)
            session['session_details'] = result['session_details']
            session['session_id'] = result['session_id']
            return redirect(url_for('feedback_historic'))
        except Exception as e:
            print(e)
            return render_template('login.html', error_code = "Usuario o contraseña incorrectos")
    if 'error_code' in request.args:
        return render_template('login.html', error_code = request.args['error_code'])
    return render_template('login.html')

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

@app.route('/logout')
def logout():
    session_details = session.get('session_details',{})
    session_id = session.get('session_id', None)

    if session_details:
        add_end_datetime_session(session_id)
        session_details = session.pop('session_details', {})
        session_id = session.pop('session_id', None)

    return redirect(url_for('login'))
    
@app.route('/generate_response_file',methods=['POST','GET'])
def download_temp_document():
    id_request_group = request.form.get('id_request_group')
    request_group = select_value_request_group(id_request_group)
    link_form_homework = get_form_by_homework(request_group.get('homework_number', ''))
    homework_number = request_group.get('homework_number', '')
    nro_clase = request_group.get('nro_clase', '')
    file = preparar_diccionario(select_requests_by_id_request_group(id_request_group), link_form_homework, homework_number)
    contador_descargas(id_request_group)
    filename_download = f'feedback_{homework_number}_{nro_clase}.docx'
    return send_file(file, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', as_attachment=True, download_name=filename_download)

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
    sorted_requests = dict(sorted(requests.items(), key=lambda item: item[1]['file_name']))
    request_group = select_value_request_group(id_requests_group)
    # link_form_homework = get_form_by_homework(request_group['homework_number'])
    # homework_number = request_group['homework_number']
    # nro_clase = request_group.get('nro_clase', '')
    link_form_homework = get_form_by_homework(request_group.get('homework_number', ''))
    homework_number = request_group.get('homework_number', '')
    nro_clase = request_group.get('nro_clase', '')

    return render_template('feedback-preview.html', current_route='/feedback-historic', requests=sorted_requests, id_requests_group=id_requests_group, link_form_homework=link_form_homework, homework_number=homework_number, nro_clase=nro_clase)

if __name__ == '__main__':
    app.run(debug=True)