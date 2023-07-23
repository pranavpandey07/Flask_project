from flask import Flask, request
from dotenv import load_dotenv
from pymongo import MongoClient
import urllib.parse
import os
import json

app = Flask(__name__, template_folder='templates')

load_dotenv()

db_host = os.environ.get('DB_HOST')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
db_name = os.environ.get('DB_NAME')
host = os.environ.get('CLUSTER_URI')

# Properly escape the username and password
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)


MONGO_URI = f"mongodb+srv://{escaped_username}:{escaped_password}" + "@" + f"{host}"



client = MongoClient(MONGO_URI)

db = client['Sign_Up_Form']
collection = db['Profile_Information']


@app.route("/signup", methods=["POST"])
def signup():
    data_byte_str = request.data
    data_string = data_byte_str.decode('utf-8')
    data = json.loads(data_string)
    password = data.get('password')
    confirm_password = data.get('confirm password')
    print(data)
    if password == confirm_password:
        data.pop("confirm password")
        collection.insert_one(data)
        print("data added to the db successfully")
    
    return "Data Added successfully"


@app.route("/view")
def view():
    projection = { "username": 1, "email": 1, "password":1, "_id": 0 }
    data = collection.find({}, projection)

    lista = [profile for profile in data]
    print(lista)
   
    
    return dict(data=lista)



@app.route("/second/")
def second():
    return "This the second function"


@app.route("/api/<name>/")
def name(name):
    return f"My name is {name}"



@app.route("/api/add/<a>/<b>")
def add_function(a,b):
    print(f"a and b is {a} , {b}")
    dicta = {"Sum of two numbers": int(a)+int(b)}
    return dicta


@app.route("/details/")
def names():
    # http://127.0.0.1:5000/details/?name=pranav&age=30
    name = request.values.get('name')
    age = request.values.get('age')

    result = {"name": name, "age":age}
    return result




if __name__ == '__main___':
    app.run(host='0.0.0.0', port=9000, debug=True)
