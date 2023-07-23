from flask import Flask, render_template, request
import datetime
import requests
import json

app = Flask(__name__, template_folder='templates')

BACKEND_URL = 'http://0.0.0.0:9000'

@app.route("/")
def home():
    current_day = datetime.datetime.today()
    current_date = current_day.date()
    current_time = current_day.time()
    print(current_time)
    return render_template("hello.html", current_date = current_date, current_time = current_time)



@app.route("/api/<name>/")
def name(name):
    return f"My name is {name}"



@app.route("/api/add/<a>/<b>")
def add_function(a,b):
    print(f"a and b is {a} , {b}")
    dicta = {"Sum of two numbers": int(a)+int(b)}
    return dicta


@app.route("/signup", methods=["POST"])
def signup():
    form_data = dict(request.form)
    requests.post(BACKEND_URL+'/signup', json=form_data)
    return "data send to the backend"


@app.route("/get_data")
def get_data():
    response = requests.get(BACKEND_URL + '/view')
    # print(response.__dict__)
    # byte_str = response.__dict__.get('_content')
    # print(byte_str)
    # data_string = byte_str.decode('utf-8')
    # data = json.loads(data_string)
    return response.json()




if __name__ == '__main___':
    app.run(host='0.0.0.0', port=8000, debug=True)
