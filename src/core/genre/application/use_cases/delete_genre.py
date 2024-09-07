from dataclasses import dataclass
from uuid import UUID
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface

@dataclass
class DeleteGenreRequest:
    id: UUID


class DeleteGenre:
    def __init__(self, repository: GenreRepositoryInterface) -> None:
        self.repository = repository
    
    def execute(self, request: DeleteGenreRequest):
        genre = self.repository.get_by_id(id=request.id)

        if genre is None:
            raise GenreNotFound(f"Genre with id {request.id} not found for delete")
        
        self.repository.delete_by_id(id=request.id)

