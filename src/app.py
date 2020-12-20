from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Task import Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

db = SQLAlchemy(app)        # Devuele instancia de base de datos
ma = Marshmallow(app)

taskInstancia = Task(db.Model)
# Esta clase sirve para definir y crear la tabla en la base de datos
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, title, description):
        self.title = title
        self.description = description
db.create_all()                             # Lee toda la clase y procede a crear la tabla

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    nombre = db.Column(db.String(25))
    apellido = db.Column(db.String(25))
    direccion = db.Column(db.String(30))

    def __init__(self, nombre, apellido, direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
db.create_all()                             # Lee toda la clase y procede a crear la tabla

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()                             # Obtiene un registro que cumpla con los parametros del esquema
tasks_schema = TaskSchema(many=True)                # Obtiene multiples registros que cumpla con los parametros del esquema

class PersonaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'apellido', 'direccion')

persona_schema = PersonaSchema()
personas_schema = PersonaSchema(many=True) 

# Permite Crear tareas
@app.route('/tasks', methods=['POST'])
def createTask():
    print(request.json)
    title = request.json['title']
    description = request.json['description']

    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

# Permite Listar todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()                    # Obtiene toda la información de la tabla
    result = tasks_schema.dump(all_tasks)           # obtiene los datos de la base de datos
    return jsonify(result) 

# Permite Listar todas las Personas
@app.route('/personas', methods=['GET'])
def get_persona():
    all_personas = Persona.query.all()                    # Obtiene toda la información de la tabla
    result = personas_schema.dump(all_personas)           # obtiene los datos de la base de datos
    return jsonify(result) 

# Permite Listar una única tarea
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

# Permite Listar una única persona
@app.route('/persona/<id>', methods=['GET'])
def get_task(id):
    task = Persona.query.get(id)
    return persona_schema.jsonify(task)

# Permite Actualizar una tarea especifica
@app.route('/tasks/<id>', methods=['PUT'])
def task_update(id):
    task = Task.query.get(id)   
    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.desciption = description
    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)

# Permite Eliminar una tarea especifica
@app.route('/tasks/<id>', methods=['DELETE'])
def task_delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)


if __name__ == "__main__":
    app.run(debug=True)



