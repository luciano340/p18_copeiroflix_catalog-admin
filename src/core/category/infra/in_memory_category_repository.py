from src.core.category.application.category_repository_interface import CategoryRepositoryInterface
from src.core.category.domain.category import Category

class InMemoryCategoryRepository(CategoryRepositoryInterface):
    def __init__(self, categories=None) -> None:
        self.categories = categories or []
    
    def save(self, category: Category) -> None:
        self.categories.append(category)