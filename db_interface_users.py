import sqlite3

def create_users_table():
    connection = sqlite3.connect("users_db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(name text)")

    connection.commit() #after a query connection.commit() must be called to persist changes
    connection.close()

def connect_to_usersdb():
    connection = sqlite3.connect("users_db")
    return connection

def add_user_to_usersdb(user, connection):
    cursor = connection.cursor()
    cursor.execute(''' 
        INSERT INTO users VALUES(:name)  
    ''', user)
    connection.commit()
    connection.close()

def is_user_in_db(name, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE name=:name", name)
    user = cursor.fetchone()
    connection.close()
    return False if user == None else True

def get_all_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    
    users = cursor.fetchall()
    connection.close()
    return users