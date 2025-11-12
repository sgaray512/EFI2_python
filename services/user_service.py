from passlib.hash import bcrypt
from repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def list_users():
        return UserRepository.get_all()

    @staticmethod
    def get_user_by_id(user_id: int):
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def register_user(name: str, email: str, password: str, role: str = "user"):
        if UserRepository.get_by_email(email):
            raise ValueError("El email ya está en uso")
        
        new_user = UserRepository.create_user(name, email)
        password_hash = bcrypt.hash(password)
        UserRepository.create_credential(new_user.id, password_hash, role)
        UserRepository.save()
        return new_user

    @staticmethod
    def deactivate_user(user_id: int):
        user = UserRepository.get_by_id(user_id)
        if not user:
            return None
        UserRepository.deactivate_user(user)
        return user