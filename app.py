from flask import Flask, g, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
import sqlite3

from user import User # User class for user table definition
import db_interface_users # methods for CRUD in users_db

app =  Flask(__name__)
app.config["JWT_SECRET_KEY"] = "" #change to secure key at least 32 characters long
jwt = JWTManager(app)

app.secrectkey = b'\x9dd\x92\x03GLS\x10>hk\xd1\x9a\xa49\xf5'
bcrypt = Bcrypt(app)

STATUS_OK = 200

# 
def get_db():
    db = getattr(g, "_database", None) # g is the application context object
    if db is None:
        db = g._databse = db_interface_users.connect_to_usersdb()
        return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# ROUTES

@app.route("/user", methods=["GET","POST"])
def add_user():
    
    if request.method == "POST":
        try:
            hashed_password = bcrypt.generate_password_hash(request.form["password"])
            user = User(request.form["first_name"],request.form["last_name"],request.form["username"],hashed_password) # request has form property to access form data with the input being
            print(user)
            db_interface_users.add_user(user.__dict__, get_db())
            return "Success"
        except KeyError:
            return "KeyError"
    elif request.method == "GET":
        try:
            name = request.form["name"]
            name_sequence = {"name": name}
            is_user_in_db = db_interface_users.is_user_in_db(name_sequence, get_db())

            print(is_user_in_db)
            return str(is_user_in_db)
        except KeyError: # request.form["key"] throws KeyError if no parameter with said key is sent in request
            return "KeyError"
   
@app.route("/users")
def get_all_users():
    users = db_interface_users.get_all_users(get_db())

    for user in users:
        users_json = User(user[1],user[2],user[3],user[4])
    del users_json.password
    return users_json.to_json()

@app.route("/login", methods = ["POST", "GET"])
def home_page():

    if request.method == "POST":
        psswd_from_request = request.form["password"]
        username_from_request = request.form["username"]

        users = db_interface_users.get_all_users(get_db())
        
        for user in users:
            if bcrypt.check_password_hash(user[4],psswd_from_request) and user[3] == username_from_request:
                access_token = create_access_token(identity=username_from_request)
                return jsonify(access_token=access_token)

    return "Incorrect credentials"
    
if __name__ == "__main__":
    db_interface_users.create_users_table() # create database
    #db_interface_users.drop_table("users")
    app.run(port=7000)