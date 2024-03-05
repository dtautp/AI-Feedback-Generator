from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI()

conversations = []

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