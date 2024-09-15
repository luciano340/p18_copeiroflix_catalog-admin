from abc import ABC, abstractmethod
from uuid import UUID

from src.core.genre.domain.genre import Genre


class GenreRepositoryInterface(ABC):
    @abstractmethod
    def save(self, genre: Genre) -> Genre:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Genre | None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self,id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, genre: Genre) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self, order_by: str) -> list[Genre]:
        raise NotImplementedError