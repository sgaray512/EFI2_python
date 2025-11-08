from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

# Tabla auxiliar para relacion muchos-muchos
entrada_categoria = db.Table(
    'entrada_categoria',
    db.Column('entrada_id', db.Integer, db.ForeignKey('entrada.id'), primary_key=True),
    db.Column('categoria_id', db.Integer, db.ForeignKey('categoria.id'), primary_key=True)
)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    entradas = db.relationship('Entrada', backref='autor', lazy=True)
    comentarios = db.relationship('Comentario', backref='autor', lazy=True)

class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    comentarios = db.relationship('Comentario', backref='entrada', lazy=True)
    categorias = db.relationship(
        'Categoria',
        secondary=entrada_categoria,
        lazy='subquery',
        backref=db.backref('entradas', lazy=True)
    )

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrada.id'), nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)