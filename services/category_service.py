from repositories.category_repository import CategoryRepository

class CategoryService:
    @staticmethod
    def list_categories():
        return CategoryRepository.get_all()

    @staticmethod
    def get_category(category_id: int):
        return CategoryRepository.get_by_id(category_id)

    @staticmethod
    def create_category(name: str):
        if not name:
            raise ValueError("El nombre de la categoría es obligatorio")
        return CategoryRepository.create(name)

    @staticmethod
    def update_category(category_id: int, name: str):
        cat = CategoryRepository.get_by_id(category_id)
        if not cat:
            return None
        return CategoryRepository.update(cat, name)

    @staticmethod
    def delete_category(category_id: int):
        cat = CategoryRepository.get_by_id(category_id)
        if not cat:
            return None
        CategoryRepository.delete(cat)
        return True