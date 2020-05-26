from flask import Flask, request

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post_route():
    if request.method == 'POST':

        data = request.get_json()
        print(type(data))
        x = dict(data)
        print('dict x: ', x)

        print('Data Received: "{data}"'.format(data=data))
        return "Request Processed.\n"