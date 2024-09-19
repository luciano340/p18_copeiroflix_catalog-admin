from dataclasses import dataclass
from uuid import UUID
from src._shared.logger import get_logger
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.genre.application.use_cases.exceptions import GenreNotFound, RelatedCategoriesInvalid, RelatedCategoriesNotFound
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface


@dataclass
class UpdateGenreRequest:
    id: UUID
    name: str | None = None
    categories_id: set[UUID] | None = None
    is_active: bool | None = None
    
class UpdateGenre:
    def __init__(self, repository: GenreRepositoryInterface, categoryRepository: CategoryRepositoryInterface):
        self.repository = repository
        self.category_repository = categoryRepository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)} - {categoryRepository} - {type(categoryRepository)}')
        
    def execute(self, request: UpdateGenreRequest) -> None:
        self.logger.info(f'Iniciando update de genero {request.id}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        genre = self.repository.get_by_id(request.id)
        
        if genre is None:
            self.logger.error(f'Genero {request.id} não localizada para atualização')
            raise GenreNotFound(f"Genre with id {request.id} not found for update")
        
        if request.name is not None:
            genre.change_name(name=request.name)
        
        if request.categories_id is not None:
            genre.categories = set()
            for category_id in request.categories_id:
                try:
                    genre.add_caterogy(category_id)
                except ValueError as err:
                    raise RelatedCategoriesInvalid(err)
                
                category = self.category_repository.get_by_id(id=category_id)
                if category is None:
                    raise RelatedCategoriesNotFound(f"Category id {category_id} not found")

        if request.is_active is not None:
            if request.is_active is True:
                genre.activate()
            else:
                genre.deactivate()

        self.logger.debug(f'Informações da entidade genero que serão enviadas para atualização no banco {genre}')
        self.repository.update(genre)
        self.logger.info(f'Atualização da genero {request.id} finalizada')