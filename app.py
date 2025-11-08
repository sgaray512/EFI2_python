from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    current_user,
    LoginManager,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)

app.secret_key = "cualquiercosa"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://garay:santiago@localhost/miniblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import db, Usuario, Entrada, Comentario, Categoria

db.init_app(app)
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nombre_usuario = request.form["username"]
        contraseña = request.form["password"]

        user = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if user and check_password_hash(user.contraseña, contraseña):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Usuario o contraseña incorrectos", "error")

    return render_template('auth/login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nombre_usuario = request.form["username"]
        correo = request.form["email"]
        contraseña = request.form["password"]

        user = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if user:
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('register'))
        
        # Hashear contraseña
        password_hash = generate_password_hash(
            contraseña,
            method='pbkdf2'
        )
        
        # Crear nuevo usuario
        new_user = Usuario(
            nombre_usuario=nombre_usuario,
            correo=correo,
            contraseña=password_hash
        )

        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado con éxito', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    entradas = Entrada.query.order_by(Entrada.fecha_creacion.desc()).all()
    return render_template('posts.html', entradas=entradas)

@app.route('/entrada/<int:id>', methods=['GET', 'POST'])
def ver_entrada(id):
    entrada = Entrada.query.get_or_404(id)

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("Debes iniciar sesión para comentar", "error")
            return redirect(url_for('login'))
        
        texto = request.form['texto']
        nuevo_comentario = Comentario(
            texto=texto,
            autor_id=current_user.id,
            entrada_id=entrada.id
        )
        db.session.add(nuevo_comentario)
        db.session.commit()
        return redirect(url_for('ver_entrada', id=id))

    return render_template('post.html', entrada=entrada)


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        categoria_ids = request.form.getlist('categorias')

        nueva_entrada = Entrada(
            titulo=titulo,
            contenido=contenido,
            autor_id=current_user.id
        )

        for cat_id in categoria_ids:
            categoria = Categoria.query.get(int(cat_id))
            if categoria:
                nueva_entrada.categorias.append(categoria)

        db.session.add(nueva_entrada)
        db.session.commit()
        flash('Post creado con éxito', 'success')
        return redirect(url_for('index'))

    categorias = Categoria.query.all()
    return render_template('create_post.html', categorias=categorias)

@app.context_processor
def inject_categorias():
    categorias = Categoria.query.all()
    return dict(categorias=categorias)

if __name__ == '__main__':
    app.run(debug=True)