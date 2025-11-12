from repositories.comment_repository import CommentRepository

class CommentService:
    @staticmethod
    def list_comments(post_id: int):
        return CommentRepository.get_by_post_id(post_id)

    @staticmethod
    def create_comment(post_id: int, user_id: int, content: str):
        if not content:
            raise ValueError("El comentario no puede estar vacío")
        
        return CommentRepository.create_comment(
            user_id=user_id,
            post_id=post_id,
            content=content
        )

    @staticmethod
    def delete_comment(comment_id: int, user_id: int, role: str):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            return None

        if role == "user" and comment.user_id != user_id:
            return False

        CommentRepository.delete(comment)
        return True