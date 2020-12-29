from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models.task import Task
from models.personas import Persona
from models.usuario import Usuario
from models.usuario import User
from schema.schemaApp import TaskSchema
from schema.schemaApp import PersonaSchema
from schema.schemaApp import UsuarioShema
from flask_jwt import JWT, jwt_required, current_identity, timedelta
from werkzeug.security import safe_str_cmp
from querysApp import QuerysApp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(
    seconds=600)  # tiempo de expiración del token

db = SQLAlchemy(app)        # Devuele instancia de base de datos
# Lee toda la clase y procede a crear la tabla
db.create_all()
# Obtiene un registro que cumpla con los parametros del esquema
task_schema = TaskSchema()
# Obtiene multiples registros que cumpla con los parametros del esquema
tasks_schema = TaskSchema(many=True)
persona_schema = PersonaSchema()
personas_schema = PersonaSchema(many=True)
usuario_schema = UsuarioShema()
usuarios_schema = UsuarioShema(many=True)
username_table = {}
userid_table = {}

# TASK
# Permite Crear tareas


@app.route('/tasks', methods=['POST'])
def createTask():
    title = request.json['title']
    description = request.json['description']
    new_task = Task(title, description)
    QuerysApp.craete_task(new_task)
    return task_schema.jsonify(new_task)

# Permite Listar todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Obtiene toda la información de la tabla
    all_tasks = QuerysApp.get_task_all()
    # obtiene los datos de la base de datos
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

# Permite Listar una única tarea
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

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

# PERSONAS

# Permite Crear tareas
@app.route('/personas', methods=['POST'])
def createPersonas():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    direccion = request.json['direccion']

    new_persona = Persona(nombre, apellido, direccion)
    db.session.add(new_persona)
    db.session.commit()
    return task_schema.jsonify(new_persona)

# Permite Listar todas las Personas
@app.route('/personas', methods=['GET'])
def get_personas():
    # Obtiene toda la información de la tabla
    all_personas = Persona.query.all()
    # obtiene los datos de la base de datos
    result = personas_schema.dump(all_personas)
    return jsonify(result)

# Permite Listar una única persona
@app.route('/persona/<id>', methods=['GET'])
def get_persona(id):
    task = Persona.query.get(id)
    return persona_schema.jsonify(task)

# USUARIOS
# Permite Crear usuarios
@app.route('/usuarios', methods=['POST'])
def createUser():
    username = request.json['username']
    password = request.json['password']

    new_user = Usuario(username, password)
    db.session.add(new_user)
    db.session.commit()
    return usuario_schema.jsonify(new_user)

# permite listar todos los usuario
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    # Obtiene toda la información de la tabla
    all_usuarios = Usuario.query.all()
    # obtiene los datos de la base de datos
    result = usuarios_schema.dump(all_usuarios)
    return jsonify(result)

# Permite Listar una único usuario
@app.route('/usuario/<id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    return usuario_schema.jsonify(usuario)

# AUTENTICATIÓN

def lista_usuarios():
    # Obtiene toda la información de la tabla
    all_usuarios = Usuario.query.all()
    # obtiene los datos de la base de datos
    result = usuarios_schema.dump(all_usuarios)
    return result


def obtenerData():
    list_users = lista_usuarios()
    for elements in list_users:
        username_table[elements["username"]] = User(
            elements["id"], elements["username"], elements["password"])
        userid_table[elements["id"]] = User(
            elements["id"], elements["username"], elements["password"])


def authenticate(username, password):
    obtenerData()
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


jwt = JWT(app, authenticate, identity)
if __name__ == "__main__":
    app.run(debug=True)
