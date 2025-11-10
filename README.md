# EFI2_python
# 📝 MiniBlog API

MiniBlog es una API REST construida con **Flask**, **SQLAlchemy** y **Marshmallow**, que permite gestionar usuarios, posts, comentarios y categorías, con autenticación mediante **JWT**.

---

## Requisitos previos

Asegurate de tener instalado:
- Python 3.11 o superior
Instalar Python:
a. Verificá si ya lo tenés:
python3 --version
b. Si no, instalalo:
sudo apt update
sudo apt install python3 python3-pip -y

- uv
Instalar uv:
a. Verificá si ya lo tenés:
uv --version
b. Si no, instalalo:
sudo snap install astral-uv --classic

## Instalación

1. Cloná este repositorio con SSH:
git clone git@github.com:sgaray512/EFI2_python.git
cd EFI2_python

2. Instalá las dependencias declaradas en requirements.txt:
uv pip install -r requirements.txt

3. Inicializá la base de datos si usás migraciones:
# Crear la base y migraciones
uv run flask db init
uv run flask db migrate -m "Inicial"
uv run flask db upgrade

# Cargar datos de prueba
uv run python seed.py

4. Ejecutá la aplicación:
uv run flask run --reload

## Autenticación y roles
El sistema usa JWT (JSON Web Tokens) con distintos roles de usuario:
Rol	                                Permisos
admin	            Acceso total (usuarios, posts, categorías, comentarios)
moderator	        Puede gestionar categorías y moderar comentarios
user	            Puede crear posts y comentarios propios

## Endpoints principales
Recurso	            Método	            Ruta	                        Descripción
Usuarios	        GET	            /api/users	                Listar todos los usuarios (admin)
	                GET	            /api/users/<id>	            Obtener un usuario específico
	                DELETE	        /api/users/<id>	            Desactivar usuario (admin)
Auth	            POST	        /api/register	            Registrar nuevo usuario
	                POST	        /api/login	                Iniciar sesión y obtener token JWT
Posts	            GET	            /api/posts	                Listar posts publicados
	                POST	        /api/posts	                Crear nuevo post (usuario autenticado)
	                DELETE	        /api/posts/<id>	            Eliminar post propio o como admin
Comentarios	        GET	            /api/comments/<post_id>	    Listar comentarios de un post
	                POST	        /api/comments/<post_id>	    Crear comentario (usuario autenticado)
	                DELETE	        /api/comments/<id>	        Eliminar comentario (propio o admin/mod)
Categorías	        GET	            /api/categories	            Listar categorías
	                POST	        /api/categories	            Crear categoría (admin/moderator)
	                PUT	            /api/categories/<id>	    Editar categoría (admin/moderator)
	                DELETE	        /api/categories/<id>	    Eliminar categoría (admin)

## Credenciales de prueba
Estas credenciales podés usarlas para probar los distintos roles:
Rol	                      Email	                Contraseña
Admin	            admin@example.com           admin123
Moderator           mod@example.com             mod123
User                user@example.com            user123

## Estructura del proyecto
EFI2_miniblog/
├── app.py
├── models.py
├── schemas.py
├── repositories/
│   ├── user_repository.py
│   ├── post_repository.py
│   ├── comment_repository.py
│   └── category_repository.py
├── services/
│   ├── user_service.py
│   ├── post_service.py
│   ├── comment_service.py
│   └── category_service.py
├── views.py
├── decorators.py
├── requirements.txt
├── test_api.http
└── README.md