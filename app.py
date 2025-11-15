from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

from models import db, User, Category, Post, Comment
from views import (
    User as UserView,
    UserDetail,
    UserRegister,
    AuthLogin,
    Post as PostView,
    PostDetail,
    Comment as CommentView,
    CommentDetail,
    Category as CategoryView,
    CategoryDetail
)
from schemas import UserSchema, RegisterSchema, LoginSchema, CategorySchema, PostSchema, CommentSchema

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///miniblog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "cualquiercosa"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

db.init_app(app)
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

with app.app_context():
    db.create_all()

# Rutas de usuarios
app.add_url_rule("/api/users", view_func=UserView.as_view("users_api"), methods=["GET"])
app.add_url_rule("/api/users/<int:id>", view_func=UserDetail.as_view("user_detail_api"), methods=["GET", "PATCH", "DELETE"])
app.add_url_rule("/api/register", view_func=UserRegister.as_view("register_api"), methods=["POST"])
app.add_url_rule("/api/login", view_func=AuthLogin.as_view("login_api"), methods=["POST"])

# Rutas de posts
app.add_url_rule("/api/posts", view_func=PostView.as_view("post_list_api"), methods=["GET", "POST"])
app.add_url_rule("/api/posts/<int:id>", view_func=PostDetail.as_view("post_detail_api"), methods=["GET", "PUT", "DELETE"])

# Rutas de comentarios
app.add_url_rule("/api/posts/<int:post_id>/comments", view_func=CommentView.as_view("post_comments_api"), methods=["GET", "POST"])
app.add_url_rule("/api/comments/<int:id>", view_func=CommentDetail.as_view("comment_detail_api"), methods=["DELETE"])


# Rutas de categorías
app.add_url_rule("/api/categories", view_func=CategoryView.as_view("category_list_api"), methods=["GET", "POST"])
app.add_url_rule("/api/categories/<int:id>", view_func=CategoryDetail.as_view("category_detail_api"), methods=["GET", "PUT", "DELETE"])

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

if __name__ == "__main__":
    app.run(debug=True)