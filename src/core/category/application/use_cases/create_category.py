from dataclasses import dataclass
from re import S
from uuid import UUID
from datetime import datetime
from src._shared.logger import get_logger
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.domain.category import Category

@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""
    is_active: bool = True

@dataclass
class CreateCategoryResponse:
    id: UUID

class CreateCategory:
    def __init__(self, repository: CategoryRepositoryInterface) -> CreateCategoryResponse:
        self.repository = repository
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {repository} - {type(repository)}')
    
    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        self.logger.info(f'Iniciando criação de categoria {request.name}')
        self.logger.debug(f'Argumentos {request} - {type(request)}')
        try:
            category = Category(name=request.name, description=request.description, is_active=request.is_active)
        except ValueError as err:
            self.logger.error(f'As informações fornecidas para a criação da categoria são inválidas - {request} - {type(request)}')
            raise InvalidCategoryData(err)
        
        self.logger.debug(f'Informaçoes persistidas {category} - {type(category)}')
        self.repository.save(category=category)
        self.logger.info(f'Criação da categoria {request.name} finalizada')
        return CreateCategoryResponse(id=category.id)

