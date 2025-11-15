from app import db
from models import Post
from sqlalchemy import func

class PostRepository:
    @staticmethod
    def get_all():
        return Post.query.all()

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
    def update(post: Post, title: str, content: str, category_id: int = None):
        post.title = title
        post.content = content
        post.category_id = category_id if category_id is not None else post.category_id
        post.updated_at = func.now()

        db.session.commit()
        return post

    @staticmethod
    def delete(post: Post):
        db.session.delete(post)
        db.session.commit()

    @staticmethod
    def soft_delete(post: Post):
        post.is_published = False
        post.updated_at = func.now()
        db.session.commit()