from dataclasses import dataclass
from math import log
from uuid import UUID
from datetime import datetime
from src._shared.logger import get_logger
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.use_cases.exceptions import CategoryNotFound

@dataclass
class GetCategoryRequest:
    id: UUID

@dataclass
class GetCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool
    created_date: datetime
    updated_date: datetime

class GetCategory:
    def __init__(self, repository: CategoryRepositoryInterface) -> None:
        self.repository = repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)}')
        
    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        category = self.repository.get_by_id(id=request.id)
        self.logger.info(f'Iniciando procura por categoria {request.id}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')

        if category:
            self.logger.info(f'Categoria {request.id} localizada')
            self.logger.debug(f'Categoria {request.id} localizada - Informações vindas do banco: {category} - {type(category)}')
            return GetCategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_date=category.created_date,
                updated_date=category.updated_date
            )
        
        self.logger.error(f"Categoria {request.id} não localizada")
        raise CategoryNotFound(f"Category with id {request.id} not found")

