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

1. Clonar este repositorio con SSH:
git clone git@github.com:sgaray512/EFI2_python.git
cd EFI2_python

2. Instalá las dependencias declaradas en requirements.txt y pyproject.toml:
uv pip install -r requirements.txt
uv init
uv sync

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
Recurso	            Método	            Ruta	                        Descripción										Rol
Usuarios	        GET	            /api/users	                Listar todos los usuarios								Admin
	                GET	            /api/users/<id>	            Obtener un usuario específico							Propio / Admin
					PATCH			/api/users/<id>				Cambiar rol												Admin
	                DELETE	        /api/users/<id>	            Desactivar usuario										Admin
Auth	            POST	        /api/register	            Registrar nuevo usuario
	                POST	        /api/login	                Iniciar sesión y obtener token JWT
Posts	            GET	            /api/posts	                Listar todos los posts publicados						Público
					GET				/api/posts/<id>				Ver un post específico									Público
	                POST	        /api/posts	                Crear nuevo post										User autenticado
					PUT				/api/posts/<id>				Editar post (propio o admin)							User/Admin
	                DELETE	        /api/posts/<id>	            Eliminar post propio o como admin						User/Admin
Comentarios	        GET	            /api/posts/<id>/comments	Listar comentarios de un post							Público
	                POST	        /api/posts/<id>/comments>	Crear comentario										User autenticado
	                DELETE	        /api/comments/<id>	        Eliminar comentario (propio, moderator o admin)			User/Mod/Admin
Categorías	        GET	            /api/categories	            Listar categorías										Público
	                POST	        /api/categories	            Crear categoría											Admin/Moderator
	                PUT	            /api/categories/<id>	    Editar categoría										Admin/Moderator
	                DELETE	        /api/categories/<id>	    Eliminar categoría										Admin

# Probar la API
Si tenés instalada la extensión REST Client en VS Code:
1. Abrí el archivo test_api.http
2. Verás botones como ▶ Send Request arriba de cada bloque de código.
3. Hacé clic para ejecutar cada petición directamente desde VS Code.
4. Las respuestas aparecerán en un panel lateral (JSON de la API).
5. El archivo incluye un flujo completo:
	Registrar usuarios (admin, moderator, user)
	Login y guardar token JWT automáticamente
	Crear categorías, posts y comentarios
	Probar permisos y eliminaciones

## Credenciales de prueba
Estas credenciales podés usarlas para probar los distintos roles:
Rol	                      Email	                Contraseña
Admin	            admin@example.com           admin123
Moderator           mod@example.com             mod123
User                user@example.com            user123

Llegado a este punto, estas credenciales se pueden probar desde Thunder Client perfectamente
Para instalar Thunder Client:
1. Ir a Extensions de Visual Studio Code
2. En el buscador escribir "Thunder Client" (su imagen es un rayo dentro de un circulo)
3. Instalarla
Luego abrir Thunder Client desde la barra lateral izquierda en Visual Studio, haciendo click en el icono del rayo
Creá una nueva request en Thunder Client:
Método: POST
URL: http://127.0.0.1:5000/api/login
Body → JSON:
{
  "email": "admin@example.com",
  "password": "admin123"
}
Hacé clic en Send.
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR..."
}
Copiá ese token (todo el texto largo)
Guardar el token para usar en las demás peticiones

En Thunder Client:
1. Andá a la pestaña Auth.
2. Elegí el tipo Bearer Token.
3. Pegá ahí el access_token que obtuviste.
De esa forma, todas las requests que requieran autenticación lo usarán automáticamente.

Probar endpoints protegidos
Por ejemplo, para listar usuarios (solo admin):
GET http://127.0.0.1:5000/api/users
Deberías obtener algo como:
[
  {
    "id": 1,
    "name": "Admin User",
    "email": "admin@example.com",
    "role": "admin",
    ...
  },
  ...
]

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