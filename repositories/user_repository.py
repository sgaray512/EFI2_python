from app import db
from models import User, UserCredential

class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id: int):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(name: str, email: str):
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.flush()
        return user

    @staticmethod
    def create_credential(user_id: int, password_hash: str, role: str):
        cred = UserCredential(user_id=user_id, password_hash=password_hash, role=role)
        db.session.add(cred)
        return cred

    @staticmethod
    def deactivate_user(user: User):
        user.is_active = False
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()