from dataclasses import dataclass
from uuid import UUID
from src._shared.logger import get_logger
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository_interface import GenreRepositoryInterface

@dataclass
class DeleteGenreRequest:
    id: UUID


class DeleteGenre:
    def __init__(self, repository: GenreRepositoryInterface) -> None:
        self.repository = repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)}')
        
    def execute(self, request: DeleteGenreRequest):
        self.logger.info(f'Iniciando deleção do genero {request.id}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        genre = self.repository.get_by_id(id=request.id)

        if genre is None:
            self.logger.error(f"Não foi possível localizar o genero {request.id} para deleção")
            raise GenreNotFound(f"Genre with id {request.id} not found for delete")
        
        self.repository.delete_by_id(id=request.id)
        self.logger.info(f'Membro do elenco {request.id} deletado')

