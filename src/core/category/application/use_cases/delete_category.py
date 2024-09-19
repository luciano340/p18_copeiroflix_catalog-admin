from dataclasses import dataclass
from uuid import UUID
from src._shared.logger import get_logger
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.use_cases.exceptions import CategoryNotFound

@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: CategoryRepositoryInterface) -> None:
        self.repository = repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)}')
         
    def execute(self, request: DeleteCategoryRequest):
        self.logger.info(f'Iniciando deleção de categoria {request.id}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        category = self.repository.get_by_id(id=request.id)

        if category is None:
            self.logger.error(f'Categoria {request.id} não localizada')
            raise CategoryNotFound(f"Category with id {request.id} not found for delete")
        
        self.repository.delete_by_id(id=request.id)
        self.logger.info(f'Categoria {request.id} deletada com sucesso!')

