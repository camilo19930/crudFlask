from flask_sqlalchemy import SQLAlchemy
from models.task import Task

db = SQLAlchemy()

class QuerysApp():

    def craete_task(self):
        db.session.add(self)
        db.session.commit()

    def get_task_all():
        return Task.query.all()



    # def createTask():
    # title = request.json['title']
    # description = request.json['description']

    # new_task = Task(title, description)
    # db.session.add(new_task)
    # db.session.commit()
    # return task_schema.jsonify(new_task)