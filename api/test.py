from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)