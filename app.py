from flask import Flask, g, request, jsonify, session
from flask_login import LoginManager
import sqlite3

from user import User # User class for user table definition
import db_interface_users # methods for CRUD in users_db

app =  Flask(__name__)
app.secrectkey = b'\x9dd\x92\x03GLS\x10>hk\xd1\x9a\xa49\xf5'

login_manager = LoginManager()
login_manager.init_app(app)

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
            user = User(request.form["first_name"],request.form["last_name"],request.form["username"],request.form["password"]) # request has form property to access form data with the input being
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
            print("KeyError occurred")
            return "KeyError"
   
@app.route("/users")
def get_all_users():
    users = db_interface_users.get_all_users(get_db())
    usersJson = jsonify(users)

    return usersJson

@app.route("/")
def home_page():
    return "Hello Jessi"
    
if __name__ == "__main__":
    db_interface_users.create_users_table() # create database
    #db_interface_users.drop_table("users")
    app.run(port=7000)