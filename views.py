from flask import request, jsonify
from marshmallow import ValidationError
from flask.views import MethodView
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
from passlib.hash import bcrypt
from datetime import timedelta

from app import db
from models import User
from services import UserService, PostService, CommentService, CategoryService
from schemas import UserSchema, RegisterSchema, LoginSchema, CategorySchema, PostSchema, CommentSchema
from decorators import role_required

# USUARIOS
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
        return jsonify([u.to_dict() for u in users]), 200

class UserDetail(MethodView):
    @jwt_required()
    def get(self, id):
        """El propio usuario o admin pueden ver el perfil"""
        claims = get_jwt()
        current_id = claims.get("id")
        role = claims.get("role")

        if role != "admin" and current_id != id:
            return jsonify({"error": "No autorizado"}), 403

        user = UserService.get_user_by_id(id)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify(user.to_dict()), 200

    @jwt_required()
    @role_required("admin")
    def delete(self, id):
        """Solo admin puede desactivar usuarios"""
        result = UserService.deactivate_user(id)
        if not result:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"msg": "Usuario desactivado"}), 200

    @jwt_required()
    @role_required("admin")
    def patch(self, id):
        """Solo admin puede cambiar roles"""
        data = request.get_json()
        new_role = data.get("role")

        if not new_role:
            return jsonify({"error": "El campo 'role' es obligatorio"}), 400

        result = UserService.change_role(id, new_role)
        if not result:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"msg": f"Rol actualizado a '{new_role}'"}), 200

# POSTS
class Post(MethodView):
    def get(self):
        posts = PostService.list_posts()
        return jsonify([p.to_dict() for p in posts]), 200

    @jwt_required()
    def post(self):
        identity = get_jwt()
        user_id = identity.get("id")
        data = request.get_json()

        try:
            validated = PostSchema().load(data)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        post = PostService.create_post(
            title=validated["title"],
            content=validated["content"],
            user_id=user_id,
            category_id=validated.get("category_id")
        )
        return jsonify({"msg": "Post creado", "id": post.id}), 201

class PostDetail(MethodView):
    def get(self, id):
        post = PostService.get_post(id)
        if not post:
            return jsonify({"error": "Post no encontrado"}), 404
        return jsonify(post.to_dict()), 200

    @jwt_required()
    def put(self, id):
        claims = get_jwt()
        user_id = claims.get("id")
        role = claims.get("role")

        post = PostService.get_post(id)
        if not post:
            return jsonify({"error": "Post no encontrado"}), 404

        data = request.get_json()
        result = PostService.update_post(
            post,
            title=data.get("title", post.title),
            content=data.get("content", post.content),
            user_id=user_id,
            role=role
        )

        if result is False:
            return jsonify({"error": "No tienes permiso para editar este post"}), 403

        return jsonify({"msg": "Post actualizado"}), 200

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        user_id = claims.get("id")
        role = claims.get("role")

        post = PostService.get_post(id)
        if not post:
            return jsonify({"error": "Post no encontrado"}), 404

        result = PostService.delete_post(post, user_id, role)
        if result is False:
            return jsonify({"error": "No tienes permiso para eliminar este post"}), 403

        return jsonify({"msg": "Post eliminado"}), 200

# COMENTARIOS
class Comment(MethodView):
    def get(self, post_id):
        comments = CommentService.list_comments(post_id)
        return jsonify([c.to_dict() for c in comments]), 200

    @jwt_required()
    def post(self, post_id):
        claims = get_jwt()
        user_id = claims.get("id")

        data = request.get_json()
        try:
            validated = CommentSchema().load(data)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        comment = CommentService.create_comment(
            post_id=post_id,
            user_id=user_id,
            content=validated["content"]
        )
        return jsonify({"msg": "Comentario creado", "id": comment.id}), 201

class CommentDetail(MethodView):
    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        user_id = claims.get("id")
        role = claims.get("role")

        result = CommentService.delete_comment(id, user_id, role)

        if result is None:
            return jsonify({"error": "Comentario no encontrado"}), 404
        if result is False:
            return jsonify({"error": "No tienes permiso para eliminar este comentario"}), 403

        return jsonify({"msg": "Comentario eliminado"}), 200

# CATEGORÍAS
class Category(MethodView):
    def get(self):
        categories = CategoryService.list_categories()
        return jsonify([c.to_dict() for c in categories]), 200

    @jwt_required()
    @role_required("admin", "moderator")
    def post(self):
        data = request.get_json()
        validated = CategorySchema().load(data)
        cat = CategoryService.create_category(validated["name"])
        return jsonify({"msg": "Categoría creada", "id": cat.id}), 201

class CategoryDetail(MethodView):
    def get(self, id):
        cat = CategoryService.get_category(id)
        if not cat:
            return jsonify({"error": "Categoría no encontrada"}), 404
        return jsonify(cat.to_dict()), 200

    @jwt_required()
    @role_required("admin", "moderator")
    def put(self, id):
        data = request.get_json()
        validated = CategorySchema().load(data)
        cat = CategoryService.update_category(id, validated["name"])
        if not cat:
            return jsonify({"error": "Categoría no encontrada"}), 404
        return jsonify({"msg": "Categoría actualizada"}), 200

    @jwt_required()
    @role_required("admin")
    def delete(self, id):
        result = CategoryService.delete_category(id)
        if not result:
            return jsonify({"error": "Categoría no encontrada"}), 404
        return jsonify({"msg": "Categoría eliminada"}), 200

# LOGIN
class AuthLogin(MethodView):
    def post(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Faltan datos"}), 400

        try:
            validated_data = LoginSchema().load(data)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        user = User.query.filter_by(email=validated_data["email"]).first()
        if not user or not user.credential:
            return jsonify({"error": "Credenciales inválidas"}), 401

        if not bcrypt.verify(validated_data["password"], user.credential.password_hash):
            return jsonify({"error": "Credenciales inválidas"}), 401

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "id": user.id,
                "email": user.email,
                "role": user.credential.role,
            },
            expires_delta=timedelta(hours=24)
        )

        return jsonify({
            "msg": "Login exitoso",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.credential.role
            }
        }), 200