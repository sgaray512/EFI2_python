from marshmallow import Schema, fields, validate
from models import User, UserCredential, Post, Comment, Category

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    role = fields.Str(dump_only=True)  # se obtiene de UserCredential

class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(
        validate=validate.OneOf(["user", "moderator", "admin"]),
        load_default="user"
    )

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    is_published = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    category_id = fields.Int(allow_none=True)
    user_id = fields.Int(dump_only=True)
    author = fields.Nested(UserSchema, only=("id", "name"), dump_only=True)
    category = fields.Nested(CategorySchema, dump_only=True)

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    is_visible = fields.Bool(dump_only=True)
    post_id = fields.Int(required=True)
    user_id = fields.Int(dump_only=True)
    author = fields.Nested(UserSchema, only=("id", "name"), dump_only=True)