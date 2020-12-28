from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(70))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __str__(self):
        return "Usuario(id='%s')" % self.id

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "Usuario(id='%s')" % self.id


