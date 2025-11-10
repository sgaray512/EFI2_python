from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db
from views import (
    User,
    UserDetail,
    UserRegister,
    AuthLogin,
    Post,
    PostDetail,
    Comment,
    CommentDetail,
    Category,
    CategoryDetail
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///miniblog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "cualquiercosa"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

db.init_app(app)
jwt = JWTManager(app)

# Usuarios
app.add_url_rule(
    "/api/users",
    view_func=User.as_view("users_api"),
    methods=["GET"]
)

app.add_url_rule(
    "/api/users/<int:id>",
    view_func=UserDetail.as_view("user_detail_api"),
    methods=["GET", "PUT", "PATCH", "DELETE"]
)

# Autenticación
app.add_url_rule(
    "/api/register",
    view_func=UserRegister.as_view("register_api"),
    methods=["POST"]
)

app.add_url_rule(
    "/api/login",
    view_func=AuthLogin.as_view("login_api"),
    methods=["POST"]
)

# Posts
app.add_url_rule(
    "/api/posts",
    view_func=Post.as_view("post_list_api"),
    methods=["GET", "POST"]
)

app.add_url_rule(
    "/api/posts/<int:id>",
    view_func=PostDetail.as_view("post_detail_api"),
    methods=["GET", "PUT", "PATCH", "DELETE"]
)

# Comentarios
app.add_url_rule(
    "/api/comments",
    view_func=Comment.as_view("comment_list_api"),
    methods=["GET", "POST"]
)

app.add_url_rule(
    "/api/comments/<int:id>",
    view_func=CommentDetail.as_view("comment_detail_api"),
    methods=["GET", "DELETE"]
)

# Categorías
app.add_url_rule(
    "/api/categories",
    view_func=Category.as_view("category_list_api"),
    methods=["GET", "POST"]
)

app.add_url_rule(
    "/api/categories/<int:id>",
    view_func=CategoryDetail.as_view("category_detail_api"),
    methods=["GET", "PUT", "DELETE"]
)

@app.route('/')
def index():
    return {
        "status": "OK",
        "message": "API Miniblog funcionando correctamente"
    }

# ERRORES
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)