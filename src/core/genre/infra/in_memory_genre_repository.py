from uuid import UUID

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface


class InMemoryGenreRepository(GenreRepositoryInterface):
    def __init__(self, categories=None) -> None:
        self.categories = categories or []
    
    def save(self, genre: Genre) -> None:
        self.categories.append(genre)
    
    def get_by_id(self, id: UUID) -> Genre | None:
        for c in self.categories:
            if c.id == id:
                return c
        return None

    def delete_by_id(self, id: UUID) -> None:
        for n, i in enumerate(self.categories):
            if i.id == id:
                self.categories.pop(n)
    
    def update(self, genre: Genre) -> None:
        for n, i in enumerate(self.categories):
            if i.id == genre.id:
                self.categories[n] = genre

    def list(self) -> list[Genre]:
        return [c for c in self.categories]