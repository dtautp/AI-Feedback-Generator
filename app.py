from flask import Flask, session, render_template, request, redirect
from openai_module import create_post_openAI
from firebase_module import validator_login
import helper

app = Flask(__name__)

app.secret_key = 'secret'

conversations = []

@app.route('/login', methods=['POST','GET'])
def login():
    if('user' in  session):
        return render_template('feedback-generator.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = validator_login(email, password)
            session['user'] = email
            return render_template('feedback-generator.html')
        except:
            return 'Failet to access'
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login.html')

## rutas
@app.route('/')
def index():
    return render_template('feedback-generator.html')

# pestaña 1
@app.route('/feedback-generator')
def option1():

    return render_template('feedback-generator.html')

# pestaña 2
@app.route('/feedback-historic')
def option2():
    return render_template('feedback-historic.html')

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
@app.route('/limpiar_conversation', methods=['POST'])
def limpiar_array():
    conversations.clear()
    return render_template('api-openai.html')

# ruta nosotros
# @app.route('/nosotros')
# def nosotros():
#     return render_template('feedback-gen copy.html')

# bloque de prueba
if __name__ == '__main__':
    app.run(debug=True)