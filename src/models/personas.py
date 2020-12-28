from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    nombre = db.Column(db.String(25))
    apellido = db.Column(db.String(25))
    direccion = db.Column(db.String(30))

    def __init__(self, nombre, apellido, direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion