from flask import Flask, session, render_template, request, redirect
from openai import OpenAI
import pyrebase
# import os
import os
import helper


app = Flask(__name__)

client = OpenAI()

config = {
    'apiKey': "AIzaSyCTeA7uOR0K7vdYvNDE5mnux1CIDyk61Aw",
    'authDomain': "ai-feedback-generator.firebaseapp.com",
    'projectId': "ai-feedback-generator",
    'storageBucket': "ai-feedback-generator.appspot.com",
    'messagingSenderId': "501121730918",
    'appId': "1:501121730918:web:85f0198b401024e59c20a7",
    'measurementId': "G-2LTX4Q4FL9",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = 'secret'

conversations = []

@app.route('/login')
def login():
    if('user' in  session):
        return 'Hi, {}'.format(session['user'])
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
        except:
            return 'Failet to access'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('login.html')

## rutas
@app.route('/')
def index():
    return render_template('feedback-gen.html')

# pestaña 1
@app.route('/feedback-gen')
def option1():

    return render_template('feedback-gen.html')

# pestaña 2
@app.route('/historial')
def option2():
    return render_template('feedback-list.html')

# preview hitoric
@app.route('/feedback-preview')
def preview():
    return render_template('feedback-preview.html')


# preview hitoric
@app.route('/feedback-test')
def prev_test():
    return render_template('test.html')

# preview hitoric
@app.route('/test-upload', methods=['POST'])
def test_rec_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        print('Received file:', file.filename.split('.')[-1])
        if(file.filename.split('.')[-1]=='docx'):
            print(helper.extract_text_from_docx(file))
        if(file.filename.split('.')[-1]=='pdf'):
            print(helper.extract_text_from_pdf(file))
        return 'File uploaded successfully'





# # ruta uso api
# @app.route('/', methods=['GET', 'POST'])
# def openai_api():
#     if request.method == 'GET':
#         return render_template('index.html', chat=conversations)
    
#     if request.method == 'POST':
#         question = request.form.get('question')

#         if question:
#             response = client.chat.completions.create(
#                 model = 'gpt-3.5-turbo-0125',
#                 messages= [
#                     {"role": "system", "content": ""},
#                     {"role": "user", "content" : question}
#                 ],
#                 temperature = 0.5,
#                 max_tokens = 150,
#                 top_p = 1,
#                 frequency_penalty = 0,
#                 presence_penalty = 0.6
#             )

#             answer = 'AI: ' + str(response.choices[0].message.content)
#             question = 'Yo: ' + question

#             conversations.append(question)
#             conversations.append(answer)

#         return render_template('index.html', chat = conversations)

# # limpiar conversacion
# @app.route('/limpiar_conversation', methods=['POST'])
# def limpiar_array():
#     conversations.clear()
#     return render_template('index.html')

# ruta nosotros
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# bloque de prueba
if __name__ == '__main__':
    app.run(debug=True)