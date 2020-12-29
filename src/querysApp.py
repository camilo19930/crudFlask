from flask_sqlalchemy import SQLAlchemy
from models.task import Task

db = SQLAlchemy()

class QuerysApp():

    def craete_task(self):
        db.session.add(self)
        db.session.commit()

    def get_task_all():
        return Task.query.all()
