from app import db
from models import Category

class CategoryRepository:
    @staticmethod
    def get_all():
        return Category.query.all()

    @staticmethod
    def get_by_id(category_id: int):
        return Category.query.get(category_id)

    @staticmethod
    def create(name: str):
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def update(category: Category, name: str):
        category.name = name
        db.session.commit()
        return category

    @staticmethod
    def delete(category: Category):
        db.session.delete(category)
        db.session.commit()