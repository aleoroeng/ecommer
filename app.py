from flask import Flask, g, request, jsonify
import db_interface_users # methods for CRUD in users_db
import sqlite3

app =  Flask(__name__)

STATUS_OK = 200

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
        print(request.form["name"])
        user = {"name": request.form["name"]} # request has form property to access form data with the input beign 
        
        db_interface_users.add_user_to_usersdb(user, get_db())
        return request.form["name"]

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
    app.run(port=7000)