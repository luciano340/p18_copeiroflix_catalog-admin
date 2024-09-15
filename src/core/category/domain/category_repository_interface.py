from abc import ABC, abstractmethod

from src.core.category.domain.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def save(self, category) -> Category:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self,id) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self, order_by) -> list[Category]:
        raise NotImplementedError