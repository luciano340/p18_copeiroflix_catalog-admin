from uuid import UUID
from src.core.category.application.category_repository_interface import CategoryRepositoryInterface
from src.core.category.domain.category import Category

class InMemoryCategoryRepository(CategoryRepositoryInterface):
    def __init__(self, categories=None) -> None:
        self.categories = categories or []
    
    def save(self, category: Category) -> None:
        self.categories.append(category)
    
    def get_by_id(self, id: UUID) -> Category | None:
        for c in self.categories:
            if c.id == id:
                return c
        return None

    def delete_by_id(self, id) -> None:
        for n, i in enumerate(self.categories):
            if i.id == id:
                self.categories.pop(n)
            