from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
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
    
    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        try:
            category = Category(name=request.name, description=request.description, is_active=request.is_active)
        except ValueError as err:
            raise InvalidCategoryData(err)

        self.repository.save(category=category)
        return CreateCategoryResponse(id=category.id)

