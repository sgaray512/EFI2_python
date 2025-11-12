from repositories.post_repository import PostRepository

class PostService:

    @staticmethod
    def list_posts():
        return PostRepository.get_all()

    @staticmethod
    def get_post(post_id: int):
        return PostRepository.get_by_id(post_id)

    @staticmethod
    def create_post(title: str, content: str, user_id: int, category_id: int = None):
        if not title or not content:
            raise ValueError("Título y contenido son obligatorios")

        return PostRepository.create_post(title, content, user_id, category_id)

    @staticmethod
    def update_post(post, title: str, content: str, user_id: int, role: str):
        if not post:
            return None
        
        if role == "user" and post.user_id != user_id:
            return False

        updated_post = PostRepository.update(post, title, content)
        return updated_post

    @staticmethod
    def delete_post(post, user_id: int, role: str):
        if not post:
            return None

        if role == "user" and post.user_id != user_id:
            return False
        
        PostRepository.delete(post)
        return True