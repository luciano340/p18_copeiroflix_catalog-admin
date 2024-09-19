from dataclasses import dataclass, field
import re
from uuid import UUID
from datetime import datetime

from src._shared.logger import get_logger
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface

@dataclass
class CreateGenreRequest:
    name: str
    categories_id: set[UUID] = field(default_factory=set)
    is_active: bool = True

@dataclass
class CreateGenreResponse:
    id: UUID

class CreateGenre:
    def __init__(self, repository: GenreRepositoryInterface ,category_repository: CategoryRepositoryInterface) -> CreateGenreResponse:
        self.repository = repository
        self.category_repository = category_repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)} - {category_repository} - {type(category_repository)}')
        
    def execute(self, request: CreateGenreRequest) -> CreateGenreResponse:
        self.logger.info(f'Iniciando de genero {request.name}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        categories_ids = {category.id for category in self.category_repository.list()}

        if not request.categories_id.issubset(categories_ids):
            self.logger.error(f'Não foi possível localizar a categoria vinculada ao genero {request.name} - {request.categories_id - categories_ids}')
            raise RelatedCategoriesNotFound(f"Categories ID not found: {request.categories_id - categories_ids}")

        try:
            genre = Genre(
                name=request.name,
                is_active=request.is_active,
                categories=request.categories_id
            )
        except ValueError as err:
            self.logger.error(f"Os argumentos repassados são inválidos {err}")
            raise InvalidGenre(err)
    
        self.repository.save(genre)
        self.logger.debug(f'Dados a serem persistidos {genre}')
        self.logger.info('Criação do genero finalizada')
        return CreateGenreResponse(
            id=genre.id
        )