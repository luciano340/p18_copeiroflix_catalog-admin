from abc import ABC, abstractmethod

from src.core.category.domain.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def save(self, category) -> Category:
        raise NotImplementedError
    
    def get_by_id(self, id) -> Category | None:
        raise NotImplementedError

    def delete_by_id(self,id) -> None:
        raise NotImplementedError