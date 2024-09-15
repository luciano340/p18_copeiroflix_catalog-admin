from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.core.genre.application.use_cases.exceptions import GenreOrderNotFound
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface
from django.core.exceptions import FieldError

@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories_id: set[UUID]
    created_date: datetime
    updated_date: datetime
    
@dataclass
class RequestListGenre:
    order_by: str = "name"

@dataclass
class ResponseListGenre:
    data: list[GenreOutput]

class ListGenre():
    def __init__(self, repository: GenreRepositoryInterface) -> None:
        self.repository = repository
    
    def execute(self, request: RequestListGenre):
        try:
            genres = self.repository.list(order_by=request.order_by)
        except FieldError:
            raise GenreOrderNotFound(f'Field {request.order_by} not found')

        mapped_genres = [
            GenreOutput(
                id=g.id,
                name=g.name,
                is_active=g.is_active,
                categories_id=g.categories,
                created_date=g.created_date,
                updated_date=g.updated_date
            ) for g in genres
        ]
        return ResponseListGenre(data=mapped_genres)