class User:
    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    def __str__(self):
        return f"first name: {self.first_name}, last name: {self.last_name}, username: {self.username}, password: {self.password}"