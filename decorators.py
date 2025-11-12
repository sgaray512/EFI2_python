from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify

def role_required(*allowed_roles: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if not role or role not in allowed_roles:
                return jsonify({"error": "Acceso denegado"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator