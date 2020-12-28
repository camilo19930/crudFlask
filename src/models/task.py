from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, title, description):
        self.title = title
        self.description = description
# db.create_all()                             # Lee toda la clase y procede a crear la tabla