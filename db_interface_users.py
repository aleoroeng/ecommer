import sqlite3

def create_users_table():
    connection = sqlite3.connect("users_db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, username TEXT, password TEXT)")

    connection.commit() #after a query connection.commit() must be called to persist changes
    connection.close()

def drop_table(table_name):
    connection = sqlite3.connect("users_db")
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE {table_name}")

    connection.commit() #after a query connection.commit() must be called to persist changes
    connection.close()

def connect_to_usersdb():
    connection = sqlite3.connect("users_db")
    return connection

def add_user(user_dict, connection):
    cursor = connection.cursor()
    cursor.execute(''' 
        INSERT INTO users (first_name, last_name, username, password) VALUES(:first_name,:last_name,:username,:password)  
    ''', user_dict)
    connection.commit()
    connection.close()

def is_user_in_db(user_dict, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=:id", user_dict)
    user_fetched = cursor.fetchone()
    connection.close()
    return False if user == None else True

def get_all_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    
    users = cursor.fetchall()
    connection.close()
    return users