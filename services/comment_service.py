from repositories.comment_repository import CommentRepository

class CommentService:
    @staticmethod
    def list_comments(post_id: int):
        comments = CommentRepository.get_all()
        return [c for c in comments if c.post_id == post_id]

    @staticmethod
    def create_comment(post_id: int, user_id: int, content: str):
        if not content:
            raise ValueError("El comentario no puede estar vacío")
        return CommentRepository.create_comment(user_id, post_id, content)

    @staticmethod
    def delete_comment(comment_id: int, user_id: int, role: str):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comentario no encontrado")

        if role not in ["admin", "moderator"] and comment.user_id != user_id:
            raise PermissionError("No tienes permiso para eliminar este comentario")

        CommentRepository.delete(comment)
        return comment