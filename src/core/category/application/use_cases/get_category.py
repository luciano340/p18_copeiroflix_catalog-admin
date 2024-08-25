from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
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
    
    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        category = self.repository.get_by_id(id=request.id)

        if category:
            return GetCategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_date=category.created_date,
                updated_date=category.updated_date
            )
        
        raise CategoryNotFound(f"Category with id {request.id} not found")

