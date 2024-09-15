from dataclasses import dataclass, field
from datetime import datetime
import os
from uuid import UUID
from src.core._shared.dto import ListOuputMeta
from src.core._shared.factory_pagination import CreateListPagination
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
    current_page: int = 1

@dataclass
class ResponseListGenre:
    data: list[GenreOutput]
    meta: ListOuputMeta = field(default_factory=ListOuputMeta)

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
        
        genres_page = CreateListPagination.configure_pagination(
            mapped_list=mapped_genres, 
            current_page=request.current_page
        )

        return ResponseListGenre(
            data=genres_page,
            meta=ListOuputMeta(
                current_page=request.current_page,
                page_size=os.environ.get("page_size", 5),
                total=len(mapped_genres)
            )
        )