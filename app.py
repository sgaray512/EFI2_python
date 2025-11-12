from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from datetime import timedelta
from flask_cors import CORS
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

# Configuraciones
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///miniblog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "cualquiercosa"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# USUARIOS
app.add_url_rule(
    "/api/users",
    view_func=User.as_view("users_api"),
    methods=["GET"]
)

app.add_url_rule(
    "/api/users/<int:id>",
    view_func=UserDetail.as_view("user_detail_api"),
    methods=["GET", "PATCH", "DELETE"]
)

# Registro y login
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

# POSTS
app.add_url_rule(
    "/api/posts",
    view_func=Post.as_view("post_list_api"),
    methods=["GET", "POST"]
)

app.add_url_rule(
    "/api/posts/<int:id>",
    view_func=PostDetail.as_view("post_detail_api"),
    methods=["GET", "PUT", "DELETE"]
)

# COMENTARIOS
app.add_url_rule(
    "/api/posts/<int:post_id>/comments",
    view_func=Comment.as_view("post_comments_api"),
    methods=["GET", "POST"]
)

# DELETE individual
app.add_url_rule(
    "/api/comments/<int:id>",
    view_func=CommentDetail.as_view("comment_detail_api"),
    methods=["DELETE"]
)

# CATEGORÍAS
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

# HOME y ERRORES
@app.route('/')
def index():
    return jsonify({
        "status": "OK",
        "message": "API Miniblog funcionando correctamente"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

#  MAIN
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)