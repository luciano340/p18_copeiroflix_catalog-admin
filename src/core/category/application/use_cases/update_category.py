from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src._shared.logger import get_logger
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.use_cases.exceptions import CategoryNotFound

@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    
class UpdateCategory:
    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)}')

    def execute(self, request: UpdateCategoryRequest) -> None:
        self.logger.info(f'Iniciando update de categoria {request.id}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        category = self.repository.get_by_id(request.id)
        
        if category is None:
            self.logger.error(f'Categoria {request.id} não localizada para atualização')
            raise CategoryNotFound(f"Category with id {request.id} not found for update")

        current_name = category.name
        current_description = category.description

        if request.name is not None:
            current_name = request.name
        
        if request.description is not None:
            current_description = request.description

        if request.is_active is not None:
            if request.is_active is True:
                category.activate()
            else:
                category.deactivate()
        
        self.logger.debug(f'Informações da entidade da categoria que serão enviadas para atualização no banco {category}')
        category.update_category(name=current_name, description=current_description)
        self.repository.update(category)
        self.logger.info(f'Atualização da categoria {request.id} finalizada')
         