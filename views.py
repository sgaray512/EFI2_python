from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import UserService
from services.post_service import PostService
from services.comment_service import CommentService
from services.category_service import CategoryService
from decorators import role_required

class UserRegister(MethodView):
    def post(self):
        data = request.get_json()
        try:
            user = UserService.register_user(
                name=data["name"],
                email=data["email"],
                password=data["password"],
                role=data.get("role", "user")
            )
            return jsonify({"msg": "Usuario registrado", "id": user.id}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400


class User(MethodView):
    @jwt_required()
    @role_required("admin")
    def get(self):
        users = UserService.list_users()
        return jsonify([u.to_dict() for u in users])

class UserDetail(MethodView):
    @jwt_required()
    @role_required("admin")
    def delete(self, id):
        result = UserService.deactivate_user(id)
        if not result:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"msg": "Usuario desactivado"}), 200

class Post(MethodView):
    def get(self):
        posts = PostService.list_posts()
        return jsonify([p.to_dict() for p in posts])

    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        data = request.get_json()
        try:
            post = PostService.create_post(
                title=data["title"],
                content=data["content"],
                user_id=identity["id"],
                category_id=data.get("category_id")
            )
            return jsonify({"msg": "Post creado", "id": post.id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

class PostDetail(MethodView):
    def get(self, id):
        post = PostService.get_post(id)
        if not post:
            return jsonify({"error": "Post no encontrado"}), 404
        return jsonify(post.to_dict())

    @jwt_required()
    def delete(self, id):
        identity = get_jwt_identity()
        post = PostService.get_post(id)
        if not post:
            return jsonify({"error": "Post no encontrado"}), 404

        try:
            PostService.delete_post(post, identity["id"], identity["role"])
            return jsonify({"msg": "Post eliminado"}), 200
        except PermissionError as e:
            return jsonify({"error": str(e)}), 403

class Comment(MethodView):
    def get(self):
        comments = CommentService.list_comments()
        return jsonify([c.to_dict() for c in comments])

    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        data = request.get_json()
        comment = CommentService.create_comment(
            user_id=identity["id"],
            post_id=data["post_id"],
            content=data["content"]
        )
        return jsonify({"msg": "Comentario creado", "id": comment.id}), 201

class CommentDetail(MethodView):
    @jwt_required()
    def delete(self, id):
        identity = get_jwt_identity()
        try:
            CommentService.delete_comment(id, identity["id"], identity["role"])
            return jsonify({"msg": "Comentario eliminado"}), 200
        except PermissionError as e:
            return jsonify({"error": str(e)}), 403
        except ValueError:
            return jsonify({"error": "Comentario no encontrado"}), 404

class Category(MethodView):
    def get(self):
        categories = CategoryService.list_categories()
        return jsonify([c.to_dict() for c in categories])

    @jwt_required()
    @role_required("admin", "moderator")
    def post(self):
        data = request.get_json()
        cat = CategoryService.create_category(data["name"])
        return jsonify({"msg": "Categoría creada", "id": cat.id}), 201

class CategoryDetail(MethodView):
    def get(self, id):
        cat = CategoryService.get_category(id)
        if not cat:
            return jsonify({"error": "Categoría no encontrada"}), 404
        return jsonify(cat.to_dict())

    @jwt_required()
    @role_required("admin", "moderator")
    def put(self, id):
        data = request.get_json()
        cat = CategoryService.update_category(id, data["name"])
        if not cat:
            return jsonify({"error": "Categoría no encontrada"}), 404
        return jsonify({"msg": "Categoría actualizada"})

    @jwt_required()
    @role_required("admin", "moderator")
    def delete(self, id):
        result = CategoryService.delete_category(id)
        if not result:
            return jsonify({"error": "Categoría no encontrada"}), 404
        return jsonify({"msg": "Categoría eliminada"})