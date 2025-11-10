from app import db
from models import Post

class PostRepository:
    @staticmethod
    def get_all_published():
        return Post.query.filter_by(is_published=True).all()

    @staticmethod
    def get_by_id(post_id: int):
        return Post.query.get(post_id)

    @staticmethod
    def create_post(title: str, content: str, user_id: int, category_id: int = None):
        post = Post(
            title=title,
            content=content,
            user_id=user_id,
            category_id=category_id,
            is_published=True
        )
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def delete(post: Post):
        db.session.delete(post)
        db.session.commit()