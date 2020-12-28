from flask_marshmallow import Marshmallow
ma = Marshmallow()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

class PersonaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'apellido', 'direccion')

class UsuarioShema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')