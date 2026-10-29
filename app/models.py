from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    contrasena_hash = db.Column(db.String(200), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    
    # Relación: un usuario puede tener muchos anuncios
    anuncios = db.relationship('Anuncio', backref='autor', lazy=True, cascade='all, delete-orphan')
    
    @property
    def contrasena(self):
        raise AttributeError('contraseña no es un atributo legible')
    
    @contrasena.setter
    def contrasena(self, contrasena):
        self.contrasena_hash = generate_password_hash(contrasena)
    
    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.contrasena_hash, contrasena)
    
    def __repr__(self):
        return f'<Usuario {self.nombre}>'

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    
    # Relación: una categoría puede tener muchos anuncios
    anuncios = db.relationship('Anuncio', backref='categoria', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Categoria {self.nombre}>'

class Anuncio(db.Model):
    __tablename__ = 'anuncios'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Claves foráneas
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    
    def __repr__(self):
        return f'<Anuncio {self.titulo}>'