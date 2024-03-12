from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash
from openai_module import create_post_openAI
from firebase_module import validator_login, add_end_datetime_session
from extract_text import update_textAssignments
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
        files = request.files.getlist('files[]')
        if len(files) != 0:
            print("si hay datos")
            global text_assignments
            text_assignments = update_textAssignments(files)

        print("No hay nada en la lista") 
        return redirect(url_for('show_text_assignments'))
        
    return render_template('feedback-generator3.html')

@app.route('/show-text-assignments')
def show_text_assignments():
    global text_assignments
    text_assignments2 = text_assignments
    return render_template('feedback-generator3.html', text_assignments=text_assignments2)

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

# limpiar conversacion
@app.route('/limpiar_conversation')
def limpiar_array():
    conversations.clear()
    print(conversations)
    return render_template('api-openai.html')

if __name__ == '__main__':
    app.run(debug=True)