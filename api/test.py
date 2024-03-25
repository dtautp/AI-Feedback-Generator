from flask import Flask

test = Flask(__name__)

@test.route('/mi_test', methods=['POST','GET'])
def home():
    return "hello_world"

if __name__ == '__main__':
    test.run(debug=True)