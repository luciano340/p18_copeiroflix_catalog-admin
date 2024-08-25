from dataclasses import dataclass
from uuid import UUID
from datetime import date, datetime
from src.core.category.domain.category_repository_interface import CategoryRepositoryInterface
from src.core.category.domain.category import Category

@dataclass
class ListCategoryRequest:
    pass

@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool
    created_date: datetime
    updated_date: datetime

@dataclass
class ListCategoryResponse:
    data: list[CategoryOutput]


class ListCategory:
    def __init__(self, repository: CategoryRepositoryInterface) -> None:
        self.repository = repository
    
    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.list()

        return ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                    created_date=category.created_date,
                    updated_date=category.updated_date
                )
                for category in categories
            ]
        )
