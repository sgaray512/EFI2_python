from repositories.post_repository import PostRepository
from models import Post

class PostService:
    @staticmethod
    def list_published_posts():
        return PostRepository.get_all_published()

    @staticmethod
    def get_post_by_id(post_id: int):
        return PostRepository.get_by_id(post_id)

    @staticmethod
    def create_post(title: str, content: str, user_id: int, category_id: int = None):
        if not title or not content:
            raise ValueError("El título y el contenido son obligatorios")
        return PostRepository.create_post(title, content, user_id, category_id)

    @staticmethod
    def delete_post(post_id: int, current_user_id: int, current_role: str):
        post = PostRepository.get_by_id(post_id)
        if not post:
            raise ValueError("Post no encontrado")
        
        if current_role != "admin" and post.user_id != current_user_id:
            raise PermissionError("No tienes permiso para eliminar este post")

        PostRepository.delete(post)
        return post