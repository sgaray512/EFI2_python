from app import db
from models import Comment

class CommentRepository:
    @staticmethod
    def get_all():
        return Comment.query.filter_by(is_visible=True).all()

    @staticmethod
    def get_by_id(comment_id: int):
        return Comment.query.get(comment_id)

    @staticmethod
    def create_comment(user_id: int, post_id: int, content: str):
        comment = Comment(
            user_id=user_id,
            post_id=post_id,
            content=content,
            is_visible=True
        )
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def delete(comment: Comment):
        db.session.delete(comment)
        db.session.commit()